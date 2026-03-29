# backend/llm/llm.py

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def call_llm(prompt, model):
    response = requests.post(
        OLLAMA_URL, json={"model": model, "prompt": prompt, "stream": False}
    )

    return response.json()["response"]


# Define roles (VERY IMPORTANT)
PLANNER_MODEL = "mistral"
EXECUTOR_MODEL = "phi"
REVIEWER_MODEL = "phi3:mini"
