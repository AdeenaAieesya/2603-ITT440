import socket
import pymysql
import time

NODE_USER = 'Azra'
LAPTOP1_IP = '192.168.43.248'
POINTS_ADDED = 3

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 8082))
server.listen(5)
print(f'[{NODE_USER}] Server on port 8082', flush=True)
print(f'[{NODE_USER}] Points added per update: +{POINTS_ADDED}', flush=True)

while True:
    try:
        conn, addr = server.accept()
        print(f'[{NODE_USER}] Client connected from {addr}', flush=True)
        msg = conn.recv(1024).decode()
        
        if "PING" in msg:
            try:
                db = pymysql.connect(host=LAPTOP1_IP, user='root', password='secretpass', database='library_stats', autocommit=True)
                with db.cursor() as cursor:
                    cursor.execute(f"UPDATE segmen_mata SET points = points + {POINTS_ADDED} WHERE user = '{NODE_USER}'")
                db.close()
                print(f'[{NODE_USER}] ✅ +{POINTS_ADDED}', flush=True)
                conn.sendall(b"OK")
            except Exception as e:
                print(f'[Error] {e}', flush=True)
                conn.sendall(b"FAIL")
        conn.close()
    except Exception as e:
        print(f'[Server Error] {e}', flush=True)
        time.sleep(1)
