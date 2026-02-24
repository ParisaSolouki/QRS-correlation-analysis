# src/qrs_correlation.py

import glob
import warnings

import numpy as np
import wfdb
from matplotlib import pyplot as plt
from scipy import io, signal

warnings.filterwarnings("ignore", category=DeprecationWarning)

# -----------------------------
# Config (you can edit these)
# -----------------------------
DATA_GLOB = "/Users/parisa/Desktop/mit-bih-arrhythmia-database/*.dat"
TEMPLATE_MAT_NAME = "Template.mat"

FS = 360  # Sampling frequency (Hz)
FL = 0.5  # High-pass cutoff (Hz)
FH = 20  # Low-pass cutoff (Hz)

# QRS window around R-peak
LEFT = 80
RIGHT = 120

# Beat type table
TABLE = {
    "N": ["N"],  # Normal
    "S": ["A", "a", "S", "J"],  # Supraventricular ectopic
    "F": ["F"],  # Fusion
    "V": ["V"],  # Ventricular ectopic
    "U": ["Q", "U", "/", "p"],  # Unknown
}


def main():
    # -----------------------------
    # Load ECG files
    # -----------------------------
    listNames = glob.glob(DATA_GLOB)

    if not listNames:
        print("No ECG files found in the specified directory.")
        print("Check DATA_GLOB path in src/qrs_correlation.py")
        return
    else:
        print(f"Processing {len(listNames)} files.")

    # -----------------------------
    # Filters
    # -----------------------------
    b1, a1 = signal.butter(N=3, Wn=FL / (FS / 2), btype="high")
    b2, a2 = signal.butter(N=3, Wn=FH / (FS / 2), btype="low")

    # -----------------------------
    # Segmentation
    # -----------------------------
    data0, data1, data2, data3, data4 = [], [], [], [], []

    for name in listNames:
        recordName = name.partition(".")[0]
        print(f"Processing record: {recordName}")

        sig, fields = wfdb.rdsamp(record_name=recordName)

        sig = signal.filtfilt(b1, a1, sig[:, 0], padtype="even", axis=0)
        sig = signal.filtfilt(b2, a2, sig, padtype="even")

        annotations = wfdb.rdann(recordName, "atr")
        pos = annotations.sample
        labels = annotations.symbol

        # segment beats
        for i in range(1, len(pos) - 1):
            start = pos[i] - LEFT
            end = pos[i] + RIGHT

            # safety check for boundaries
            if start < 0 or end > len(sig):
                continue

            qrs = sig[start:end]
            beat_type = labels[i]

            if beat_type in TABLE["N"]:
                data0.append(qrs)
            elif beat_type in TABLE["S"]:
                data1.append(qrs)
            elif beat_type in TABLE["F"]:
                data2.append(qrs)
            elif beat_type in TABLE["V"]:
                data3.append(qrs)
            elif beat_type in TABLE["U"]:
                data4.append(qrs)

    data0 = np.array(data0, dtype=np.float64)
    data1 = np.array(data1, dtype=np.float64)
    data2 = np.array(data2, dtype=np.float64)
    data3 = np.array(data3, dtype=np.float64)
    data4 = np.array(data4, dtype=np.float64)

    print("-" * 40)
    print("Segmentation is done!")
    print("Shapes:")
    print(
        "N:",
        data0.shape,
        "S:",
        data1.shape,
        "F:",
        data2.shape,
        "V:",
        data3.shape,
        "U:",
        data4.shape,
    )

    # If no normal beats, we can't build a template
    if data0.size == 0:
        print("No N beats found -> cannot build template.")
        return

    # -----------------------------
    # Plot examples
    # -----------------------------
    plt.figure(figsize=(10, 8))

    plt.subplot(3, 2, 1)
    if len(data0) > 0:
        plt.plot(data0[:100, :].T)
    plt.title("N")

    plt.subplot(3, 2, 2)
    if len(data1) > 0:
        plt.plot(data1[:100, :].T)
    plt.title("S")

    plt.subplot(3, 2, 3)
    if len(data2) > 0:
        plt.plot(data2[:100, :].T)
    plt.title("F")

    plt.subplot(3, 2, 4)
    if len(data3) > 0:
        plt.plot(data3[:100, :].T)
    plt.title("V")

    plt.subplot(3, 2, 5)
    if len(data4) > 0:
        plt.plot(data4[:100, :].T)
    plt.title("U")

    plt.tight_layout()
    plt.show()

    # -----------------------------
    # Build template from N beats
    # -----------------------------
    template1 = np.mean(data0, axis=0)

    plt.figure(figsize=(6, 4))
    plt.plot(template1)
    plt.title("Template for N beats")
    plt.xlabel("Sample Number")
    plt.ylabel("Amplitude")
    plt.show()

    io.savemat(file_name=TEMPLATE_MAT_NAME, mdict={"N": template1})
    print(f"Template saved to {TEMPLATE_MAT_NAME}")

    # -----------------------------
    # Correlation
    # -----------------------------
    # pick sample beats (check we have enough)
    if len(data0) < 2:
        print("Not enough N beats for qrs0 = data0[1].")
        return

    qrs0 = data0[1, :]

    if len(data1) >= 2:
        qrs1 = data1[1, :]
    else:
        qrs1 = None

    # Plot
    plt.figure(figsize=(10, 6))

    plt.subplot(2, 2, 1)
    plt.plot(qrs0)
    plt.title("QRS0 (N)")

    if qrs1 is not None:
        plt.subplot(2, 2, 2)
        plt.plot(qrs1)
        plt.title("QRS1 (S)")

    plt.subplot(2, 2, 3)
    plt.plot(template1)
    plt.title("Template (mean of N)")

    plt.tight_layout()
    plt.show()

    crr0 = np.corrcoef(qrs0, template1)[0, 1]
    print(f"Correlation(QRS0, Template) = {crr0:.4f}")

    if qrs1 is not None:
        crr1 = np.corrcoef(qrs1, template1)[0, 1]
        print(f"Correlation(QRS1, Template) = {crr1:.4f}")

    # correlation for first 5 N beats (if exist)
    k = min(5, len(data0))
    crr = np.corrcoef(template1, data0[:k, :])
    print(f"Correlation(Template, first {k} N beats) = {crr[0, 1:]}")


if __name__ == "__main__":
    main()
