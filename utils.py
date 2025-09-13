from models import FoodNutrient
import redis


def create_redis_client(host: str | None, port: int | None) -> redis.Redis | None:

    if host is not None and port is not None:
        redis_client = redis.Redis(host=host, port=port, decode_responses=True)
        return redis_client

    return None


macros_nutrient_ids = {
    1062: "energy (kjoules?)",
    1008: "energy (kcal?)",
    1079: "fiber",
    1292: "fats mono",
    1293: "fats poly",
    1258: "fats sat",
    1003: "protein",
    1005: "carbs (by difference)",
}


def nutrient_is_macro(nutrient: FoodNutrient) -> bool:
    return nutrient.nutrient_id in macros_nutrient_ids
