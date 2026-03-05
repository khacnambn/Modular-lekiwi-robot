import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42

# Font Times New Roman
font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
prop = fm.FontProperties(fname=font_path, size=20)

# --- Data ---
# RMS
docked_rms = [0.321, 0.163, 0.284, 0.336, 0.174, 0.155, 0.190, 0.155, 0.325, 0.123]
coop_rms   = [0.712, 0.602, 0.666, 0.681, 1.086, 0.754, 0.689, 0.137, 0.291, 0.450]

# Std (σθ)
docked_std = [0.677448, 0.551495, 0.376859, 0.408276, 0.613177,
              0.813605, 0.455464, 0.568404, 0.331412, 0.800980]

coop_std   = [1.233827, 1.845251, 0.842365, 0.841582, 0.866070,
              0.487136, 0.868655, 0.761039, 1.135686, 1.153616]

# --- Vẽ ---
fig, ax1 = plt.subplots(figsize=(9,6))
ax2 = ax1.twinx()  # trục Y thứ 2

# Vị trí cho các box
positions_rms = [1, 4]   # Docked, Coop cho RMS
positions_std = [2, 5]   # Docked, Coop cho σθ

# Vẽ RMS trên ax1
bp1 = ax1.boxplot([docked_rms, coop_rms], positions=positions_rms,
                  patch_artist=True, widths=0.6)
for patch, color in zip(bp1['boxes'], ["#1A80BB", "#B8B8B8"]):
    patch.set_facecolor(color)

# Vẽ σθ trên ax2
bp2 = ax2.boxplot([docked_std, coop_std], positions=positions_std,
                  patch_artist=True, widths=0.6)
for patch, color in zip(bp2['boxes'], ["#1A80BB", "#B8B8B8"]):
    patch.set_facecolor(color)

# Trục X: 2 nhóm
ax1.set_xticks([1.5, 4.5])
ax1.set_xticklabels(
    ["Docked Robot", "Cooperating Robots"],
    fontproperties=prop, fontsize=18
)

# Dịch nhãn X xuống thấp hơn (sát boxplot)
ax1.tick_params(axis="x", pad=12)

# Trục Y
ax1.set_ylabel("Mean RMS Acceleration (m/s²)", fontproperties=prop, fontsize=18, color="black")
ax2.set_ylabel("Angle Standard Deviation (°)", fontproperties=prop, fontsize=18, color="black")

ax1.tick_params(axis='y', labelsize=16)
ax2.tick_params(axis='y', labelsize=16)
plt.xticks(fontproperties=prop, fontsize=16)

# Grid theo trục chính (RMS)
ax1.grid(True, linestyle="--", alpha=0.6)

# --- Thêm nhãn trên mỗi box dựa vào whisker thay vì max ---
def box_top(bp, idx):
    """Lấy y trên cùng của whisker (cap) cho box idx"""
    cap = bp['caps'][2*idx+1]  # cap trên
    return cap.get_ydata()[0]

# RMS nhãn
ax1.text(1, box_top(bp1,0)+0.02, "RMS", ha="center", va="bottom", fontproperties=prop, fontsize=14)
ax1.text(4, box_top(bp1,1)+0.02, "RMS", ha="center", va="bottom", fontproperties=prop, fontsize=14)

# σθ nhãn
ax2.text(2, box_top(bp2,0)+0.02, r"$\sigma_\theta$", ha="center", va="bottom", fontproperties=prop, fontsize=14)
ax2.text(5, box_top(bp2,1)+0.02, r"$\sigma_\theta$", ha="center", va="bottom", fontproperties=prop, fontsize=14)

plt.tight_layout()
plt.savefig("boxplot_dualY_labels_fixed.pdf", format="pdf", bbox_inches="tight", dpi=300)
plt.show()
