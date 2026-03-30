# cluster.py

import os

NODES = [
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003",
]

SELF = os.getenv("SELF_URL")

MASTER = os.getenv("MASTER_URL")  # dynamic in real system

def is_master():
    return SELF == MASTER
