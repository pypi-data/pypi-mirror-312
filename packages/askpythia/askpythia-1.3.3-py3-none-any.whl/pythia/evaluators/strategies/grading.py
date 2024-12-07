import json
from typing import Union, List, Optional, Dict

from pythia.evaluators import SimpleEvaluator, utils
from pythia.evaluators._evaluators import Evaluation
from pythia.evaluators.models import HostedModel
from pythia.evaluators.prompts import grading


class GradeEvaluator(SimpleEvaluator):
    """
    This class implements a simple A-F grade-based evaluator
    """

    default_grade_scale = {
        "A": 0.96,
        "B": 0.75,
        "C": 0.50,
        "D": 0.20,
        "F": 0.00
    }

    def __init__(self, model: HostedModel, grade_scale: Optional[Dict[str, float]] = None, default_score: float = 0.0):
        self._model = model
        if grade_scale:
            self.grade_scale = grade_scale
        else:
            self.grade_scale = GradeEvaluator.default_grade_scale

    @property
    def model(self) -> HostedModel:
        return self._model

    def _create_summary_call(
            self,
            summary: str,
            reference: Union[str, List[str]],
            question: Optional[str] = None) -> List[Dict[str, str]]:
        if isinstance(reference, list):
            reference = "\n\n".join(reference)
        if question is None:
            system_message = grading.GRADING_SUMMARY_SYSTEM
            user_message = grading.GRADING_SUMMARY_TEMPLATE.format(
                summary=summary,
                reference=reference
            )
        else:
            system_message = grading.GRADING_SUMMARY_W_Q_SYSTEM
            user_message = grading.GRADING_SUMMARY_W_Q_TEMPLATE.format(
                summary=summary,
                question=question,
                reference=reference,
            )
        return [{
                "role": "system",
                "content": system_message
            }, {
                "role": "user",
                "content": user_message
            }]

    def _create_qa_call(
            self,
            answer: str,
            question: str,
            context: Optional[Union[str, List[str]]] = None) -> List[Dict[str, str]]:
        if isinstance(context, list):
            context = "\n\n".join(context)
        if context is None:
            system_message = grading.GRADING_NO_CONTEXT_QA_SYSTEM
            user_message = grading.GRADING_NO_CONTEXT_QA_TEMPLATE.format(
                answer=answer,
                question=question,
            )
        else:
            system_message = grading.GRADING_QA_SYSTEM
            user_message = grading.GRADING_QA_TEMPLATE.format(
                answer=answer,
                question=question,
                context=context,
            )
        return [{
                "role": "system",
                "content": system_message
            }, {
                "role": "user",
                "content": user_message
            }]

    def _process_summary_response(self, response: str) -> Evaluation:
        try:
            result = utils.parse_json_result(response)
            result["metrics"] = {"score": self.grade_scale.get(result["verdict"][0], self.default_grade_scale)}
        except AttributeError:
            return Evaluation(reasoning=json.dumps({
                "error": "ValueError",
                "text": response,
            }))
        return Evaluation(**result)

    def _process_qa_response(self, response: str) -> Evaluation:
        try:
            result = utils.parse_json_result(response)
            result["metrics"] = {"score": self.grade_scale.get(result["verdict"][0], self.default_grade_scale)}
        except AttributeError:
            return Evaluation(reasoning=json.dumps({
                "error": "ValueError",
                "text": response,
            }))
        return Evaluation(**result)
