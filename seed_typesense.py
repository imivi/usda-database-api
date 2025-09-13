import sqlite3
from typesense_client import client, add_foods
import food_service


def recreate_collection():

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



def main():
    '''
    1. Reset the "foods" collection
    2. Get foods from database, in chunks of 100
    3. Insert them into typesense
    '''
    recreate_collection()

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
            add_foods(foods)
            print(f"Added foods with id {min_food_id}-{max_food_id}")

if __name__ == "__main__":
    main()