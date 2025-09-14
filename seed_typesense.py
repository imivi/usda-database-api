import sqlite3
from typesense_client import create_typesense_client
import food_service
import typesense_service
import typesense


def recreate_collection(client: typesense.Client):

    # Drop pre-existing collection if any
    try:
        client.collections["foods"].delete()
    except Exception as e:
        pass

    # Create a collection
    client.collections.create({
        "name": "foods",
        "fields": [
            {"name": "food_id", "type": "int32"},
            {"name": "food_name", "type": "string"},
        ],
        "default_sorting_field": "food_id"
    })



def seed_typesense(client: typesense.Client):
    '''
    1. Reset the "foods" collection
    2. Get foods from database, in chunks of 100
    3. Insert them into typesense
    '''

    recreate_collection(client)

    after_food_id = 0
    with sqlite3.connect("database/db.sqlite3") as db_conn:

        while True:
            
            foods = food_service.get_food_names(db_conn, 1000, after_food_id)
            
            if len(foods) == 0:
                break

            food_ids = [food.food_id for food in foods]
            min_food_id = min(food_ids)
            max_food_id = max(food_ids)
            after_food_id = max_food_id
            typesense_service.add_foods(client, foods)
            print(f"Added foods with id {min_food_id}-{max_food_id}")


if __name__ == "__main__":
    from env import env
    client = create_typesense_client()
    print("Seeding Typesense...", env.TYPESENSE_HOST, env.TYPESENSE_PORT)
    seed_typesense(client)