import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42

# Font Times New Roman
font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
prop = fm.FontProperties(fname=font_path, size=20)

# Dữ liệu RMS trung bình (10 giá trị mỗi loại)
docked_rms = [0.321, 0.163, 0.284, 0.336, 0.174, 0.155, 0.190, 0.155, 0.325, 0.123]
coop_rms   = [0.712, 0.602, 0.666, 0.681, 1.086, 0.754, 0.689, 0.137, 0.291, 0.450]

# Vẽ boxplot
fig, ax = plt.subplots(figsize=(6,5))
bp = ax.boxplot([docked_rms, coop_rms], patch_artist=True, widths=0.6)

# Tô màu
colors = ["#1A80BB", "#B8B8B8"]  # xanh biển cho Docked, cam cho Cooperating
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)

# Nhãn trục
ax.set_xticks([1, 2])
ax.set_xticklabels(["Docked Robot", "Cooperating Robots"], fontproperties=prop, fontsize=20)
ax.set_ylabel("Mean RMS Acceleration (m/s²)", fontproperties=prop, fontsize=20)

# Cỡ chữ trục Y
plt.yticks(fontproperties=prop, fontsize=20)

# Grid
ax.grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig("boxplot_rms.pdf", format="pdf", bbox_inches="tight", dpi=300)
plt.show()
