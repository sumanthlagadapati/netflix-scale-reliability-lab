import time
import random
from kubernetes import client, config

def chaos_monkey():
    try:
        # Load kubeconfig
        config.load_kube_config()
        v1 = client.CoreV1Api()
        
        print("--- Netflix Chaos Monkey Started ---")
        
        while True:
            # Get all pods in the default namespace
            pods = v1.list_namespaced_pod(namespace="default")
            
            # Filter for our netflix-lab pods
            netflix_pods = [pod for pod in pods.items if "service" in pod.metadata.name]
            
            if not netflix_pods:
                print("No Netflix service pods found. Waiting...")
                time.sleep(10)
                continue
                
            # Randomly pick a pod to terminate
            pod_to_kill = random.choice(netflix_pods)
            pod_name = pod_to_kill.metadata.name
            
            print(f"🔥 Chaos Monkey is terminating pod: {pod_name}")
            
            v1.delete_namespaced_pod(name=pod_name, namespace="default")
            
            # Wait for some time before next "attack"
            wait_time = random.randint(30, 60)
            print(f"Waiting {wait_time} seconds for next attack...")
            time.sleep(wait_time)
            
    except Exception as e:
        print(f"Error in Chaos Monkey: {e}")

if __name__ == "__main__":
    chaos_monkey()
