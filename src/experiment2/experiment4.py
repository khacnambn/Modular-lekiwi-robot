import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# Font Times New Roman
font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
prop = fm.FontProperties(fname=font_path, size=18)

systems = ["Cooperating robots", "Docked robot"]
times_sec = [176, 117]   # giá trị giây

# --- Vị trí ---
spacing = 0.075   # giảm khoảng cách giữa 2 cột
y_pos = np.arange(len(systems)) * spacing

fig, ax = plt.subplots(figsize=(6, 2.5))

# Vẽ cột ngang
bars = ax.barh(y_pos, times_sec, height=0.05, 
               color=["#B8B8B8", "#1A80BB"], align='center')

# Bỏ nhãn Y (sẽ tự vẽ text trong bar)
ax.set_yticks([])

# Giới hạn trục X
x_max = max(times_sec)
ax.set_xlim(0, x_max * 1.25)  # kéo dài thêm để có chỗ viết chữ

# Viết chữ vào trong bar
for bar, time, label in zip(bars, times_sec, systems):
    ax.text(bar.get_width()/2, bar.get_y() + bar.get_height()/2,
            f"{label} ({time})",
            ha='center', va='center', color="white",
            fontsize=16, fontproperties=prop, weight='bold')

# Nhãn trục X
ax.set_xlabel("Average Completion Time (seconds)", fontsize=16, fontproperties=prop)
plt.xticks(fontproperties=prop, fontsize=14)

plt.tight_layout()
plt.savefig("experiment4_inside_labels.pdf", format="pdf", bbox_inches="tight", dpi=300)
plt.show()
