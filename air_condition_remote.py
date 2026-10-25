from typing import FrozenSet, Iterable, Optional

from teaching_device import TeachingDevice
from device_status import DeviceStatus

class AirConditionerRemote(TeachingDevice):
    def __init__(self, id: str, name: str, storage_location: str, compatible_rooms: Iterable[str]) -> None:
        super().__init__(id, name, storage_location)
        self._compatible_rooms: FrozenSet[str] = frozenset(compatible_rooms)

    @property
    def compatible_rooms(self) -> FrozenSet[str]:  # bất biến -> chỉ đọc
        return self._compatible_rooms

    def is_compatible_with(self, room_id: str) -> bool:
        return room_id in self._compatible_rooms

    def is_ready_for_use(self) -> bool:
        return self.status == DeviceStatus.Available

    def get_default_priority_score(self, room_id: Optional[str] = None) -> float:
        """100 nếu tương thích, ngược lại 0.
        Không truyền room_id: coi là tương thích nếu remote hỗ trợ ít nhất một phòng."""
        compatible = bool(self._compatible_rooms) if room_id is None else self.is_compatible_with(room_id)
        return 100.0 if compatible else 0.0