import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import csv

# Chỉ định font Times New Roman bằng đường dẫn
font_path = "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
prop = fm.FontProperties(fname=font_path, size=20)

LOG_FILES = [
    ("/home/nam/Lekiwi_ws/src/experiment2/docking_L/tracking_log5.csv", "Docked Robot Path", "#1A80BB"),
    ("/home/nam/Lekiwi_ws/src/experiment2/single_L/tracking_log3.csv", "Single Robot Path", "#EA801C"),
]
REF_FILE = "/home/nam/Lekiwi_ws/src/experiment2/reference_path.csv"

# Load reference path
ref_x, ref_y = [], []
with open(REF_FILE) as f:
    reader = csv.DictReader(f)
    for row in reader:
        ref_x.append(abs(float(row["x"])))
        ref_y.append(float(row["y"]))

plt.figure(figsize=(8,8))
# Desired Path: xanh lá đậm
plt.plot(ref_x, ref_y, "-o", color="#2E7D32", label="Desired Path")

plt.xticks(fontproperties=prop, fontsize=20)
plt.yticks(fontproperties=prop, fontsize=20)

for log_file, label, color in LOG_FILES:
    robot_x, robot_y = [], []
    with open(log_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            robot_x.append(abs(float(row["robot_x"])))
            robot_y.append(float(row["robot_y"]))
    plt.plot(robot_x, robot_y, "-", color=color, label=label)

plt.axis("equal")
plt.grid(True)
plt.legend(prop=prop)
plt.xlabel("X (m)", fontproperties=prop)
plt.ylabel("Y (m)", fontproperties=prop)
plt.savefig("experiment2.pdf", format="pdf", bbox_inches="tight", dpi=300)
plt.show()
