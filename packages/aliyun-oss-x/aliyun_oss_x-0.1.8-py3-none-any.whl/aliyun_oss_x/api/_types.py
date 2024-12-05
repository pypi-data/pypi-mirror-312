from typing import TypeVar, Any, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from httpx._types import ProxyTypes, HeaderTypes

    class ResultProtocol(Protocol):
        def __init__(self, resp: Any) -> None: ...

    ResultType = TypeVar("ResultType", bound=ResultProtocol)

    __all__ = ["ResultType", "ProxyTypes", "HeaderTypes"]
