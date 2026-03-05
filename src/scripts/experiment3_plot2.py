import csv
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# Đường dẫn font
font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
prop = fm.FontProperties(fname=font_path, size=20)

# Hàm đọc cột timestamp và ax từ file CSV
def read_csv_data(filename):
    timestamps = []
    ax_values = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamps.append(float(row['timestamp']))
            ax_values.append(float(row['rms']))
    return timestamps, ax_values

# Đọc file CSV 1 (imu_log_1757391126.csv)
timestamps1, ax1 = read_csv_data("/home/nam/Lekiwi_ws/src/scripts/log2/imu_log_1757328375.csv")

# Đọc file CSV 2 (imu_log_1757327784.csv)
timestamps2, ax2 = read_csv_data("/home/nam/Lekiwi_ws/src/scripts/log1/imu_log_1757394179.csv")

# Chuẩn hóa thời gian về 0
time1 = [t - timestamps1[0] for t in timestamps1]
time2 = [t - timestamps2[0] for t in timestamps2]

# Vẽ biểu đồ
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(time1, ax1, label="Cooperating Robots", color="#B8B8B8")
ax.plot(time2, ax2, label="Docked Robot", color="#1A80BB")

# Đường chuẩn y=0
ax.axhline(0, color="black", linestyle="--", linewidth=1)

# Nhãn trục
ax.set_xlabel("Time (s)", fontproperties=prop, fontsize=20)
ax.set_ylabel("RMS Acceleration (m/s²)", fontproperties=prop, fontsize=20)

# Ticks
ax.tick_params(axis="both", labelsize=20)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontproperties(prop)

# Đặt giới hạn trục x
xmax = max(max(time1), max(time2))
ax.set_xlim(0, xmax * 1.1)

# Chú thích
handles, labels = ax.get_legend_handles_labels()
# Đổi thứ tự: IMU Log 2 trước, IMU Log 1 sau
ax.legend([handles[1], handles[0]], [labels[1], labels[0]], 
          prop=prop, fontsize=20)

# Lưới
ax.grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.show()