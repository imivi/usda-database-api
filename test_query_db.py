import sqlite3
from food_service import get_food_nutrients
import utils


# Test foods
SUN_DRIED_TOMATOES = 168567
MUFFINS = 167515


def main():
    db_conn = sqlite3.connect("db.sqlite3")

    # rows = db_conn.execute(sql_query).fetchall()

    food_id = SUN_DRIED_TOMATOES

    print("Getting nutrients for food with id", food_id)

    for nutrient in get_food_nutrients(db_conn, food_id):
        if utils.nutrient_is_macro(nutrient):
            print(nutrient, "\n")


main()
