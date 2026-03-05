import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# Font Times New Roman
font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
prop = fm.FontProperties(fname=font_path, size=20)

systems = ["Cooperating\nrobots", "Docked\nrobot"]
times_sec = [84, 76]   # giá trị giây

# --- CHỈNH ĐỂ ĐẶT CÁC THANH GẦN HƠN ---
spacing = 0.6
y_pos = np.arange(len(systems)) * spacing

fig, ax = plt.subplots(figsize=(6.5, 3.0))

# Vẽ cột ngang
bars = ax.barh(y_pos, times_sec, height=0.35, 
               color=["#B8B8B8", "#1A80BB"], align='center')

# Đặt nhãn trục Y
ax.set_yticks(y_pos)
ax.set_yticklabels(systems, fontproperties=prop, fontsize=16)

# Giới hạn trục Y
y_margin = spacing * 0.6
ax.set_ylim(y_pos.min() - y_margin, y_pos.max() + y_margin)

# Giới hạn trục X
x_max = max(times_sec)
ax.set_xlim(0, x_max * 1.20)

# Ghi trực tiếp số giây
x_offset = x_max * 0.02
for bar, time in zip(bars, times_sec):
    ax.text(time + x_offset, bar.get_y() + bar.get_height()/2,
            f"{time}", va='center', fontsize=16, fontproperties=prop)

# Nhãn trục và font
ax.set_xlabel("Average Transport Time (seconds)", fontsize=16, fontproperties=prop)
plt.xticks(fontproperties=prop, fontsize=16)
plt.yticks(fontproperties=prop, fontsize=16)

plt.tight_layout()
plt.savefig("experiment4_fixed.pdf", format="pdf", bbox_inches="tight", dpi=300)
plt.show()
