import socket
import time

NODE_USER = 'Azra'
POINTS_ADDED = 3

print(f"[C Client] Starting...")
print(f"[C Client] Connecting to server on port 8082")
print(f"[C Client] Points added per update: +{POINTS_ADDED}")
print("========================================\n")

while True:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('azra-server', 8082))
        print("[C Client] ✅ Connected to server!")

        client.sendall(b"PING")
        print("[C Client] 📤 Sent: PING")

        response = client.recv(1024).decode()
        print(f"[C Client] 📥 Server response: {response}")
        print(f"[C Client] ✅ +{POINTS_ADDED} points added to database!")

        client.close()
        print("========================================\n")

    except ConnectionRefusedError:
        print("[C Client] ⏳ Waiting for server...")
    except Exception as e:
        print(f"[C Client] Error: {e}")

    time.sleep(30)
