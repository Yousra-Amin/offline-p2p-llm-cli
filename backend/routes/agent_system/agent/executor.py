# agent/executor.py

from routes.agent_system.llm.llm import call_llm

def execute_step(step, context=""):
	prompt = f"""
You are an AI executor.

Execute this step:
{step}

Context:
{context}

Return result:
"""

	result = call_llm(prompt)
	return result