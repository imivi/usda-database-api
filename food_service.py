import sqlite3
from typing import Any

from models import Food, FoodNutrient, FoodNutrientMinimal
import utils


def strip_nutrient_food_data(nutrient: FoodNutrient) -> FoodNutrientMinimal:
    """Modify nutrient values to remove unnecessary information the food it belongs to"""
    return FoodNutrientMinimal(
        food_nutrient_amount=nutrient.food_nutrient_amount,
        food_nutrient_id=nutrient.food_nutrient_id,
        nutrient_id=nutrient.nutrient_id,
        nutrient_name=nutrient.nutrient_name,
        nutrient_unit_name=nutrient.nutrient_unit_name,
        is_macro=utils.nutrient_is_macro(nutrient),
    )


def convert_food_nutrients_to_food(nutrients: list[FoodNutrient]) -> Food:

    return Food(
        id=nutrients[0].fdc_id,
        description=nutrients[0].food_description,
        data_type=nutrients[0].food_data_type,
        nutrients=[strip_nutrient_food_data(nutrient) for nutrient in nutrients],
    )


def get_food(db_conn: sqlite3.Connection, food_id: int) -> Food | None:
    nutrients = get_food_nutrients(db_conn, food_id)

    if len(nutrients) == 0:
        return None

    return convert_food_nutrients_to_food(nutrients)


def get_food_nutrients(db_conn: sqlite3.Connection, food_id: int) -> list[FoodNutrient]:

    # print("Getting food nutrients:", food_id)

    sql_query = """
        SELECT
            food_nutrient.id AS food_nutrient_id,
            food_nutrient.fdc_id AS fdc_id,
            food_nutrient.amount AS food_nutrient_amount,
            food_nutrient.nutrient_id AS nutrient_id,
            nutrient.name AS nutrient_name,
	        nutrient.unit_name AS nutrient_unit_name,
            food.description AS food_description,
            food.data_type AS food_data_type
        FROM food_nutrient
        -- The RIGHT JOIN below makes sure that if there are no matching nutrients no rows are returned
        RIGHT JOIN nutrient ON nutrient.id = food_nutrient.nutrient_id
        LEFT JOIN food ON food.fdc_id = food_nutrient.fdc_id
        WHERE food_nutrient.fdc_id = ?
        ORDER BY nutrient.name;
    """

    columns = [
        "food_nutrient_id",
        "fdc_id",
        "food_nutrient_amount",
        "nutrient_id",
        "nutrient_name",
        "nutrient_unit_name",
        "food_description",
        "food_data_type",
    ]

    rows = db_conn.execute(sql_query, [food_id]).fetchall()

    # Convert each row into a dictionary with column names as keys
    nutrients = [dict(zip(columns, values)) for values in rows]

    return [FoodNutrient(**values) for values in nutrients]


def get_multiple_foods_with_nutrients(
    db_conn: sqlite3.Connection, limit: int, after_id=0
) -> list[Food]:

    sql_query = f"""
        SELECT
            food_nutrient.nutrient_id AS food_nutrient_id,
            food.fdc_id AS fdc_id,
            food_nutrient.amount AS food_nutrient_amount,
            nutrient.id AS nutrient_id,
            nutrient.name AS nutrient_name,
	        nutrient.unit_name AS nutrient_unit_name,
            food.description AS food_description,
            food.data_type as food_data_type
        -- Create subquery
        FROM (
            select food.fdc_id, food.description, food.data_type
            FROM food
            WHERE food.fdc_id > {after_id}
            ORDER BY food.fdc_id
            LIMIT {limit}
        ) food
        LEFT JOIN food_nutrient ON food_nutrient.fdc_id = food.fdc_id
        LEFT JOIN nutrient ON nutrient.id = food_nutrient.nutrient_id;
    """

    columns = [
        "food_nutrient_id",
        "fdc_id",
        "food_nutrient_amount",
        "nutrient_id",
        "nutrient_name",
        "nutrient_unit_name",
        "food_description",
        "food_data_type",
    ]

    rows = db_conn.execute(sql_query).fetchall()

    nutrients_by_food: dict[int, list[Any]] = {}
    for row in rows:
        # Convert each row into a dictionary with column names as keys
        nutrients = dict(zip(columns, row))
        food_id = nutrients["fdc_id"]
        nutrients_by_food.setdefault(food_id, [])
        nutrients_by_food[food_id].append(nutrients)

    foods: list[Food] = []

    for food_nutrients in nutrients_by_food.values():
        if len(food_nutrients) > 0:
            nutrients_classes = [FoodNutrient(**values) for values in food_nutrients]
            foods.append(convert_food_nutrients_to_food(nutrients_classes))

    return foods
    # return [FoodNutrient(**values) for values in nutrients]


if __name__ == "__main__":
    db_conn = sqlite3.connect("database/db.sqlite3")
    foods = get_multiple_foods_with_nutrients(db_conn, 3, 167512)
    print(foods)
