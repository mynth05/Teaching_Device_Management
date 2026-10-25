from typing import Callable, Dict, Generic, List, Optional

from exceptions import DuplicateIdException
from interfaces import IRepository, T


class InMemoryRepository(IRepository[T], Generic[T]):
    """Kho lưu trữ tổng quát, dùng dict (tra cứu theo Id O(1), giữ thứ tự thêm vào)."""

    def __init__(self) -> None:
        self._items: Dict[str, T] = {}

    def add(self, item: T) -> None:
        if item is None:
            raise ValueError("Không chấp nhận phần tử None.")
        if item.id in self._items:
            raise DuplicateIdException(item.id)
        self._items[item.id] = item

    def remove(self, id: str) -> bool:
        return self._items.pop(id, None) is not None

    def find_by_id(self, id: str) -> Optional[T]:
        return self._items.get(id)

    def get_all(self) -> List[T]:
        # Trả về bản sao -> mã bên ngoài không sửa được collection nội bộ
        return list(self._items.values())

    def find_all(self, condition: Callable[[T], bool]) -> List[T]:
        return [item for item in self._items.values() if condition(item)]