#!/bin/bash

source .venv/bin/activate
SELF_URL=http://localhost:$1 MASTER_URL=http://localhost:8000 uvicorn node.main:app --port $1