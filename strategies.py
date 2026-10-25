from typing import Callable, Generic, List

from exceptions import NoSuitableItemException
from interfaces import ISelectionStrategy, S


class HighestPriorityStrategy(ISelectionStrategy[S], Generic[S]):
    """Chọn phần tử có điểm cao nhất; hàm tính điểm được truyền từ bên ngoài."""

    def __init__(self, score_selector: Callable[[S], float]) -> None:
        self._score_selector = score_selector

    def select(self, candidates: List[S]) -> S:
        if not candidates:
            raise NoSuitableItemException()
        return max(candidates, key=self._score_selector)  # không sửa danh sách đầu vào


class FirstAvailableStrategy(ISelectionStrategy[S], Generic[S]):
    """Chọn phần tử đầu tiên trong danh sách ứng viên."""

    def select(self, candidates: List[S]) -> S:
        if not candidates:
            raise NoSuitableItemException()
        return candidates[0]