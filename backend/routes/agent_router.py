# backend/routes/agent.py

from fastapi import APIRouter
from pydantic import BaseModel
from routes.agent_system.agent.agent import run_agent_steps  # we’ll modify this

router = APIRouter()

class TaskRequest(BaseModel):
	task: str

@router.post("/run")
def run_task(req: TaskRequest):
	results = run_agent_steps(req.task)
	return {"steps": results}
# {
#   "steps": [
#     {
#       "step": "step 1",
#       "result": "result 1"
#     },
#     {
#       "step": "step 2",
#       "result": "result 2"
#     },
#     {
#       "step": "step 3",
#       "result": "result 3"
#     },
#     {
#       "step": "step 4",
#       "result": "result 4"
#     },
#     {
#       "step": "step 5",
#       "result": "result 5"
#     },
#   ]
# }