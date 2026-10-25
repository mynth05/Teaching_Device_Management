"""Kịch bản kiểm thử theo mục 9 của đề bài. Chạy: python main.py"""
from allocation_service import AllocationService
from exceptions import DuplicateIdException, NoSuitableItemException
from repository import InMemoryRepository
from strategies import FirstAvailableStrategy, HighestPriorityStrategy
from air_condition_remote import AirConditionerRemote
from projector_remote import ProjectorRemote
from microphone import WirelessMicrophone
from device_status import DeviceStatus


def title(text: str) -> None:
    print(f"\n=== {text} ===")


def main() -> None:
    # Dữ liệu mẫu
    projectors = [
        ProjectorRemote("PJ01", "Remote Epson", "Kho A", 85),
        ProjectorRemote("PJ02", "Remote Sony", "Kho A", 45),
        ProjectorRemote("PJ03", "Remote BenQ", "Kho B", 10),   # pin < 20 -> chưa sẵn sàng
    ]
    acs = [
        AirConditionerRemote("AC01", "Remote Daikin", "Kho A", {"A203", "A204"}),
        AirConditionerRemote("AC02", "Remote LG", "Kho B", {"B101"}),
    ]
    mics = [
        WirelessMicrophone("MIC01", "Micro Shure", "Kho C", 90, 80),
        WirelessMicrophone("MIC02", "Micro Sony", "Kho C", 50, 30),   # tín hiệu < 40
        WirelessMicrophone("MIC03", "Micro Boya", "Kho C", 40, 70),
    ]

    # 1. Thêm thiết bị vào repository (cùng một lớp generic cho 3 loại -> yêu cầu 11)
    title("1. Thêm thiết bị")
    pj_repo: InMemoryRepository[ProjectorRemote] = InMemoryRepository()
    ac_repo: InMemoryRepository[AirConditionerRemote] = InMemoryRepository()
    mic_repo: InMemoryRepository[WirelessMicrophone] = InMemoryRepository()
    for d in projectors: pj_repo.add(d)
    for d in acs: ac_repo.add(d)
    for d in mics: mic_repo.add(d)
    print(f"Máy chiếu: {len(pj_repo.get_all())}, Điều hòa: {len(ac_repo.get_all())}, Micro: {len(mic_repo.get_all())}")

    # 2. Thêm trùng mã
    title("2. Thêm trùng mã")
    try:
        pj_repo.add(ProjectorRemote("PJ01", "Bản sao", "Kho A", 50))
    except DuplicateIdException as e:
        print("DuplicateIdException:", e, "| DuplicateId =", e.duplicate_id)

    # 3. Tìm theo mã
    title("3. Tìm theo mã")
    print("PJ02  ->", pj_repo.find_by_id("PJ02"))
    print("XXXX  ->", pj_repo.find_by_id("XXXX"))
    print("remove('XXXX') ->", pj_repo.remove("XXXX"))

    # 4. Lọc thiết bị sẵn sàng
    title("4. Lọc thiết bị sẵn sàng")
    print("Máy chiếu sẵn sàng:", pj_repo.find_all(lambda d: d.is_ready_for_use()))
    print("Micro sẵn sàng    :", mic_repo.find_all(lambda d: d.is_ready_for_use()))

    # Tạo các service
    pj_service = AllocationService(pj_repo, HighestPriorityStrategy(lambda d: d.get_default_priority_score()))
    ac_service = AllocationService(ac_repo, FirstAvailableStrategy())
    mic_service = AllocationService(mic_repo, FirstAvailableStrategy())

    # 5. Máy chiếu điểm cao nhất
    title("5. Máy chiếu có điểm cao nhất")
    selected = pj_service.allocate(lambda d: True)
    print("Được chọn:", selected, "| pin =", selected.battery_level)

    # 6. Điều hòa tương thích phòng
    title("6. Điều hòa tương thích phòng A203")
    selected_ac = ac_service.allocate(lambda d: d.is_compatible_with("A203"))
    print("Được chọn:", selected_ac)

    # 7. Micro đầu tiên sẵn sàng
    title("7. Micro đầu tiên sẵn sàng")
    selected_mic = mic_service.allocate()
    print("Được chọn:", selected_mic)

    # 8. Đổi chiến lược lúc chạy
    title("8. Đổi chiến lược lúc chạy")
    mic_service.release("MIC01")
    mic_service.change_strategy(HighestPriorityStrategy(lambda m: m.get_default_priority_score()))
    print("HighestPriority:", mic_service.allocate())      # MIC01 (85)
    mic_service.release("MIC01")
    mic_service.change_strategy(HighestPriorityStrategy(lambda m: m.signal_quality))
    print("Theo tín hiệu  :", mic_service.allocate())       # MIC01 (80)
    mic_service.release("MIC01")
    mic_service.change_strategy(HighestPriorityStrategy(lambda m: m.battery_level * -1))
    print("Pin thấp nhất  :", mic_service.allocate())       # MIC03 (40)

    # 9. Không có ứng viên
    title("9. Không có ứng viên phù hợp")
    try:
        ac_service.allocate(lambda d: d.is_compatible_with("Z999"))
    except NoSuitableItemException as e:
        print("NoSuitableItemException:", e)

    # 10. Thiết bị chuyển sang Borrowed
    title("10. Trạng thái sau cấp phát")
    print("Máy chiếu được chọn:", selected.id, "->", selected.status.value)
    assert selected.status == DeviceStatus.Borrowed
    assert pj_repo.find_by_id(selected.id).status == DeviceStatus.Borrowed
    print("Máy chiếu sẵn sàng còn lại:", pj_repo.find_all(lambda d: d.is_ready_for_use()))
    pj_service.release(selected.id)
    print("Sau khi trả:", selected.id, "->", selected.status.value)

    # 11. Repository generic dùng chung cho nhiều loại
    title("11. Repository generic dùng cho nhiều loại thiết bị")
    print(type(pj_repo).__name__, type(ac_repo).__name__, type(mic_repo).__name__,
          "-> cùng một lớp InMemoryRepository, không sao chép mã")


if __name__ == "__main__":
    main()