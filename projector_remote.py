from teaching_device import  TeachingDevice, require_percent
from device_status import DeviceStatus

class ProjectorRemote(TeachingDevice):
    MIN_BATTERY = 20

    def __init__(self, id: str, name: str, storage_location: str, battery_level: int) -> None:
        super().__init__(id, name, storage_location)
        self._battery_level = require_percent(battery_level, "BatteryLevel")

    @property
    def battery_level(self) -> int:
        return self._battery_level

    def is_ready_for_use(self) -> bool:
        return self.status == DeviceStatus.Available and self._battery_level >= self.MIN_BATTERY

    def get_default_priority_score(self) -> float:
        return float(self._battery_level)