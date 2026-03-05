import socket
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import numpy as np
import time
import csv
import math

UDP_IP = "0.0.0.0"
UDP_PORT = 4210

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Buffers
N = 200
gyro_x, gyro_y, gyro_z = deque([0]*N, maxlen=N), deque([0]*N, maxlen=N), deque([0]*N, maxlen=N)

fig, ax = plt.subplots(1, 1, figsize=(10,6))

# CSV log
filename = f"gyro_log_{int(time.time())}.csv"
f = open(filename, "w", newline="")
writer = csv.writer(f)
writer.writerow([
    "timestamp",
    "gx","gy","gz",
    "rms_gyro","ang_speed_now","jerk_gyro","max_ang_speed"
])

dt = 0.05  # 20Hz

# === Helper functions ===
def compute_rms(data):
    return np.sqrt(np.mean(np.array(data)**2))

def compute_jerk(data, dt):
    arr = np.array(data)
    diff = np.diff(arr) / dt
    return np.mean(np.abs(diff)) if len(diff) > 0 else 0

# === Tạo sẵn line objects ===
xdata = np.arange(N)
line_gx, = ax.plot(xdata, gyro_x, label="Gx")
line_gy, = ax.plot(xdata, gyro_y, label="Gy")
line_gz, = ax.plot(xdata, gyro_z, label="Gz")

ax.set_ylim([-500, 500])   # chỉnh theo dải gyro
ax.set_xlim(0, N)
ax.legend(loc="upper right")

# Textbox hiển thị thông số
text_box = ax.text(
    0.02, 0.95, "", transform=ax.transAxes,
    fontsize=10, va="top", ha="left",
    bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.7)
)

def init():
    line_gx.set_data([], [])
    line_gy.set_data([], [])
    line_gz.set_data([], [])
    text_box.set_text("")
    return line_gx, line_gy, line_gz, text_box

def update(frame):
    try:
        data, _ = sock.recvfrom(1024, socket.MSG_DONTWAIT)
        vals = data.decode().strip().split(",")
        if len(vals) == 3:  # chỉ nhận gyro gx, gy, gz
            gx, gy, gz = map(float, vals)
            gyro_x.append(gx); gyro_y.append(gy); gyro_z.append(gz)
    except BlockingIOError:
        pass

    # --- Metrics ---
    rms_gyro = compute_rms(gyro_x)
    ang_speed_now = np.sqrt(gyro_x[-1]**2 + gyro_y[-1]**2 + gyro_z[-1]**2)
    jerk_gyro = compute_jerk(gyro_x, dt)
    max_ang_speed = max([np.sqrt(x**2+y**2+z**2) for x,y,z in zip(gyro_x,gyro_y,gyro_z)])

    # --- Log CSV ---
    writer.writerow([
        time.time(),
        gyro_x[-1], gyro_y[-1], gyro_z[-1],
        rms_gyro, ang_speed_now, jerk_gyro, max_ang_speed
    ])

    # --- Update lines ---
    xdata = np.arange(len(gyro_x))
    line_gx.set_data(xdata, gyro_x)
    line_gy.set_data(xdata, gyro_y)
    line_gz.set_data(xdata, gyro_z)

    # --- Update textbox ---
    text_box.set_text(
        f"RMS={rms_gyro:.2f}\n"
        f"|ω|={ang_speed_now:.2f}\n"
        f"Jerk={jerk_gyro:.2f}\n"
        f"Max|ω|={max_ang_speed:.2f}"
    )

    return line_gx, line_gy, line_gz, text_box

ani = animation.FuncAnimation(fig, update, init_func=init, interval=50, blit=True)
plt.tight_layout()
plt.show()

f.close()
