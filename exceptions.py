from device_status import DeviceStatus
class DuplicateIdException(Exception):
    """Ném ra khi phần tử có Id đã tồn tại trong repository"""
    def __init__(self, duplicate_id: str):
        super().__init__(f" Id '{duplicate_id}' đã tồn tại")
        self.duplicate_id = duplicate_id

class NoSuitableItemException(Exception):
    """Ném ra khi không có đối tượng phù hợp để chọn/ cấp phát"""

    def __init__(self, message: str = "Không có thiết bị phù hợp."):
        super().__init__(message)

class DeviceNotReadyException(Exception):
    """Ném ra khi thiết bị không ở trạng thái phù hợp để mượn/ trả"""
    def __init__(self, device_id: str, current_status = DeviceStatus,message: str = "" ):
        super().__init__(
            message or f"Thiết bị '{device_id}' chưa sẵn sàng (trạng thái: 'current_status.value')"
        )
        self.device_id = device_id
        self.current_status = current_status