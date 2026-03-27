# backend/main.py

from fastapi import FastAPI
from routes.agent_router import router as agent_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],  # for development
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(agent_router)

@app.get("/")
def root():
	return {"message": "Agentic backend running"}