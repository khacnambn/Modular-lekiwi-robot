import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# Font Times New Roman
font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
prop = fm.FontProperties(fname=font_path, size=20)

# Dữ liệu
metrics = ["Angular\ndeviation (°)", "Coordinate\ndeviation (m)"]
systems = ["Docked\nsystem", "Single\nrobot"]

docked = [0.3805, 0.079]
single = [0.4773, 0.082]

bar_height = 0.35
y_pos = np.arange(len(metrics))
offset = bar_height / 2

fig, ax = plt.subplots(figsize=(7, 3.5))

# Vẽ với màu mới
bars1 = ax.barh(y_pos + offset, docked, height=bar_height, color="#1A80BB", label="Docked robot")
bars2 = ax.barh(y_pos - offset, single, height=bar_height, color="#EA801C", label="Single robot")

# Nhãn Y
ax.set_yticks(y_pos)
ax.set_yticklabels(metrics, fontproperties=prop, fontsize=18)

# Nhãn số
for bars in [bars1, bars2]:
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.01, 
                bar.get_y() + bar.get_height()/2,
                f"{width:.3f}", 
                va='center', fontsize=18, fontproperties=prop)

# Nhãn X
ax.set_xlabel("Standard Deviation", fontsize=16, fontproperties=prop)
ax.set_xlim(0, max(max(docked), max(single)) * 1.3)

# Legend: đảo thứ tự để Docked xuống dưới
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, prop=prop, fontsize=16, loc="upper right")

plt.xticks(fontproperties=prop, fontsize=16)
plt.yticks(fontproperties=prop, fontsize=16)

plt.tight_layout()
plt.savefig("std_dev_comparison_updated.pdf", format="pdf", bbox_inches="tight", dpi=300)
plt.show()
