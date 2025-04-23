from fastapi import FastAPI, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

from database import SessionLocal
from models import User

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# ✅ Allow local + Azure frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://wonderful-glacier-00dcf8400.6.azurestaticapps.net"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 FastAPI app has started successfully!")

@app.get("/")
def read_root():
    logger.info("✅ GET request received at root endpoint")
    return {"message": "Hello from FastAPI on Azure!"}

# ✅ Get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

# ✅ POST /greet/ — stores name to DB
@app.post("/greet/")
async def greet_user(payload: dict = Body(...), db: AsyncSession = Depends(get_db)):
    name = payload.get("name", "").strip()
    if not name:
        return {"message": "Please provide a name."}

    logger.info(f"🧾 Storing user: {name}")

    new_user = User(name=name)
    db.add(new_user)
    await db.commit()

    return {"message": f"Hi {name}, Welcome!"}

# ✅ GET /users/ — returns all saved users
@app.get("/users/")
async def get_users(db: AsyncSession = Depends(get_db)):
    logger.info("📥 GET /users requested")
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [{"id": user.id, "name": user.name} for user in users]
