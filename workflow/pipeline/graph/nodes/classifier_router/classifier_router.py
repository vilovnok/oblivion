from typing import Dict, Literal

from workflow.pipeline.graph.nodes._base import _BaseRouter
from workflow.pipeline.graph.state import State


class ClassifierRouter(_BaseRouter):
    """
    Router Node to retranslate classifier node output to Retriever or Operator nodes.
    """

    def __init__(
        self,
        name: str,
        description: str,
        mapping: Dict,
        show_logs: bool = False,
    ) -> None:
        super().__init__(name, description, mapping)
        self.show_logs = show_logs

    def invoke(self, state: State) -> Literal["no", "yes"]:
        label = state.label
        history = state.history

        if self.show_logs:
            print(self.name)
            print(f"Count of text: {label}")
            print(f"Length texts: {len(history[-1].content)}")
            print("----------------")

        return label