# agent/planner.py

from agent_system.llm.llm import call_llm, PLANNER_MODEL


def create_plan(task):
    prompt = f"""
You are a planning agent.

Break the task into clear, actionable steps.

Each step MUST be an instruction (imperative verb).

BAD example:
- "The chemical equation is..."

GOOD example:
- "Write the chemical equation"

Task:
{task}

Return ONLY numbered steps.
"""

    response = call_llm(prompt, PLANNER_MODEL)
    return parse_steps(response)


def parse_steps(response):
    lines = response.split("\n")
    steps = []

    current_step = ""

    print("\n\nprinting lines\n\n")
    print(lines)
    print("\n\n")

    for line in lines[2:]:
        line = line.strip()

        if (
            line[:4] == "Task"
            or line[:5] == "*Task"
            or line[:6] == "**Task"
            or line == ""
        ):
            continue

        if (
            line[1:2] == "."
            or line[2:3] == "."
            or line[3:4] == "."
            or line[4:5] == "."
            or line[:4] == "Step"
            or line[:5] == "*Step"
            or line[:6] == "**Step"
        ):
            if current_step != "":
                steps.append(current_step)
            current_step = line + "\n"
        else:
            current_step += line + "\n"

    if current_step != "":
        steps.append(current_step)
        current_step = ""

    return steps
