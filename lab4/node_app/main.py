from fastapi import FastAPI
import os
import socket

app = FastAPI()

NODE_NAME = os.getenv("NODE_NAME", "Unknown Node")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "node": NODE_NAME,
        "container_id": socket.gethostname()
    }