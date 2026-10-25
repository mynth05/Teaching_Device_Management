from device_status import DeviceStatus
from abc import ABC, abstractmethod
from exceptions import DeviceNotReadyException
from interfaces import IIdentifiable


def _require_text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} không hợp lệ.")
    return value.strip()
 
 
def require_percent(value: int, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 100:
        raise ValueError(f"{field} phải là số nguyên từ 0 đến 100.")
    return value
 
 
class TeachingDevice(IIdentifiable, ABC):
    """Lớp cơ sở trừu tượng: cấu trúc + hành vi chung (mượn/trả).
    Hành vi thay đổi theo loại thiết bị: is_ready_for_use, get_default_priority_score."""
 
    def __init__(self, id: str, name: str, storage_location: str) -> None:
        self._id = _require_text(id, "Id")
        self._name = _require_text(name, "Name")
        self._storage_location = _require_text(storage_location, "StorageLocation")
        self._status = DeviceStatus.Available
 
    @property
    def id(self) -> str:
        return self._id
 
    @property
    def name(self) -> str:
        return self._name
 
    @property
    def storage_location(self) -> str:
        return self._storage_location
 
    @property
    def status(self) -> DeviceStatus:
        return self._status
 
    # ---- hành vi đa hình ----
    @abstractmethod
    def is_ready_for_use(self) -> bool: ...
 
    @abstractmethod
    def get_default_priority_score(self) -> float: ...
 
    # ---- hành vi chung ----
    def borrow(self) -> None:
        if not self.is_ready_for_use():
            raise DeviceNotReadyException(self.id, self._status)
        self._status = DeviceStatus.Borrowed
 
    def return_device(self) -> None:
        if self._status != DeviceStatus.Borrowed:
            raise DeviceNotReadyException(
                self.id, self._status, f"Thiết bị '{self.id}' không ở trạng thái Borrowed nên không thể trả."
            )
        self._status = DeviceStatus.Available
 
    def send_to_maintenance(self) -> None:
        if self._status != DeviceStatus.Available:
            raise DeviceNotReadyException(self.id, self._status)
        self._status = DeviceStatus.UnderMaintenance
 
    def finish_maintenance(self) -> None:
        if self._status != DeviceStatus.UnderMaintenance:
            raise DeviceNotReadyException(self.id, self._status)
        self._status = DeviceStatus.Available
 
    def __repr__(self) -> str:
        return f"{type(self).__name__}(id={self.id!r}, status={self._status.value})"