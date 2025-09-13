# USDA Database API

## 💡 What is this?

This is an unofficial open source API for **FoodData Central**, USDA's food nutrition database. More information here: https://fdc.nal.usda.gov/

This project is non-commercial and not affiliated with USDA in any way.

Note that the USDA datasets are not included in this repository. If you wish to run this API, you will have to download them from USDA as described below.

## ⚙️ Installation

Requirement: Docker and Docker Compose

1. Clone or download this repository
2. Download the CSV datasets ("Foundation Foods", "SR Legacy" and "FNDDS") from the USDA website: https://fdc.nal.usda.gov/download-datasets
3. After downloading and unzipping the datasets, copy the CSV datasets listed below inside the `datasets` directory

```txt
datasets/
├── foundation/
|   ├── food_category.csv
|   ├── food.csv
|   ├── food_nutrient.csv
|   └── nutrient.csv
├── sr_legacy/
|   ├── food_category.csv
|   ├── food.csv
|   ├── food_nutrient.csv
|   └── nutrient.csv
└── fndds_survey/
    ├── (omit food_category.csv!)
    ├── food.csv
    ├── food_nutrient.csv
    └── nutrient.csv
```

Run `docker compose up`. This will run a Redis server; then the API will initialize and seed the SQLite database by reading from the datasets; finally the API will serve the food nutrient data via the HTTP endpoints listed below.

## 🌐 API endpoints

| Method | Endpoint | Returned value |
| -      | -        | -              |
| GET    | `/foods/:food_id` | Food |
| GET    | `/foods?limit=<int>&after=<food_id>` | list[Food] |

```py
Food = {
    description: str
    data_type: str
    nutrients: list[
        food_nutrient_id: int
        food_nutrient_amount: float
        nutrient_id: int
        nutrient_name: str
        is_macro: bool
    ]
}
```

## Example

`GET http://localhost:8000/foods/168567`

Result:

```json
{
    "id": 168567,
    "description": "Tomatoes, sun-dried",
    "data_type": "sr_legacy_food",
    "nutrients": [
        {
            "food_nutrient_id": 1370638,
            "food_nutrient_amount": 0.402,
            "nutrient_id": 1222,
            "nutrient_name": "Alanine",
            "nutrient_unit_name": "G",
            "is_macro": false
        },
        {
            "food_nutrient_id": 1370583,
            "food_nutrient_amount": 0.0,
            "nutrient_id": 1018,
            "nutrient_name": "Alcohol, ethyl",
            "nutrient_unit_name": "G",
            "is_macro": false
        },
        {
            "food_nutrient_id": 1370657,
            "food_nutrient_amount": 0.343,
            "nutrient_id": 1220,
            "nutrient_name": "Arginine",
            "nutrient_unit_name": "G",
            "is_macro": false
        },
        {
            "food_nutrient_id": 1370620,
            "food_nutrient_amount": 12.6,
            "nutrient_id": 1007,
            "nutrient_name": "Ash",
            "nutrient_unit_name": "G",
            "is_macro": false
        },
        ...
    ]
}
```

## Database schema

<img src="https://github.com/imivi/usda-database-api/blob/main/docs/usda_database_schema.png" alt="Database schema">
