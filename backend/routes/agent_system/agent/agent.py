# backend/agent/agent.py

from routes.agent_system.agent.planner import create_plan
from routes.agent_system.agent.executor import execute_step

def run_agent_steps(task):
	steps = create_plan(task)

	results = []
	context = ""

	for step in steps:
		result = execute_step(step, context)

		results.append({
			"step": step,
			"result": result
		})

		context += f"\n{result}"

	return results