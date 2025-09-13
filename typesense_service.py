import typesense
from models import TypesenseFood


def add_food(client: typesense.Client, food_id:int, food_name:str):
    client.collections["foods"].documents.create({
        "food_id": food_id,
        "food_name": food_name,
    })


def add_foods(client: typesense.Client, foods:list[TypesenseFood]):
    client.collections["foods"].documents.import_([food.__dict__ for food in foods])


def search_foods(client: typesense.Client, food_name: str, limit: int):
    print("Searching foods...")
    response = client.collections['foods'].documents.search({
        'q': food_name,
        'query_by': 'food_name',
        # 'sort_by': 'food_name:desc',
        "limit": limit,
    })
    return response["hits"]


def get_all_items(client: typesense.Client):
    items = client.collections["foods"].documents.export()
    return items
