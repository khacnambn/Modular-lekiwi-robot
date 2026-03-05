import json
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
prop = fm.FontProperties(fname=font_path, size=20)

# Load file log 1
with open("/home/nam/Lekiwi_ws/src/scripts/move_dual/traj_log3.json", "r") as f:
    data1 = json.load(f)

# Load file log 2
with open("/home/nam/Lekiwi_ws/src/scripts/move_docked/traj_log8.json", "r") as f:
    data2 = json.load(f)

# Chuẩn hóa thời gian về 0 cho mỗi file
time1 = [entry["t"] - data1[0]["t"] for entry in data1]
time2 = [entry["t"] - data2[0]["t"] for entry in data2]

# Lấy error
error1 = [entry["error1"] for entry in data1]
error2 = [entry["error"] for entry in data2]

# Vẽ biểu đồ
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(time1, error1, label="Cooperating Robot", color="#B8B8B8")
ax.plot(time2, error2, label="Docked Robot", color="#1A80BB")

# Đường chuẩn y=0
ax.axhline(0, color="black", linestyle="--", linewidth=1)

# Nhãn trục
ax.set_xlabel("Time (s)", fontproperties=prop, fontsize=20)
ax.set_ylabel("Angular Error (°)", fontproperties=prop, fontsize=20)

# Ticks
ax.tick_params(axis="both", labelsize=20)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontproperties(prop)

xmax = max(max(time1), max(time2))
ax.set_xlim(0, xmax * 1.1)

# Chú thích
# Lấy các handle và label từ ax
handles, labels = ax.get_legend_handles_labels()

# Đổi thứ tự: Docked Robot trước, Single Robot sau
ax.legend([handles[1], handles[0]], [labels[1], labels[0]], 
          prop=prop, fontsize=20)
# Lưới
ax.grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.show()
