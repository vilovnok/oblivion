from langchain_core.output_parsers import StrOutputParser, BaseOutputParser

from workflow.pipeline.graph.nodes._base import _BaseNode
from workflow.pipeline.graph.llms._base import _BaseLLM
from workflow.pipeline.graph.state import State


class ClassifierNode(_BaseNode):
    """
    Classifier Node to classify input query (user input) in categories.
    """

    def __init__(
        self,
        name: str,
        description: str,
        prompt: str = None,
        model_name: str = "Qwen/Qwen2.5-7B-Instruct",
        port: int = 7987,
        show_logs: bool = False,
    ) -> None:
        super().__init__(name=name, description=description, prompt=prompt, model_name=model_name, port=port)
        self.show_logs = show_logs

    def invoke(self, state: State):
        if self.show_logs:
            print(self.name)            
            print("----------------")

        return {
            "history": state.history,
            "label": state.label
        }
