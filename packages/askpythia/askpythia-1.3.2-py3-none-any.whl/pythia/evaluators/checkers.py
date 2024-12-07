"""
This module contains the classes and functions for the checking logic used in some evaluators
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Union, Optional

from pythia.evaluators import utils
from pythia.evaluators.models import HostedModel
from pythia.evaluators.prompts import pythiav1
from pythia.template import label_neutral, label_entailment, label_contradiction


@dataclass
class Check:
    """Dataclass for the results from claim or statement checking"""
    category: str
    reasoning: Union[str, List[str]]


class BaseChecker(ABC):
    @abstractmethod
    def check_summary(
            self,
            summary: str, summary_extraction: List[Union[str, List[str]]],
            reference: Union[str, List[str]], reference_extraction: Optional[List[Union[str, List[str]]]] = None,
            question: Optional[str] = None, **kwargs) -> List[Check]:
        """
        This method checks the extracted claims or statements from a summary against the reference or reference
        claims or statements
        :param summary: this is the text of the generated summary
        :param summary_extraction: this is the extracted claims (`List[List[str]]`) or extracted statements
        (`List[str]`) from the summary
        :param reference: this is the reference text(s)
        :param reference_extraction: this is the extracted claims (`List[List[str]]`) or extracted statements
        (`List[str]`) from the reference(s)
        :param question: This is an optional question that can be used as a focus of the claim or statement checking.
        For example, if this is a summary of a set of patient documents then you can focus the checking with the
        question "What drugs have been prescribed?"
        :param kwargs: these arguments can be used to provide arguments for functions and methods used to
        evaluate. For example, if an evaluator uses a call to an LLM, the temperature can be supplied by the kwargs
        :return: The list of checks of the summary claims or statements
        """
        pass

    @abstractmethod
    def check_qa(
            self,
            answer: str, answer_extraction: List[Union[str, List[str]]],
            question: str,
            context: Optional[Union[str, List[str]]],
            context_extraction: Optional[List[Union[str, List[str]]]] = None,
            **kwargs) -> List[Check]:
        """
        This method checks the extracted claims or statements from an answer against the question and optionally
        context or context claims or statements
        :param answer: this is the text of the generated summary
        :param answer_extraction: this is the extracted claims (`List[List[str]]`) or extracted statements
        (`List[str]`) from the summary
        :param question: The question posed to the system
        :param context: this is the context text(s)
        :param context_extraction: this is the extracted claims (`List[List[str]]`) or extracted statements
        (`List[str]`) from the context(s)
        :param kwargs: these arguments can be used to provide arguments for functions and methods used to
        evaluate. For example, if an evaluator uses a call to an LLM, the temperature can be supplied by the kwargs
        :return: The list of checks of the answer claims or statements
        """
        pass


class PythiaV1Checker(BaseChecker):
    def __init__(self, model: HostedModel):
        self.model = model

    def check_summary(self, summary: str, summary_extraction: List[Union[str, List[str]]],
                      reference: Union[str, List[str]],
                      reference_extraction: Optional[List[Union[str, List[str]]]] = None,
                      question: Optional[str] = None, **kwargs) -> List[Check]:
        if not isinstance(reference, list):
            reference = [reference]
        messages = []
        for ref in reference:
            for claim in summary_extraction:
                claim = " ".join(claim)
                if question:
                    prompt = pythiav1.LLM_CHECKING_PROMPT_Q.format(reference=ref, question=question, claim=claim)
                else:
                    prompt = pythiav1.LLM_CHECKING_PROMPT.format(reference=ref, claim=claim)
                messages.append([{"role": "user", "content": prompt}])
        raw_results = utils.parallel_batch_model_call(messages, self.model, verbose=False, **kwargs)
        results = []
        for result in raw_results:
            if not result or len(result) == 0:
                results.append(Check("N/A", "empty result"))
                continue
            clean = result.strip().lower()
            if clean.startswith(label_entailment):
                results.append(Check(label_entailment, result))
            elif clean.startswith(label_contradiction):
                results.append(Check(label_contradiction, result))
            elif clean.startswith(label_neutral):
                results.append(Check(label_neutral, result))
            else:
                results.append(Check("N/A", "unrecognized category"))
        return results

    def check_qa(
            self,
            answer: str, answer_extraction: List[Union[str, List[str]]],
            question: str,
            context: Optional[Union[str, List[str]]],
            context_extraction: Optional[List[Union[str, List[str]]]] = None,
            **kwargs) -> List[Check]:
        if context is None:
            raise ValueError("The PythiaV1 strategy only supports QA with context")
        if not isinstance(context, list):
            context = [context]
        messages = []
        for ctx in context:
            for claim in answer_extraction:
                claim = " ".join(claim)
                if question:
                    prompt = pythiav1.LLM_CHECKING_PROMPT_Q.format(reference=ctx, question=question, claim=claim)
                else:
                    prompt = pythiav1.LLM_CHECKING_PROMPT.format(reference=ctx, claim=claim)
                messages.append([{"role": "user", "content": prompt}])
        raw_results = utils.batch_model_call(messages, self.model, **kwargs)
        results = []
        for result in raw_results:
            if not result or len(result) == 0:
                results.append(Check("N/A", "empty result"))
                continue
            clean = result.strip().lower()
            if clean.startswith(label_entailment):
                results.append(Check(label_entailment, result))
            elif clean.startswith(label_contradiction):
                results.append(Check(label_contradiction, result))
            elif clean.startswith(label_neutral):
                results.append(Check(label_neutral, result))
            else:
                results.append(Check("N/A", "unrecognized category"))
        return results


__all__ = ["Check", "BaseChecker", "PythiaV1Checker"]
