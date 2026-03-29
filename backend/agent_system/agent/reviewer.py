from agent_system.llm.llm import call_llm, REVIEWER_MODEL


def review_step(step, result):
    prompt = f"""
You are a reviewer agent.

Step:
{step}

Result:
{result}

Is this correct and useful?

If yes, say "OK".
If not, suggest a fix.
"""

    return call_llm(prompt, REVIEWER_MODEL)
