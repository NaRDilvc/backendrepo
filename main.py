from fastapi import FastAPI, Query, Path, Body
import logging

# Logging config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Root route
@app.get("/")
def read_root():
    logger.info("📥 GET / called")
    return {"message": "Hello from FastAPI on Azure!"}

# Path + Query parameter route
@app.get("/items/{item_id}")
def read_item(
    item_id: int = Path(..., description="The ID of the item"),
    q: str = Query(None, description="Optional query string")
):
    logger.info(f"🔍 GET /items/{item_id}?q={q}")
    return {"item_id": item_id, "query": q}

# List route
@app.get("/products")
def list_products(limit: int = 10):
    logger.info(f"📋 GET /products?limit={limit}")
    return {"products": [f"Product {i+1}" for i in range(limit)]}

# POST route with JSON body
@app.post("/users/")
def create_user(user: dict = Body(...)):
    logger.info(f"🧍‍♂️ POST /users → {user}")
    return {"status": "User created", "user": user}
