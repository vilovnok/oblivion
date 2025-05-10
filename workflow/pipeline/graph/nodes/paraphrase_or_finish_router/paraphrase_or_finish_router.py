from typing import Dict, Literal

from workflow.pipeline.graph.nodes._base import _BaseRouter
from workflow.pipeline.graph.state import State





class ParaphraseOrFinishRouter(_BaseRouter):
    """
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

        if self.show_logs:
            print(self.name)
            print("----------------")

        if state.history[-1].content:
            return "yes"
        else:
            return "no"
