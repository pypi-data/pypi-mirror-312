import json
import re
from typing import Union, List, Optional, Dict

from pythia.evaluators import SimpleEvaluator, utils
from pythia.evaluators._evaluators import Evaluation
from pythia.evaluators.models import HostedModel
from pythia.evaluators.prompts import lynx_qa


class LynxQA(SimpleEvaluator):
    """
    This class implements the methodology from the Lynx paper
    https://arxiv.org/abs/2407.08488
    Lynx: An Open Source Hallucination Evaluation Model
    Selvan Sunitha Ravi, Bartosz Mielczarek, Anand Kannappan, Douwe Kiela, Rebecca Qian
    """
    def __init__(self, model: HostedModel):
        self._model = model

    @staticmethod
    def _process_result(result: str):
        result = result.strip().strip("`")
        result = result[result.index("{"):result.rindex("}")+1]
        if re.match("""^{\\s*"reasoning"\\s*:\\s*\\[\\s*[^"]""", result, re.M):
            reasoning_start = result.index("[")
            reasoning_end = result.index("]")
            reasoning = result[reasoning_start:reasoning_end+1]
            reasoning = '["' + reasoning[1:-1].replace("\n", "\\n") + '"]'
            result = result[:reasoning_start] + reasoning + result[reasoning_end+1:]
        return result

    @property
    def model(self) -> HostedModel:
        return self._model

    def _create_summary_call(
            self,
            summary: str,
            reference: Union[str, List[str]],
            question: Optional[str] = None) -> List[Dict[str, str]]:
        raise NotImplementedError("The Lynx strategy only supports QA with context like RAG QA")

    def _create_qa_call(
            self,
            answer: str,
            question: str,
            context: Optional[Union[str, List[str]]] = None) -> List[Dict[str, str]]:
        if isinstance(context, list):
            context = "\n\n".join(context)
        if context is None:
            raise ValueError("The Lynx strategy requires a context")
        return [{
                "role": "system",
                "content": lynx_qa.SIMPLE_QA_SYSTEM
            }, {
                "role": "user",
                "content": lynx_qa.SIMPLE_QA_TEMPLATE.format(
                    answer=answer,
                    question=question,
                    context=context,
                )
            }]

    def _process_summary_response(self, response: str) -> Evaluation:
        raise NotImplementedError("The Lynx strategy only supports QA with context like RAG QA")

    def _process_qa_response(self, response: str) -> Evaluation:
        try:
            result = utils.parse_json_result(response)
            result["metrics"] = {"score": 1.0 if result["verdict"].upper() == "PASS" else 0.0}
        except AttributeError:
            return Evaluation(reasoning=json.dumps({
                "error": "ValueError",
                "text": response,
            }))
        return Evaluation(**result)

    def evaluate_summary(
            self,
            summary: str,
            reference: Union[str, List[str]],
            question: Optional[str] = None,
            **kwargs) -> Evaluation:
        raise NotImplementedError("The Lynx strategy only supports QA with context like RAG QA")
