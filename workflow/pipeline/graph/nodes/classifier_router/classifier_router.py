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
        """
        Initialize the ClassifierRouter.

        Args:
            name (str): Name of the node.
            description (str): Description of the node's purpose.
            mapping (Dict): Mapping for routing decisions.
            show_logs (bool): Flag to enable or disable logging.
        """
        super().__init__(name, description, mapping)
        self.show_logs = show_logs

    def invoke(self, state: State) -> Literal["no", "yes"]:
        """
        Determine the next step based on the catalog and category names.

        Args:
            state (State): Current state of the workflow.

        Returns:
            Literal["extract", "no_info"]: Determines whether to return "profile" or "no_info".
        """
        
        label = state.label
        history = state.history
        if self.show_logs:
            print(self.name)
            print(f"Label: {label}")
            print(f"Length texts: {len(history[-1].content)}")
            print("----------------")

        return label