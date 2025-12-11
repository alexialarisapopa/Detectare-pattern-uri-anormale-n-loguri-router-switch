import random
import pandas as pd
import os
from datetime import datetime, timedelta
from tqdm import tqdm   # bară de progres

normal_messages = [
    "LINK-UP: Interface GigabitEthernet0/1 is up",
    "LINK-DOWN: Interface GigabitEthernet0/2 is down",
    "OSPF: Neighbor adjacency established",
    "DHCP: New lease granted",
    "STP: Topology change detected",
    "PORT-SECURITY: 1 MAC address learned",
    "SYSLOG: System running normally",
    "NTP: Time synchronized",
    "BGP: New peer session established",
]

anomaly_messages = [
    "SECURITY ALERT: Possible intrusion detected",
    "AUTH-FAIL: Multiple invalid SSH attempts",
    "CPU HIGH: 98% utilization for 300 seconds",
    "DDOS DETECTED: Abnormal traffic spike",
    "PORT-SCAN: Multiple SYN packets detected",
    "CONFIG ERROR: Unexpected configuration rollback",
    "MALWARE: Suspicious binary executed",
    "DATA-LEAK: Unexpected outbound transfer"
]

devices = ["R1", "R2", "R3", "SW1", "SW2", "SW3", "FW1", "FW2"]


# --------------------
# Timestamp realistic
# --------------------
def random_timestamp():
    base = datetime.now()
    offset = timedelta(seconds=random.randint(-300000, 0))
    return (base + offset).strftime("%Y-%m-%d %H:%M:%S")


# --------------------
# Generator scalabil (versiune redusă)
# --------------------
def generate_logs(n=50000, anomaly_ratio=0.18, batch_size=10000):
    base_path = r"C:\Users\A\OneDrive\Desktop\facultate\Proiect_RN\data\raw"
    os.makedirs(base_path, exist_ok=True)

    output_file = os.path.join(base_path, "generated_logs.csv")

    # Dacă fișierul există, îl ștergem pentru a evita dublarea datelor
    if os.path.exists(output_file):
        os.remove(output_file)

    header_written = False

    print(f"[INFO] Generating {n} logs in batches of {batch_size}…\n")

    for _ in tqdm(range(0, n, batch_size)):
        batch = []

        # batchul poate fi mai mic în ultima iterație
        current_batch_size = min(batch_size, n)

        for _ in range(current_batch_size):
            msg = random.choice(anomaly_messages) if random.random() < anomaly_ratio else random.choice(normal_messages)
            label = 1 if msg in anomaly_messages else 0

            batch.append({
                "timestamp": random_timestamp(),
                "device": random.choice(devices),
                "severity": random.randint(0, 7),
                "message": msg,
                "label": label
            })

        df = pd.DataFrame(batch)

        df.to_csv(output_file, mode="a", header=not header_written, index=False)
        header_written = True

        n -= batch_size  # scade numărul de loguri rămase

    print(f"\n[INFO] Done! → {output_file}")


# --------------------
# RUN
# --------------------
if __name__ == "__main__":
    generate_logs(n=50000, anomaly_ratio=0.18)
