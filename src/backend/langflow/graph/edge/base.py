# Path: src/backend/langflow/graph/edge/base.py
from langflow.utils.logger import logger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langflow.graph.vertex.base import Vertex


class Edge:
    def __init__(self, source: "Vertex", target: "Vertex", raw_edge: dict):
        self.source: "Vertex" = source
        self.target: "Vertex" = target
        self.source_handle = raw_edge.get("sourceHandle", "")
        self.target_handle = raw_edge.get("targetHandle", "")
        # 'BaseLoader;BaseOutputParser|documents|PromptTemplate-zmTlD'
        # target_param is documents
        self.target_param = self.target_handle.split("|")[1]

        self.validate_edge()
        self.parse_target_handle(raw_edge)

    def parse_target_handle(self, raw_edge: dict) -> None:
        # handle structure: base_class|type|id for target
        # handle structure: name|id|base_classes for source
        _target_handle = raw_edge["targetHandle"]
        self._target_handle_parts = _target_handle.split("|")
        # This param can be used to pass data to the target
        self._target_param_key = self._target_handle_parts[1]

    def validate_edge(self) -> None:
        # Validate that the outputs of the source node are valid inputs
        # for the target node
        self.source_types = self.source.output
        self.target_reqs = self.target.required_inputs + self.target.optional_inputs
        # Both lists contain strings and sometimes a string contains the value we are
        # looking for e.g. comgin_out=["Chain"] and target_reqs=["LLMChain"]
        # so we need to check if any of the strings in source_types is in target_reqs
        self.valid = any(
            output in target_req
            for output in self.source_types
            for target_req in self.target_reqs
        )
        # Get what type of input the target node is expecting
        self.matched_type = next(
            (output for output in self.source_types if output in self.target_reqs),
            None,
        )
        no_matched_type = self.matched_type is None
        if no_matched_type:
            logger.debug(self.source_types)
            logger.debug(self.target_reqs)
        if no_matched_type:
            raise ValueError(
                f"Edge between {self.source.vertex_type} and {self.target.vertex_type} "
                f"has no matched type"
            )

    def __repr__(self) -> str:
        return f"{self.source.vertex_type} -> {self.target.vertex_type}"

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __eq__(self, __value: object) -> bool:
        return (
            self.__repr__() == __value.__repr__()
            if isinstance(__value, Edge)
            else False
        )
