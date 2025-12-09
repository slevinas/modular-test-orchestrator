# docker/test-target/app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import socket
import os
import time

app = FastAPI(title="Modular Test Orchestrator Demo Target")

START_TIME = time.time()


class EchoRequest(BaseModel):
    message: str


@app.get("/health")
async def health():
    """Simple liveness check."""
    return {"status": "ok"}


@app.get("/info")
async def info():
    """Basic metadata for sanity checks."""
    return {
        "service": "demo-test-target",
        "host": socket.gethostname(),
        "env": os.getenv("APP_ENV", "local"),
        "uptime_seconds": round(time.time() - START_TIME, 2),
    }


@app.post("/echo")
async def echo(body: EchoRequest):
    """Round-trip payload check."""
    return {"echo": body.message}
