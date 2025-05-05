import subprocess
import os
import sys

PIPELINES = [
    "./pipelines/ingest_raw_events.py",
    "./pipelines/preprocess_clean_events.py",
    "./pipelines/detect_entry_exit_events.py",
    "./pipelines/influx_write_events.py",
]

def run_all_pipelines():
    """
    Launches all pipeline components concurrently using subprocess.
    """
    processes = []
    for script in PIPELINES:
        print(f"[STARTING] - {script}...")
        p = subprocess.Popen(
            [sys.executable, script],
            env={**os.environ, "PYTHONPATH": os.getcwd()}
        )
        processes.append(p)

    for p in processes:
        p.wait()

if __name__ == "__main__":
    print("[LAUNCHING] - all RFID pipelines...")
    run_all_pipelines()
