import os
import subprocess
from datetime import datetime

def capture_snapshot(name, command):
    print(f"Capturing {name}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{name}_{timestamp}.txt"
        
        with open(filename, "w") as f:
            f.write(f"--- SNAPSHOT: {name} ---\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Command: {command}\n")
            f.write("-" * 30 + "\n")
            f.write(result.stdout)
            if result.stderr:
                f.write("\nERRORS:\n")
                f.write(result.stderr)
        
        print(f"Saved to {filename}")
    except Exception as e:
        print(f"Failed to capture {name}: {e}")

def main():
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
        
    # Capture various states
    capture_snapshot("pods_status", "kubectl get pods")
    capture_snapshot("services_status", "kubectl get svc")
    capture_snapshot("hpa_status", "kubectl get hpa")
    capture_snapshot("cluster_info", "kubectl cluster-info")

if __name__ == "__main__":
    main()
