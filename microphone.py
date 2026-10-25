from teaching_device import TeachingDevice, require_percent
from device_status import DeviceStatus


class WirelessMicrophone(TeachingDevice):
    MIN_BATTERY = 30
    MIN_SIGNAL = 40

    def __init__(self, id: str, name: str, storage_location: str, battery_level: int, signal_quality: int) -> None:
        super().__init__(id, name, storage_location)
        self._battery_level = require_percent(battery_level, "BatteryLevel")
        self._signal_quality = require_percent(signal_quality, "SignalQuality")

    @property
    def battery_level(self) -> int:
        return self._battery_level

    @property
    def signal_quality(self) -> int:
        return self._signal_quality

    def is_ready_for_use(self) -> bool:
        return (
            self.status == DeviceStatus.Available
            and self._battery_level >= self.MIN_BATTERY
            and self._signal_quality >= self.MIN_SIGNAL
        )

    def get_default_priority_score(self) -> float:
        return (self._battery_level + self._signal_quality) / 2