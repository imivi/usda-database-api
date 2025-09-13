from fastapi import FastAPI, HTTPException
import food_service
import sqlite3
from env import env
import utils
import models
import json


# Initialize Fastapi
app = FastAPI()

# Connect to SQLite database
db_conn = sqlite3.connect("database/db.sqlite3")

# Create Redis client if required
redis_client = utils.create_redis_client(env.REDIS_HOST, env.REDIS_PORT)


@app.get("/")
async def root():
    return {"message": "Welcome to the unofficial USDA Database API"}


@app.get("/foods")
async def get_foods(limit: int, after: int):
    max_rows = 100  # Return at most 100 foods
    foods = food_service.get_multiple_foods_with_nutrients(
        db_conn,
        min(limit, max_rows),
        after,
    )
    return foods


@app.get("/foods/{food_id}")
async def get_food_by_id(food_id: int):

    if redis_client is not None:
        try:
            cached_food_json = redis_client.get(str(food_id))

            # Cache hit
            if cached_food_json is not None:
                food = models.create_food_from_dict(json.loads(cached_food_json))
                return food

            # Else, cache miss

        except Exception as error:
            print(error)
            raise HTTPException(
                status_code=500,
                detail="Error reading from Redis cache",
            )

    food = food_service.get_food(db_conn, food_id)
    if food is not None and redis_client is not None:
        # print("Saving food into redis as json:", food.to_json())
        redis_client.set(str(food_id), food.to_json())

    if food is None:
        raise HTTPException(status_code=404, detail=f"Food not found: {food_id}")

    return food
