# agent/agent.py

from agent.planner import create_plan
from agent.executor import execute_step

def run_agent(task):
	print(f"\n🧠 Task: {task}\n")

	steps = create_plan(task)

	print("📋 Plan:")
	for s in steps:
		print(s)

	print("\n🚀 Executing...\n")

	for i, step in enumerate(steps):
		print(f"➡️ Step {i+1}: {step}")

		result = execute_step(step)

		print(f"✅ Result:\n{result}\n")

	print("🎉 Task Completed!\n")