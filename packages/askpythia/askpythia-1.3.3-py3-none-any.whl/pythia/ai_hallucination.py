import concurrent
import json
import multiprocessing
import os
import base64
from openai import OpenAI
import time
from collections import Counter
from litellm import batch_completion
from openai import RateLimitError as OpenAIRateLimitError
from openai import APIError as OpenAIAPIError
from openai import Timeout as OpenAITimeout
from tqdm import tqdm
from pythia.prompt_gpt import LLM_CHECKING_PROMPT, LLM_CHECKING_PROMPT_Q
from pythia.llm_extractor import llm_extractor
from pythia.template import primary_labels, label_contradiction, label_entailment, label_neutral
from pythia.validator_call import ValidatorCall

model_name = os.getenv("MODEL_NAME", "gpt-4o")


def get_model_batch_response(prompts, max_new_tokens=500, temperature=0, model=model_name):
    if not prompts or len(prompts) == 0:
        raise ValueError("Invalid input.")

    message_list = []
    for prompt in prompts:
        if len(prompt) == 0:
            raise ValueError("Invalid prompt.")
        if isinstance(prompt, str):
            messages = [{
                'role': 'user',
                'content': prompt
            }]
        elif isinstance(prompt, list):
            messages = prompt
        else:
            raise ValueError("Invalid prompt type.")
        message_list.append(messages)
    import litellm
    litellm.suppress_debug_info = True
    while True:
        try:
            responses = batch_completion(
                model=model,
                messages=message_list,
                temperature=temperature,
                n=1,
                max_tokens=max_new_tokens
            )
            response_list = [r.choices[0].message.content for r in responses]
            for r in response_list:
                if not r or len(r) == 0:
                    raise ValueError(f'{model} API returns None or empty string')
            return response_list
        except Exception as e:
            if isinstance(e, OpenAIRateLimitError) or isinstance(e, OpenAIAPIError) or isinstance(e, OpenAITimeout):
                print(f"{e} [sleep 10 seconds]")
                time.sleep(10)
                continue
            print(e)
            return None


def llm_check(claims, reference, question=None, batch_size=16, temperature=0.0, model=model_name):
    ret_labels = []
    prompt_list = []

    for claim in claims:
        claim = f"({claim[0]}, {claim[1]}, {claim[2]})"
        if question is None:
            prompt = LLM_CHECKING_PROMPT.format(
                reference=reference,
                claim=claim
            )
        else:
            prompt = LLM_CHECKING_PROMPT_Q.format(
                question=question,
                reference=reference,
                claim=claim
            )
        prompt_list.append(prompt)

    for i in tqdm(range(0, len(prompt_list), batch_size)):
        batch_prompts = prompt_list[i:i + batch_size]
        llm_responses = get_model_batch_response(
            prompts=batch_prompts,
            temperature=temperature,
            model=model,
            max_new_tokens=10,
        )
        for llm_response in llm_responses:
            if llm_response and len(llm_response):
                label = None
                if label_contradiction in llm_response.lower():
                    label = label_contradiction
                elif label_entailment in llm_response.lower():
                    label = label_entailment
                else:
                    label = label_neutral
                ret_labels.append(label)
            else:
                raise 'API returns None or empty string'
    return ret_labels


def parallel_llm_check(claims, references, question=None, batch_size=16, temperature=0.0, model=model_name):
    num_cpus = multiprocessing.cpu_count()
    max_workers = min(num_cpus, len(references))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(llm_check, claims, reference, question, batch_size, temperature, model)
                   for reference
                   in references]

    results = [future.result() for future in futures]
    merged_list = [item for sublist in results for item in sublist]
    return merged_list


def calc_accuracy(e, c, r=None, we=1, wc=1, wr=0):
    eps = 1e-10
    if r is None or wr == 0:
        r = 1.0
        wr = 0
    accuracy = (we + wc + wr) / (we * (1 / (e + eps)) + wc * (1 / (1 - c + eps)) + wr * (1 / (r + eps)))
    return round(accuracy, ndigits=9)


# call each validator using the name from the input
def call_method(validator, obj, method_name, *args, **kwargs):
    method = getattr(obj, method_name, None)
    if callable(method):
        return method(validator=validator, **kwargs)
    else:
        raise AttributeError(f"Method {method_name} not found in {obj}")


from concurrent.futures import ThreadPoolExecutor, as_completed


def call_validators(input_reference, input_response, question=None, validators_list=None):
    if validators_list is None:
        return None
    if len(validators_list) == 0:
        return None
    validators_data = []
    validator_class = ValidatorCall()

    def call_validator(validator):
        validator_name = validator['name']
        print("Execute Validator {}".format(validator_name))
        try:
            validator_data = call_method(
                validator, validator_class, validator_name,
                input_reference=input_reference,
                input_response=input_response,
                question=question
            )
            return validator_data
        except Exception as e:
            print("Fail to execute validation for validator {}. Exception {}".format(validator_name, e))
            return [{
                "validatedField": "",
                "validator": validator,
                "isValid": False,
                "errorMessage": str(e),
                "riskScore": 1
            }]

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(call_validator, validator) for validator in validators_list]
        for future in as_completed(futures):
            validators_data.extend(future.result())
    print("Validators executed ...")

    return validators_data


def ask_pythia_method(input_reference, input_response, question=None):
    claims = llm_extractor(input_response, question=question)
    classes = parallel_llm_check(claims, input_reference, question=question)
    metrics = Counter(classes)
    metrics.update({label: 0 for label in primary_labels})
    if classes:
        metrics = {c: n / max(len(classes), 1) for c, n in metrics.items()}
    metrics["accuracy"] = calc_accuracy(metrics[label_entailment], metrics[label_contradiction])
    triples = []
    for claim, clazz in zip(claims, classes):
        triples.append({
            "claim": claim,
            "class": clazz
        })

    return {
        "claims": triples,
        "metrics": metrics
    }


def ask_pythia(input_reference, input_response, question=None, validators_list=None):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future1 = executor.submit(
            ask_pythia_method, input_reference, input_response, question)
        future2 = executor.submit(call_validators, input_reference, input_response, question, validators_list)

        pythia_results = future1.result()
        validator_results = future2.result()
    if validator_results is None:
        return pythia_results
    pythia_results["validatorsResults"] = validator_results
    return pythia_results

