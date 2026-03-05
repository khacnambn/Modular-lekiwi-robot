import matplotlib.pyplot as plt
import csv

# ==============================
# Load dữ liệu từ CSV
# ==============================
ref_points = []
with open("reference_path.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Lấy trục X và Z thay vì X và Y
        ref_points.append((float(row["x"]), float(row["y"])))

if not ref_points:
    print("❌ Không có dữ liệu trong reference_path.csv")
    exit(1)

# ==============================
# Chuẩn bị dữ liệu
# ==============================
ref_x, ref_y = zip(*ref_points)
print("📍 Các điểm reference (X,Z):")
for i, (x, y) in enumerate(ref_points):
    print(f"  {i}: (X={x:.3f}, Z={y:.3f})")

# ==============================
# Vẽ
# ==============================
plt.figure(figsize=(6,6))
plt.plot(ref_x, ref_y, "b-o", label="Reference Path (X-Z)")   # đường xanh
plt.scatter(ref_x[0], ref_y[0], c="g", s=100, label="Start") # điểm đầu
plt.scatter(ref_x[-1], ref_y[-1], c="r", s=100, label="End") # điểm cuối
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.title("Reference Path Visualization (mặt phẳng XZ)")
plt.xlabel("X (m)")
plt.ylabel("Z (m)")
plt.show()
