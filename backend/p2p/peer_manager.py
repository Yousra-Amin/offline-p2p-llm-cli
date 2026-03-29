# backend/p2p/peer_manager.py

import socket
import json


def send_step_to_peer(peer, step):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)

        peer_ip, port = peer
        client.connect((peer_ip, port))

        request = json.dumps({"step": step})
        client.sendall(request.encode())

        response = client.recv(8192).decode()
        data = json.loads(response)

        return data["result"]

    except Exception as e:
        print(f"❌ Peer failed: {peer_ip}", e)
        return None
