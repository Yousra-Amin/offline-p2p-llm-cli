import sys
from p2p.node import start_node

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 5001

    start_node(port)
