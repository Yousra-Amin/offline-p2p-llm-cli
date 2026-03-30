# worker.py
from agent_system.agent.executor import execute_step


def process_subtask(step: str, context: str):
    response = execute_step(step, context)
    return response
