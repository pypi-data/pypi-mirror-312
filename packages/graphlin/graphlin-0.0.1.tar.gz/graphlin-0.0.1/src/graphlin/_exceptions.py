class GraphlinException(Exception):
    """Base class for all Graphlin exceptions."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class GraphlinConnectionError(GraphlinException):
    """Raised when Gremlin connection fails."""


class GraphlinValidationError(GraphlinException):
    """Raised when validation of a change fails."""


class NodeNotFound(GraphlinException):
    """Raised when a node is not found."""

    def __init__(self, node_id: str):
        self.node_id = node_id
        super().__init__(f"Node with ID {node_id} not found.")


class EdgeNodeNotFound(GraphlinException):
    """Raised when a node is not found."""

    def __init__(self, node_id: str):
        self.node_id = node_id
        super().__init__(f"Cannot create edge to node with ID {node_id} because it does not exist.")
