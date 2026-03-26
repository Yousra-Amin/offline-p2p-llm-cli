# agent/executor.py

from llm.llm import call_llm

def execute_step(step):
	prompt = f"""
You are an AI executor.

Execute this step:
{step}

Return result:
"""

	result = call_llm(prompt)
	return result