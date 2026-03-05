import sys
sys.path.append("/home/nam/Lekiwi_ws/src/Vive_Tracker")
import time
import csv
import numpy as np
from scipy.spatial.transform import Rotation as R
from track import ViveTrackerModule

# ==============================
# Khởi tạo Vive Tracker
# ==============================
v_tracker = ViveTrackerModule()
v_tracker.print_discovered_objects()

if "tracker_1" not in v_tracker.devices or "tracker_2" not in v_tracker.devices:
    print("❌ Cần có 2 tracker: tracker_static (gốc) và tracker_dynamic (di động)")
    sys.exit(1)

tracker_static = v_tracker.devices["tracker_2"]
tracker_dynamic = v_tracker.devices["tracker_1"]

def hmdmatrix34_to_numpy(mat):
    """Chuyển đổi HmdMatrix34_t sang numpy array 4x4"""
    arr = np.zeros((4, 4))
    # HmdMatrix34_t là một object có thuộc tính m chứa 3x4 phần tử
    for i in range(3):
        for j in range(4):
            arr[i, j] = mat.m[i][j]
    arr[3, 3] = 1.0
    return arr

# ==============================
# Hàm tính vị trí tương đối
# ==============================
def get_relative_position():
    """Trả về vị trí động so với tĩnh (x,y,z)"""
    pose_static_raw = tracker_static.get_pose_matrix()  # HmdMatrix34_t
    pose_dynamic_raw = tracker_dynamic.get_pose_matrix()  # HmdMatrix34_t

    # Kiểm tra dữ liệu trả về
    if pose_static_raw is None or pose_dynamic_raw is None:
        return None

    pose_static = hmdmatrix34_to_numpy(pose_static_raw)
    pose_dynamic = hmdmatrix34_to_numpy(pose_dynamic_raw)

    # Kiểm tra lại kích thước
    if pose_static.shape != (4, 4) or pose_dynamic.shape != (4, 4):
        return None

    # Tọa độ động trong hệ gốc tĩnh
    rel_pose = np.linalg.inv(pose_static) @ pose_dynamic
    x, y, z = rel_pose[0, 3], rel_pose[1, 3], rel_pose[2, 3]
    return (x, y, z)

# ==============================
# Ghi dữ liệu
# ==============================
ref_points = []
print("✅ Sẵn sàng ghi quỹ đạo. Nhấn Enter để lưu 1 điểm, gõ 'q' rồi Enter để thoát.")

while True:
    cmd = input(">> ")
    if cmd.strip().lower() == "q":
        break

    pos = get_relative_position()
    if pos is not None:
        ref_points.append(pos)
        print(f"📍 Ghi điểm: {pos}")
    else:
        print("⚠️ Không lấy được dữ liệu tracker.")

# ==============================
# Lưu ra CSV
# ==============================
with open("reference_path.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["x", "y", "z"])
    writer.writeheader()
    for (x, y, z) in ref_points:
        writer.writerow({"x": x, "y": y, "z": z})

print("💾 Đã lưu reference_path.csv thành công.")
