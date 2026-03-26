# main.py

from agent.agent import run_agent

def main():
	print("=== Agentic System (Phase 1) ===")

	while True:
		task = input("\nEnter a task (or 'exit'): ")

		if task.lower() == "exit":
			break

		run_agent(task)


if __name__ == "__main__":
	main()