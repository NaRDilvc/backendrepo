from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# ✅ Enable CORS for localhost dev + deployed frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://my-fastapi-backend-ajenfcfqejehav4d.southeastasia-01.azurewebsites.net"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ POST /greet/
@app.post("/greet/")
def greet_user(payload: dict = Body(...)):
    name = payload.get("name", "").strip()
    if not name:
        return {"message": "Please provide a name."}
    return {"message": f"Hi {name}, Welcome!"}
