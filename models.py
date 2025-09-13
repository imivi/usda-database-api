from dataclasses import dataclass, asdict
import json


@dataclass
class FoodNutrient:
    food_nutrient_id: int
    fdc_id: int
    food_nutrient_amount: float
    nutrient_id: int
    nutrient_name: str
    nutrient_unit_name: str
    food_description: str
    food_data_type: str


@dataclass
class FoodNutrientMinimal:
    food_nutrient_id: int
    food_nutrient_amount: float
    nutrient_id: int
    nutrient_name: str
    nutrient_unit_name: str
    is_macro: bool

    def to_json(self):
        return json.dumps(self.__dict__)


@dataclass
class Food:
    id: int
    description: str
    data_type: str
    nutrients: list[FoodNutrientMinimal]

    def to_json(self):
        return json.dumps(asdict(self))


def create_food_from_dict(data: dict) -> Food:
    return Food(
        id=data["id"],
        description=data["description"],
        data_type=data["data_type"],
        nutrients=[FoodNutrientMinimal(**values) for values in data["nutrients"]],
    )



@dataclass
class TypesenseFood:
    food_id: int
    food_name: str

