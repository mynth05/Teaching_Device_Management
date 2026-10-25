from typing import Callable, Generic, Optional, TypeVar

from exceptions import DeviceNotReadyException
from interfaces import IRepository, ISelectionStrategy
from teaching_device import TeachingDevice

D = TypeVar("D", bound=TeachingDevice)


class AllocationService(Generic[D]):
    """Dịch vụ cấp phát tổng quát: chỉ phụ thuộc IRepository[D] và ISelectionStrategy[D]."""

    def __init__(self, repository: IRepository[D], strategy: ISelectionStrategy[D]) -> None:
        if repository is None or strategy is None:
            raise ValueError("repository và strategy không được None.")
        self._repository = repository
        self._strategy = strategy

    def change_strategy(self, new_strategy: ISelectionStrategy[D]) -> None:
        if new_strategy is None:
            raise ValueError("strategy không được None.")
        self._strategy = new_strategy

    def allocate(self, additional_condition: Optional[Callable[[D], bool]] = None) -> D:
        # 1-3. Lấy từ repo, giữ thiết bị sẵn sàng, áp điều kiện bổ sung
        candidates = self._repository.find_all(
            lambda d: d.is_ready_for_use() and (additional_condition is None or additional_condition(d))
        )
        # 4. Chọn bằng chiến lược hiện tại (ném NoSuitableItemException nếu rỗng)
        selected = self._strategy.select(candidates)
        # 5-6. Mượn và trả về
        selected.borrow()
        return selected

    def release(self, device_id: str) -> D:
        """Trả thiết bị về kho."""
        device = self._repository.find_by_id(device_id)
        if device is None:
            raise KeyError(f"Không tìm thấy thiết bị '{device_id}'.")
        device.return_device()
        return device