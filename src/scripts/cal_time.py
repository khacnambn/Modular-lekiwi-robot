import json
import csv

# Danh sách các file cần tính thời gian
json_files = [
    "/home/nam/Lekiwi_ws/src/scripts/move_docked/traj_log4.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_docked/traj_log5.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_docked/traj_log6.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_docked/traj_log7.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_docked/traj_log10.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_docked/traj_log11.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_docked/traj_log12.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_docked/traj_log13.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_docked/traj_log14.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_docked/traj_log15.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_dual/traj_log1.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_dual/traj_log2.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_dual/traj_log3.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_dual/traj_log4.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_dual/traj_log5.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_dual/traj_log6.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_dual/traj_log7.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_dual/traj_log8.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_dual/traj_log9.json",
    "/home/nam/Lekiwi_ws/src/scripts/move_dual/traj_log10.json"
]
csv_files = [
    "imu_log_1757391126.csv",
    "imu_log_1757327784.csv"
]

# Hàm tính thời gian chạy từ file JSON
def get_json_duration(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        if not data:  # Kiểm tra nếu file rỗng
            return None
        t_start = data[0]["t"]
        t_end = data[-1]["t"]
        return t_end - t_start
    except Exception as e:
        print(f"Lỗi khi đọc {filename}: {e}")
        return None

# Hàm tính thời gian chạy từ file CSV
def get_csv_duration(filename):
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            timestamps = [float(row['timestamp']) for row in reader]
        if not timestamps:  # Kiểm tra nếu file rỗng
            return None
        t_start = timestamps[0]
        t_end = timestamps[-1]
        return t_end - t_start
    except Exception as e:
        print(f"Lỗi khi đọc {filename}: {e}")
        return None

# Tính và in thời gian chạy cho các file JSON
print("Thời gian chạy của các file JSON:")
for file in json_files:
    duration = get_json_duration(file)
    if duration is not None:
        print(f"{file}: {duration:.6f} giây")
    else:
        print(f"{file}: Không thể tính thời gian (file rỗng hoặc lỗi)")

# Tính và in thời gian chạy cho các file CSV
print("\nThời gian chạy của các file CSV:")
for file in csv_files:
    duration = get_csv_duration(file)
    if duration is not None:
        print(f"{file}: {duration:.6f} giây")
    else:
        print(f"{file}: Không thể tính thời gian (file rỗng hoặc lỗi)")