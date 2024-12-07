from typing import List, Dict, Optional, Union, Collection

from tqdm import tqdm

from pythia.evaluators import ClaimEvaluator, utils, SingleClaimEvaluation
from pythia.evaluators._evaluators import Evaluation
from pythia.evaluators.checkers import PythiaV1Checker, Check
from pythia.evaluators.extractors import PythiaV1Extractor
from pythia.evaluators.models import HostedModel
from pythia.template import primary_labels
from pythia import ai_hallucination, validator


class PythiaV1Evaluator(ClaimEvaluator):
    """
    This class implements a simple A-F grade-based evaluator
    """

    def __init__(self, model: HostedModel):
        self._model = model
        self.extractor = PythiaV1Extractor(model)
        self.checker = PythiaV1Checker(model)

    @staticmethod
    def _calculate_metrics(clean_results: List[Check]) -> Dict[str, float]:
        counts = {label: 0 for label in primary_labels}
        for result in clean_results:
            counts[result.category] += 1
        total = sum(counts.values())
        metrics = {m: ct / max(1, total) for m, ct in counts.items()}
        metrics["accuracy"] = utils.calc_accuracy(counts)
        return metrics

    def extract(self, text: str, question: Optional[str], **kwargs) -> List[List[str]]:
        return self.extractor.extract(text, question, **kwargs)

    @property
    def model(self) -> HostedModel:
        return self._model

    def evaluate_summary(self, summary: str, reference: Union[str, List[str]], question: Optional[str] = None,
                         validators_enabled: Optional[bool] = False, **kwargs) -> Evaluation:
        claims = self.extract(summary, question)
        results = self.checker.check_summary(summary, claims, reference, None, question, **kwargs)
        clean_results = [r for r in results if r.category in primary_labels]
        validators_result = None
        if validators_enabled:
            validators_list = validator.ValidatorPool().enabled_validators
            validators_result = ai_hallucination.call_validators(input_reference=reference, input_response=summary,
                                                                 question=question, validators_list=validators_list)
        metrics = PythiaV1Evaluator._calculate_metrics(clean_results)
        claim_evals = [
            SingleClaimEvaluation(claim=c, category=r.category, reasoning=r.reasoning)
            for (c, r) in zip(claims, results)
        ]
        return Evaluation(metrics=metrics, claims=claim_evals, validatorsResults=validators_result)

    def batch_summary(
            self,
            summaries: Collection[str],
            references: Collection[List[str]],
            questions: Optional[Collection[Optional[str]]] = None,
            **kwargs) -> List[Evaluation]:
        assert len(summaries) == len(references)
        if questions is not None:
            data = (summaries, ["\n\n".join(rs) for rs in references], questions)
        else:
            data = (summaries, references)
        assert questions is None or len(summaries) == len(questions)
        return [self.evaluate_summary(*elements, **kwargs) for elements in tqdm(zip(*data))]

    def evaluate_qa(self, answer: str, question: str, context: Optional[Union[str, List[str]]] = None,
                    **kwargs) -> Evaluation:
        if context is None:
            raise ValueError("The PythiaV1 strategy supports Summaries and QA with context")
        claims = self.extract(answer, question)
        results: List[Check] = self.checker.check_summary(answer, claims, context, None, question, **kwargs)
        clean_results = [r for r in results if r.category in primary_labels]
        metrics = PythiaV1Evaluator._calculate_metrics(clean_results)
        claim_evals = [
            SingleClaimEvaluation(claim=c, category=r.category, reasoning=r.reasoning)
            for (c, r) in zip(claims, results)
        ]
        verdict = "PASS" if metrics["accuracy"] >= 0.9 else "FAIL"
        return Evaluation(metrics=metrics, claims=claim_evals, verdict=verdict)

    def batch_qa(
            self,
            answers: Collection[str],
            questions: Collection[str],
            contexts: Optional[Collection[Optional[List[str]]]] = None,
            **kwargs):
        assert len(answers) == len(questions)
        assert contexts is None or len(answers) == len(contexts)
        if contexts is not None:
            data = (answers, questions, ["\n\n".join(cs) for cs in contexts])
        else:
            data = (answers, questions)
        return [self.evaluate_qa(*elements, **kwargs) for elements in tqdm(zip(*data))]
