import socket
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import numpy as np
import math
import csv
import time

UDP_IP = "0.0.0.0"   # listen on all interfaces
UDP_PORT = 4210

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Buffers
N = 400  
acc_x, acc_y, acc_z = deque([0]*N, maxlen=N), deque([0]*N, maxlen=N), deque([0]*N, maxlen=N)

fig, ax1 = plt.subplots(1, 1, figsize=(10,6))

# === Helper functions ===
def compute_rms(data):
    return np.sqrt(np.mean(np.array(data)**2))

def compute_tilt(ax, ay, az):
    return np.degrees(np.arctan2(np.sqrt(ax**2 + ay**2), az))

def compute_jerk(acc_series, dt=0.05):  # dt=50ms ~ 20Hz
    acc = np.array(acc_series)
    jerk = np.diff(acc) / dt
    return np.mean(np.abs(jerk)) if len(jerk) > 0 else 0

tilt_threshold = 10 
tilt_cross_count = 0
tilt_prev_above = False

def count_tilt_cross(tilt_angle):
    global tilt_cross_count, tilt_prev_above
    above = tilt_angle > tilt_threshold
    if above and not tilt_prev_above:
        tilt_cross_count += 1
    tilt_prev_above = above
    return tilt_cross_count

def compute_frequency(acc_series, dt=0.05):
    acc = np.array(acc_series)
    acc = acc - np.mean(acc) 
    fft_vals = np.fft.rfft(acc)
    freqs = np.fft.rfftfreq(len(acc), d=dt)
    peak_idx = np.argmax(np.abs(fft_vals))
    return freqs[peak_idx]

# === CSV logging ===
log_filename = f"imu_log_{int(time.time())}.csv"
csv_file = open(log_filename, "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["timestamp","ax","ay","az","rms","tilt_now","jerk","tilt_crosses","freq"])

# === Tạo sẵn line object ===
xdata = np.arange(N)
line_x, = ax1.plot(xdata, acc_x, label="Ax")
line_y, = ax1.plot(xdata, acc_y, label="Ay")
line_z, = ax1.plot(xdata, acc_z, label="Az")

ax1.set_ylim([-15, 15])
ax1.set_xlim(0, N)
ax1.legend(loc="upper right")

# === Text box để hiển thị thông số realtime ===
info_text = ax1.text(
    0.02, 0.95, "", transform=ax1.transAxes, fontsize=10,
    verticalalignment="top", bbox=dict(facecolor="white", alpha=0.7, edgecolor="gray")
)

def init():
    line_x.set_data([], [])
    line_y.set_data([], [])
    line_z.set_data([], [])
    info_text.set_text("")
    return line_x, line_y, line_z, info_text

def update(frame):
    global acc_x, acc_y, acc_z

    # đọc socket non-blocking
    try:
        data, _ = sock.recvfrom(1024, socket.MSG_DONTWAIT)
        vals = data.decode().strip().split(",")
        if len(vals) >= 3: 
            ax, ay, az = map(float, vals[:3])
            # Đảo dấu trục Y
            az = -az
            ax = -ax
            acc_x.append(ax)
            acc_y.append(ay)
            acc_z.append(az)
    except BlockingIOError:
        pass

    # === Benchmark ===
    rms_val = compute_rms(acc_x)
    tilt_now = compute_tilt(acc_x[-1], acc_y[-1], acc_z[-1])
    jerk_val = compute_jerk(acc_x)
    tilt_crosses = count_tilt_cross(tilt_now)
    freq_val = compute_frequency(acc_x)

    # === Write log CSV ===
    csv_writer.writerow([time.time(), acc_x[-1], acc_y[-1], acc_z[-1],
                         rms_val, tilt_now, jerk_val, tilt_crosses, freq_val])

    # === Update line data (không clear) ===
    xdata = np.arange(len(acc_x))
    line_x.set_data(xdata, acc_x)
    line_y.set_data(xdata, acc_y)
    line_z.set_data(xdata, acc_z)

    # === Update text box ===
    info_text.set_text(
        f"RMS={rms_val:.2f}\n"
        f"Tilt={tilt_now:.1f}°\n"
        f"Jerk={jerk_val:.2f}\n"
        f"Crosses={tilt_crosses}\n"
        f"Freq={freq_val:.2f} Hz"
    )

    return line_x, line_y, line_z, info_text

start_time = time.time()
timeout = 79  # seconds

def update_with_timeout(frame):
    if time.time() - start_time > timeout:
        plt.close(fig)
        return line_x, line_y, line_z, info_text
    return update(frame)

try:
    ani = animation.FuncAnimation(fig, update_with_timeout, init_func=init, interval=20, blit=True)
    plt.tight_layout()
    plt.show()
finally:
    csv_file.close()
    print(f"\nLogging finished. Data saved to file: {log_filename}")
