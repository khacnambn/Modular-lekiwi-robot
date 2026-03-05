import csv
import numpy as np

LOG_FILE = "/home/nam/Lekiwi_ws/src/experiment2/docking_L/tracking_log8.csv"

def analyze_log(file_path):
    times, errors = [], []

    with open(file_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            times.append(float(row["timestamp"]))
            errors.append(float(row["error"]))

    errors = np.array(errors)
    times = np.array(times)

    if len(errors) == 0:
        print("❌ Không có dữ liệu trong log file")
        return

    # Tính benchmark
    mean_err = np.mean(errors)
    rms_err = np.sqrt(np.mean(errors**2))
    max_err = np.max(errors)
    std_err = np.std(errors)
    total_time = times[-1] - times[0]

    print("=== Benchmark Result ===")
    print(f"📊 Mean Error = {mean_err:.3f} m")
    print(f"📊 RMS Error  = {rms_err:.3f} m")
    print(f"📊 Max Error  = {max_err:.3f} m")
    print(f"📊 Std Error  = {std_err:.3f} m")
    print(f"⌛ Total Time  = {total_time:.2f} s")

if __name__ == "__main__":
    analyze_log(LOG_FILE)
