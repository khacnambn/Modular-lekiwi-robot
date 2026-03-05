import csv
import time
import math
import sys
sys.path.append("/home/nam/Lekiwi_ws/src/Vive_Tracker")
from track import ViveTrackerModule  # <-- import API thật

# Tracker IDs (theo tên trong track.py)
STATIC_TRACKER_ID = "tracker_2"
MOBILE_TRACKER_ID = "tracker_1"

REFERENCE_FILE = "reference_path.csv"
OUTPUT_FILE = "tracking_log.csv"

def load_reference(file_path):
    ref_points = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Reference path dùng X-Y
            ref_points.append((float(row["x"]), float(row["y"])))
    return ref_points

def find_nearest_point(robot_x, robot_y, ref_points):
    min_dist = float("inf")
    nearest_point = (0, 0)
    for (rx, ry) in ref_points:
        d = math.sqrt((robot_x - rx) ** 2 + (robot_y - ry) ** 2)
        if d < min_dist:
            min_dist = d
            nearest_point = (rx, ry)
    return nearest_point, min_dist

import numpy as np

def hmdmatrix34_to_numpy(mat):
    arr = np.zeros((4, 4))
    for i in range(3):
        for j in range(4):
            arr[i, j] = mat.m[i][j]
    arr[3, 3] = 1.0
    return arr

def get_relative_position(static_tracker, mobile_tracker):
    pose_static_raw = static_tracker.get_pose_matrix()
    pose_dynamic_raw = mobile_tracker.get_pose_matrix()
    if pose_static_raw is None or pose_dynamic_raw is None:
        return None
    pose_static = hmdmatrix34_to_numpy(pose_static_raw)
    pose_dynamic = hmdmatrix34_to_numpy(pose_dynamic_raw)
    if pose_static.shape != (4, 4) or pose_dynamic.shape != (4, 4):
        return None
    rel_pose = np.linalg.inv(pose_static) @ pose_dynamic
    x, y, z = rel_pose[0, 3], rel_pose[1, 3], rel_pose[2, 3]
    return (x, y, z)

def main():
    v_tracker = ViveTrackerModule()
    v_tracker.print_discovered_objects()

    if STATIC_TRACKER_ID not in v_tracker.devices or MOBILE_TRACKER_ID not in v_tracker.devices:
        print(f"❌ Không tìm thấy {STATIC_TRACKER_ID} hoặc {MOBILE_TRACKER_ID}")
        return

    static_tracker = v_tracker.devices[STATIC_TRACKER_ID]
    mobile_tracker = v_tracker.devices[MOBILE_TRACKER_ID]

    ref_points = load_reference(REFERENCE_FILE)
    print(f"Loaded {len(ref_points)} reference points.")

    start_time = time.time()  # Thêm dòng này

    with open(OUTPUT_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "robot_x", "robot_y", "ref_x", "ref_y", "error"])

        try:
            while True:
                current_time = time.time()
                elapsed = current_time - start_time
                if elapsed >= 79:
                    print("\n=== Logger auto stopped after 79 seconds ===")
                    break

                pos = get_relative_position(static_tracker, mobile_tracker)
                if pos is None:
                    print("⚠️ Tracker pose invalid, skipping...")
                    time.sleep(0.1)
                    continue

                robot_x, robot_y, robot_z = pos

                nearest_ref, error = find_nearest_point(robot_x, robot_y, ref_points)

                ts = current_time
                writer.writerow([ts, robot_x, robot_y, nearest_ref[0], nearest_ref[1], error])
                f.flush()

                print(f"[{ts:.2f}] Robot=({robot_x:.2f},{robot_y:.2f}) "
                      f"Ref=({nearest_ref[0]:.2f},{nearest_ref[1]:.2f}) "
                      f"Error={error:.3f} m")

                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n=== Logger stopped ===")

if __name__ == "__main__":
    main()