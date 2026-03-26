# agent/planner.py

from llm.llm import call_llm

def create_plan(task):
	prompt = f"""
You are an AI planner.

Break the following task into clear, numbered steps. Give all steps together and only the steps.

Task:
{task}

Steps:
1.
"""

	response = call_llm(prompt)

	steps = parse_steps(response)
	return steps


def parse_steps(response):
	lines = response.split("\n")
	steps = []

	current_step = ""

	for line in lines[2:]:

		if line[:4] == "Task" or \
			line[:5] == "*Task" or \
			line[:6] == "**Task" or \
			line == "":
			continue

		if line[1:2] == "." or \
			line[2:3] == "." or \
			line[3:4] == "." or \
			line[4:5] == "." or \
 			line[:4] == "Step" or \
			line[:5] == "*Step" or \
			line[:6] == "**Step":
			if current_step != "":
				steps.append(current_step)
			current_step = line + "\n"
		else:
			current_step += (line + "\n")
	
	if current_step != "":
		steps.append(current_step)
		current_step = ""

	return steps