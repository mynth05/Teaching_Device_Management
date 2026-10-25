from abc import ABC, abstractmethod
from typing import Optional, List, TypeVar, Generic, Callable

class IIdentifiable(ABC):
    """Đối tượng có mã định danh -> cho phép repository tìm theo Id."""
    @property
    @abstractmethod
    def id(self)->str:...

T = TypeVar("T", bound = IIdentifiable)
S = TypeVar("S")
class IRepository(ABC, Generic[T]):
    @abstractmethod
    def add(self, item: T) -> None: ...
 
    @abstractmethod
    def remove(self, id: str) -> bool: ...
 
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[T]: ...
 
    @abstractmethod
    def get_all(self) -> List[T]: ...
 
    @abstractmethod
    def find_all(self, condition: Callable[[T], bool]) -> List[T]: ...
 
 
class ISelectionStrategy(ABC, Generic[S]):
    @abstractmethod
    def select(self, candidates: List[S]) -> S: ...

        