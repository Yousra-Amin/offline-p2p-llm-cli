from agent_system.agent.planner import create_plan
from agent_system.agent.executor import execute_step
from p2p.peer_manager import send_step_to_peer
from p2p.peers import PEERS


def run_agent_steps(task):
    steps = create_plan(task)

    results = []
    # context = ""

    print("\n\nPrinting Steps\n\n")
    print(steps)

    for i, step in enumerate(steps):

        # 🔁 Try peer first (load sharing)
        peer_ip = PEERS[i % len(PEERS)] if PEERS else None

        if peer_ip:
            print(f"🌍 Sending to peer {peer_ip}")
            result = send_step_to_peer(peer_ip, step)

            # ⚠️ Fault tolerance
            if result is None:
                print("⚠️ Peer failed, running locally")
                result = execute_step(step)
        else:
            result = execute_step(step)

        results.append({"step": step, "result": result})

        # context += f"\n{result}"

    return results
