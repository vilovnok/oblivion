from langchain_core.output_parsers import StrOutputParser, BaseOutputParser

from workflow.pipeline.graph.nodes._base import _BaseNode
from workflow.pipeline.graph.llms._base import _BaseLLM
from workflow.pipeline.graph.state import State


class GenerateQueryNode(_BaseNode):
    """
    
    """

    def __init__(
        self,
        name: str,
        description: str,
        llm: _BaseLLM,
        prompt: str = None,
        output_parser: BaseOutputParser = StrOutputParser(),
        show_logs: bool = False,
    ) -> None:
        super().__init__(name, description, llm, prompt, output_parser)
        self.show_logs = show_logs

    def invoke(self, state: State):
        if self.show_logs:
            print(self.name)            
            print("----------------")

        return {
            "history": state.history,
            "label": state.label
        }
