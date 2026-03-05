import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42

# Font Times New Roman
font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
prop = fm.FontProperties(fname=font_path, size=20)

# Dữ liệu Std (10 giá trị mỗi loại)
docked_std = [0.677448, 0.551495, 0.376859, 0.408276, 0.613177,
              0.813605, 0.455464, 0.568404, 0.331412, 0.800980]

coop_std   = [1.233827, 1.845251, 0.842365, 0.841582, 0.866070,
              0.487136, 0.868655, 0.761039, 1.135686, 1.153616]

# Vẽ boxplot
fig, ax = plt.subplots(figsize=(6,5))
bp = ax.boxplot([docked_std, coop_std], patch_artist=True, widths=0.6)

# Tô màu
colors = ["#1A80BB", "#B8B8B8"]  # xanh biển cho Docked, cam cho Cooperating
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)

# Nhãn trục
ax.set_xticks([1, 2])
ax.set_xticklabels(["Docked Robot", "Cooperating Robots"], fontproperties=prop, fontsize=20)
ax.set_ylabel("Angle Standard Deviation (°)", fontproperties=prop, fontsize=20)

# Cỡ chữ trục Y
plt.yticks(fontproperties=prop, fontsize=20)

# Grid
ax.grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig("boxplot_std.pdf", format="pdf", bbox_inches="tight", dpi=300)
plt.show()
