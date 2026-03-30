# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

from node.cluster import SELF, MASTER, is_master
from node.worker import process_subtask
from node.election import elect_new_master, get_alive_nodes
from agent_system.agent.planner import create_plan

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# Health Check
# -------------------------------
@app.get("/health")
async def health():
    return {"status": "alive"}


# -------------------------------
# New Master Select
# -------------------------------
@app.post("/set_master")
async def set_master(payload: dict):
    new_master = payload["master"]
    os.environ["MASTER_URL"] = new_master
    return {"result": "successful"}


# -------------------------------
# Receive Task (Entry Point)
# -------------------------------
@app.post("/task")
async def receive_task(payload: dict):
    task = payload["task"]

    if not is_master():
        # forward to master
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(f"{MASTER}/task", json=payload)
                return res.json()
        except:
            # master failed → elect new one
            new_master = await elect_new_master()
            if new_master == SELF:
                return await handle_as_master(task)
            else:
                async with httpx.AsyncClient() as client:
                    res = await client.post(f"{new_master}/task", json=payload)
                    return res.json()

    return await handle_as_master(task)


# -------------------------------
# Master Logic
# -------------------------------
async def handle_as_master(task: str):
    subtasks = split_task(task)

    results = await distribute_tasks(subtasks)

    # final = " ".join(results)
    # return {"result": final}
    print("printing results\n")
    print(results)
    return {"result": results}


# -------------------------------
# Split Task
# -------------------------------
def split_task(task: str):
    return create_plan(task)


# -------------------------------
# Distribution
# -------------------------------
async def distribute_tasks(subtasks):
    servants = await get_alive_nodes(include_self=False)

    curr_start = 0

    async def send(subtask, context):
        nonlocal curr_start
        for i in range(len(servants)):
            node = servants[(curr_start + i) % len(servants)]
            try:
                async with httpx.AsyncClient(timeout=120) as client:
                    print(f"Sending subtask={subtask[:10]} to node={node}")
                    res = await client.post(
                        f"{node}/subtask", json={"subtask": subtask, "context": context}
                    )
                    curr_start = (curr_start + i + 1) % len(servants)
                    return res.json()["result"]
            except:
                continue

        # fallback: master handles
        curr_start = 0
        print(f"Running locally subtask={subtask[:10]} in node={SELF}")
        return process_subtask(subtask, context)

    context = ""
    results = []

    for s in subtasks:
        result = await send(s, context)
        results.append(result)
        context += f"\n{result}"

    return results


# -------------------------------
# Servant Endpoint
# -------------------------------
@app.post("/subtask")
async def handle_subtask(payload: dict):
    subtask = payload["subtask"]
    context = payload["context"]

    try:
        result = process_subtask(subtask, context)
        return {"result": result}
    except:
        raise HTTPException(status_code=500, detail="Worker failed")
