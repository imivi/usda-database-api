import os
import sqlite3
from env import env

import pandas as pd


def get_csv_paths(folder_path: str) -> list[str]:
    csv_files = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))

    return csv_files


def initialize_db(db_conn: sqlite3.Connection):
    cursor = db_conn.cursor()

    create_tables_query = """
    CREATE TABLE IF NOT EXISTS food_category (
        id INTEGER PRIMARY KEY,
        code INTEGER,
        description TEXT
    );
    CREATE TABLE IF NOT EXISTS food (
        fdc_id INTEGER PRIMARY KEY,
        data_type TEXT,
        description TEXT,
        food_category_id INTEGER,
        publication_date TEXT
    );
    CREATE TABLE IF NOT EXISTS food_nutrient (
        id INTEGER PRIMARY KEY,
        fdc_id INTEGER,
        nutrient_id INTEGER,
        amount REAL,
        data_points INTEGER,
        derivation_id INTEGER,
        min TEXT,
        max TEXT,
        median TEXT,
        footnote TEXT,
        min_year_acquired TEXT
    );
    CREATE TABLE IF NOT EXISTS nutrient (
        id INTEGER PRIMARY KEY,
        name TEXT,
        unit_name TEXT,
        nutrient_nbr INTEGER,
        rank INTEGER
    );
    """

    cursor.executescript(create_tables_query)

    db_conn.commit()


def insert_rows_into_db(db_cursor: sqlite3.Cursor, table_name, csv_chunk):

    values = [tuple(row) for row in csv_chunk.values]
    placeholders = ", ".join(["?" for _ in csv_chunk.columns])
    insert_query = f"INSERT OR IGNORE INTO {table_name} VALUES ({placeholders})"

    db_cursor.executemany(insert_query, values)


def load_csv_into_table(db_conn: sqlite3.Connection, csv_path: str, table_name: str):

    chunk_size = 1000

    csv_chunks = pd.read_csv(
        csv_path,
        chunksize=chunk_size,
        header=0,  # Skip the header row
    )

    cursor = db_conn.cursor()

    for csv_chunk in csv_chunks:
        insert_rows_into_db(cursor, table_name, csv_chunk)

    db_conn.commit()


def get_csv_table(csv_path: str) -> str:
    name, _ = os.path.splitext(csv_path)
    for table_name in ["food", "food_nutrient", "nutrient", "food_category"]:
        if name.endswith(table_name):
            return table_name
    raise Exception("Invalid CSV name, cannot identify table:", csv_path)


def main():

    with sqlite3.connect("database/db.sqlite3") as db_conn:

        # Create tables if they don't exist yet
        if env.INIT_DB:
            initialize_db(db_conn)
            print('✅ Database initialized')

        # Read CSVs and insert rows into database
        if env.SEED_DB:
            for i, csv_path in enumerate(get_csv_paths("datasets")):
                table_name = get_csv_table(csv_path)
                print(i + 1, "CSV inserted into table:", csv_path, "-->", table_name)
                load_csv_into_table(db_conn, csv_path, table_name)
            print('✅ Database seeded')



if __name__ == "__main__":
    main()
