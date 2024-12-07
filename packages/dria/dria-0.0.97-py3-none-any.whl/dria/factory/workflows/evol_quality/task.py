from dria_workflows import Workflow, WorkflowBuilder, Operator, Write, Edge
from dria.factory.utilities import get_abs_path
from dria.models import TaskResult
from dria.factory.workflows.template import SingletonTemplate
from typing import Dict, List, Any

MUTATION_TEMPLATES: Dict[str, str] = {
    "HELPFULNESS": "Please make the Response more helpful to the user.",
    "RELEVANCE": "Please make the Response more relevant to #Given Prompt#.",
    "DEEPENING": "Please make the Response more in-depth.",
    "CREATIVITY": "Please increase the creativity of the response.",
    "DETAILS": "Please increase the detail level of Response.",
}


class EvolveQuality(SingletonTemplate):

    def workflow(
        self, prompt: str, response: str, method: str = "HELPFULNESS"
    ) -> Workflow:
        """
        Evolve quality of the response to a prompt through rewriting.
        :param prompt:
        :param response:
        :param method: HELPFULNESS | RELEVANCE | DEEPENING | CREATIVITY | DETAILS
        :return:
        """
        self.params.response = response
        self.params.method = method
        selected_method = (
            MUTATION_TEMPLATES[method]
            if method in MUTATION_TEMPLATES
            else MUTATION_TEMPLATES["DETAILS"]
        )
        builder = WorkflowBuilder(
            prompt=prompt, response=response, method=selected_method
        )
        builder.generative_step(
            path=get_abs_path("rewrite.md"),
            operator=Operator.GENERATION,
            outputs=[Write.new("rewritten_response")],
        )
        flow = [Edge(source="0", target="_end")]
        builder.flow(flow)
        builder.set_return_value("rewritten_response")
        return builder.build()

    def parse_result(self, result: List[TaskResult]) -> List[Dict[str, Any]]:
        return [
            {
                "response": self.params.response,
                "evolved_response": r.result.strip(),
                "method": self.params.method,
                "model": r.model,
            }
            for r in result
        ]
