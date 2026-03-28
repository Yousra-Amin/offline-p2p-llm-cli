from routes.agent_system.llm.llm import call_llm, EXECUTOR_MODEL

def execute_step(step, context):
	prompt = f"""
You are an execution agent.

Current context:
{context}

Execute this step:
{step}

Return a clear and useful result.
"""

	return call_llm(prompt, EXECUTOR_MODEL)