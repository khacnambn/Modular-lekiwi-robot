import pandas as pd
import numpy as np
import sys

def analyze_csv(filename):
    df = pd.read_csv(filename)

    rms_mean = df["rms"].mean()

    # Max tilt
    max_tilt = df["tilt_now"].max()

    jerk_mean = df["jerk"].mean()

    # tilt_crosses
    tilt_crosses = df["tilt_crosses"].iloc[-1]

    # median frequency
    freq_median = df["freq"].median()

    print("=== Stability Benchmark Summary ===")
    print(f"RMS (mean): {rms_mean:.3f} m/s^2")
    print(f"Max Tilt: {max_tilt:.2f} °")
    print(f"Jerk (mean): {jerk_mean:.3f} m/s^3")
    print(f"Tilt Crosses: {tilt_crosses} times")
    print(f"Dominant Frequency (median): {freq_median:.2f} Hz")

    return {
        "RMS_mean": rms_mean,
        "Max_Tilt": max_tilt,
        "Jerk_mean": jerk_mean,
        "Tilt_Crosses": tilt_crosses,
        "Dominant_Freq": freq_median
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze.py imu_log_xxx.csv")
        sys.exit(1)

    filename = sys.argv[1]
    analyze_csv(filename)
