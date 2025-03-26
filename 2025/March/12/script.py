import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

# Configuration
HOST = "8.138.23.35"
PORT = 8000
NUM_SAMPLES = 100000
MAX_WORKERS = 50  # Adjust based on your network/system capabilities

# Shared queue for results
results = Queue()
completed = 0
lock = threading.Lock()

def collect_sample():
    global completed
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)  # Set a timeout to avoid hanging connections
        s.connect((HOST, PORT))
        s.recv(1024).decode()  # Receive the prompt
        s.send(b"\n")  # Send empty key
        response = s.recv(1024).decode()
        s.close()
        
        if response.startswith("🔒 "):
            ciphertext = response[2:]
            results.put(eval(ciphertext))
            
            # Update counter with thread safety
            with lock:
                global completed
                completed += 1
                print(f"\rCompleted: {completed}/{NUM_SAMPLES}", end="", flush=True)
            
            return True
        return False
    except Exception as e:
        print(f"\nError: {e}")
        return False

def save_results():
    # Convert queue to list
    all_results = []
    while not results.empty():
        all_results.append(results.get())
    
    print(f"\nSaving {len(all_results)} results to out.txt")
    with open("out.txt", "wb") as f:
        f.write(b"\n\n\n".join(all_results))

def main():
    start_time = time.time()
    print(f"Starting collection of {NUM_SAMPLES} samples using {MAX_WORKERS} threads")
    
    # Use ThreadPoolExecutor to manage threads
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit tasks
        futures = [executor.submit(collect_sample) for _ in range(NUM_SAMPLES)]
        
        # Wait for all tasks to complete
        for future in futures:
            future.result()
    
    # Save all collected results
    save_results()
    
    elapsed = time.time() - start_time
    print(f"\nCompleted in {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()