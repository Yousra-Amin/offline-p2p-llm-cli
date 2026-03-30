from agent_system.llm.llm import call_llm, EXECUTOR_MODEL


def execute_step(step, context=""):
    prompt = f"""
You are an execution agent.

Execute this step:
{step}

Current Context:
{context}

Return a clear and useful result.
"""
    if context == "":
        prompt = f"""
You are an execution agent.

Execute this step:
{step}

Return a clear and useful result.
"""

    return call_llm(prompt, EXECUTOR_MODEL)
