import pandas as pd
import numpy as np
import json
import glob

# Đường dẫn đến các file log (thay đổi nếu cần)
log_files = sorted(glob.glob("/home/nam/Lekiwi_ws/src/scripts/log_single_L/traj_log*.json"))

results = []

for i, file in enumerate(log_files, start=1):
    with open(file, "r") as f:
        data = json.load(f)

    # Lấy dữ liệu error1, error2
    error1 = [entry["error"] for entry in data if "error" in entry]
    # error2 = [entry["error2"] for entry in data if "error2" in entry]

    # Tính Mean & Std
    mean1, std1 = np.mean(error1), np.std(error1)
    # mean2, std2 = np.mean(error2), np.std(error2)

    results.append({
        "Run": f"Run {i}",
        "Robot_Mean": mean1,
        "Robot_Std": std1,
        # "Robot2_Mean": mean2,
        # "Robot2_Std": std2
    })

# Chuyển sang DataFrame
df = pd.DataFrame(results)
print(df)

# Nếu muốn lưu ra CSV:
# df.to_csv("tracking_error_stats.csv", index=False)
