from fastapi import FastAPI
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 FastAPI app has started successfully!")

@app.get("/")
def read_root():
    logger.info("✅ GET request received at root endpoint")
    return {"message": "Hello from FastAPI on Azure!"}
