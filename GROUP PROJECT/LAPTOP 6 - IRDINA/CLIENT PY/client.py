import socket
import time

NODE_USER = 'Irdina'
POINTS_ADDED = 4

print(f"[Python Client] Starting...")
print(f"[Python Client] Connecting to server on port 8084")
print(f"[Python Client] Points added per update: +{POINTS_ADDED}")
print("========================================\n")

while True:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('irdina-server', 8084))
        print("[Python Client] ✅ Connected to server!")

        client.sendall(b"TRIGGER")
        print("[Python Client] 📤 Sent: TRIGGER")

        response = client.recv(1024).decode()
        print(f"[Python Client] 📥 Server response: {response}")
        print(f"[Python Client] ✅ +{POINTS_ADDED} points added to database!")

        client.close()
        print("========================================\n")

    except ConnectionRefusedError:
        print("[Python Client] ⏳ Waiting for server...")
    except Exception as e:
        print(f"[Python Client] Error: {e}")

    time.sleep(30)
