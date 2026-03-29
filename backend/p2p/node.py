# backend/p2p/node.py

import socket
import threading
import json
from agent_system.agent.executor import execute_step

HOST = "0.0.0.0"


def handle_client(conn, addr):
    try:
        data = conn.recv(4096).decode()
        request = json.loads(data)

        step = request.get("step")

        print(f"📥 Received task from {addr}: {step}")

        result = execute_step(step)

        response = json.dumps({"result": result})
        conn.sendall(response.encode())

    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()


def start_node(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, port))
    server.listen(5)

    print(f"🌐 Node listening on port {port}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
