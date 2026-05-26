import time
import random
import os
import argparse
import logging
from logging.handlers import RotatingFileHandler
from kubernetes import client, config

# Global outage simulation toggle (set via environment variable or CLI flag)
GLOBAL_OUTAGE_MODE = None

def chaos_monkey(global_outage_mode=False, log_file=None, log_max_bytes=5*1024*1024, log_backup_count=3):
    # Set up logging
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(RotatingFileHandler(log_file, maxBytes=log_max_bytes, backupCount=log_backup_count))
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=handlers
    )
    try:
        # Load kubeconfig
        config.load_kube_config()
        v1 = client.CoreV1Api()
        
        logging.info("--- Netflix Chaos Monkey Started ---")
        if global_outage_mode:
            logging.warning("!!! GLOBAL OUTAGE MODE ENABLED: All Netflix service pods will be terminated at once !!!")
        
        while True:
            # Get all pods in the default namespace
            pods = v1.list_namespaced_pod(namespace="default")
            
            # Filter for our netflix-lab pods
            netflix_pods = [pod for pod in pods.items if "service" in pod.metadata.name]
            
            if not netflix_pods:
                logging.info("No Netflix service pods found. Waiting...")
                time.sleep(10)
                continue
            
            if global_outage_mode:
                logging.critical(f"🔥 GLOBAL OUTAGE: Terminating ALL Netflix service pods!")
                for pod in netflix_pods:
                    pod_name = pod.metadata.name
                    logging.error(f"🔥 Terminating pod: {pod_name}")
                    v1.delete_namespaced_pod(name=pod_name, namespace="default")
                logging.critical("All Netflix service pods terminated. Waiting 60 seconds before next check...")
                time.sleep(60)
                continue
            
            # Randomly pick a pod to terminate
            pod_to_kill = random.choice(netflix_pods)
            pod_name = pod_to_kill.metadata.name
            
            logging.warning(f"🔥 Chaos Monkey is terminating pod: {pod_name}")
            
            v1.delete_namespaced_pod(name=pod_name, namespace="default")
            
            # Wait for some time before next "attack"
            wait_time = random.randint(30, 60)
            logging.info(f"Waiting {wait_time} seconds for next attack...")
            time.sleep(wait_time)
            
    except Exception as e:
        logging.exception(f"Error in Chaos Monkey: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Netflix Chaos Monkey for Kubernetes disaster drills.")
    parser.add_argument(
        "--global-outage",
        action="store_true",
        help="Trigger a global outage by terminating all Netflix service pods at once. Overrides GLOBAL_OUTAGE_MODE env var."
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default=None,
        help="Path to a file to write logs to (in addition to console)."
    )
    parser.add_argument(
        "--log-max-bytes",
        type=int,
        default=5*1024*1024,
        help="Maximum size (in bytes) of a log file before rotation. Default: 5MB."
    )
    parser.add_argument(
        "--log-backup-count",
        type=int,
        default=3,
        help="Number of rotated backup log files to keep. Default: 3."
    )
    args = parser.parse_args()

    # CLI flag takes precedence, else fallback to env var
    if args.global_outage:
        GLOBAL_OUTAGE_MODE = True
    else:
        GLOBAL_OUTAGE_MODE = os.environ.get("GLOBAL_OUTAGE_MODE", "false").lower() == "true"

    chaos_monkey(
        global_outage_mode=GLOBAL_OUTAGE_MODE,
        log_file=args.log_file,
        log_max_bytes=args.log_max_bytes,
        log_backup_count=args.log_backup_count
    )
