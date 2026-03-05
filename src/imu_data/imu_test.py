import socket
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

UDP_IP = "0.0.0.0"   # listen on all interfaces
UDP_PORT = 4210

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Buffers
N = 200
acc_x, acc_y, acc_z = deque([0]*N, maxlen=N), deque([0]*N, maxlen=N), deque([0]*N, maxlen=N)
gyro_x, gyro_y, gyro_z = deque([0]*N, maxlen=N), deque([0]*N, maxlen=N), deque([0]*N, maxlen=N)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,8))

def update(frame):
    try:
        data, _ = sock.recvfrom(1024)
        vals = data.decode().strip().split(",")
        if len(vals) == 6:
            ax, ay, az, gx, gy, gz = map(float, vals)
            acc_x.append(ax); acc_y.append(ay); acc_z.append(az)
            gyro_x.append(gx); gyro_y.append(gy); gyro_z.append(gz)
    except:
        pass

    ax1.clear()
    ax1.plot(acc_x, label="Ax")
    ax1.plot(acc_y, label="Ay")
    ax1.plot(acc_z, label="Az")
    ax1.set_ylim([-15,15])
    ax1.set_title("Accelerometer (m/s^2)")
    ax1.legend(loc="upper right")

    ax2.clear()
    ax2.plot(gyro_x, label="Gx")
    ax2.plot(gyro_y, label="Gy")
    ax2.plot(gyro_z, label="Gz")
    ax2.set_ylim([-2,2])
    ax2.set_title("Gyroscope (rad/s)")
    ax2.legend(loc="upper right")

ani = animation.FuncAnimation(fig, update, interval=50)
plt.tight_layout()
plt.show()
