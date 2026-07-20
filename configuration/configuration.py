from pydantic import BaseModel, Field, field_validator
from typing import Any


DEFAULT_LIST_LEVEL: list[tuple[int, int]] = [
            (15, 17),
            (20, 21),
            (30, 30),
            (27, 10),
            (10, 10),
            (26, 27),
            (26, 17),
            (15, 13),
            (10, 7),
            (10, 10)]


class Config(BaseModel):
    level_list: list[tuple[int, int]] = Field(default=DEFAULT_LIST_LEVEL,
                                              min_length=10)
    number_pacgum: int = Field(default=42, ge=1)
    points_per_pacgum: int = Field(default=10, ge=1)
    points_per_super_pacgum: int = Field(default=20, ge=1)
    points_per_ghost: int = Field(default=40, ge=1)
    lives: int = Field(default=3, ge=1)
    seed: int = Field(default=42, ge=0)
    level_max_time: int = Field(default=100, ge=1)

    @field_validator("level_list", mode="before")
    @classmethod
    def validate_list_level(cls: Any, arg: Any) -> list[tuple[int, int]]:
        list_level: list[tuple[int, int]] = []

        if not isinstance(arg, list):
            print("Level list must be a list")
            return DEFAULT_LIST_LEVEL

        if len(arg) < 10:
            print("Level list must contains at least 10 levels")
            return DEFAULT_LIST_LEVEL

        for data in arg:
            if not isinstance(data, (tuple, list)):
                print("Level list must be a list of tuple")

            elif len(data) != 2:
                print("Each level must contain only a width and a height.")

            elif not isinstance(data[0], int) or not isinstance(data[1], int):
                print("The width and height of the "
                      "levels must be integer values.")

            elif data[0] < 2 or data[1] < 2 or data[0] > 35 or data[1] > 35:
                print("The width and height of the levels "
                      "must not be less than 2 or greater than 35.")

            else:
                list_level.append((data[0], data[1]))

        if len(list_level) < 10:
            print("Level list must contains at least 10 valid levels")
            return DEFAULT_LIST_LEVEL

        return list_level

    @staticmethod
    def is_positive_int(arg_name: str, arg: Any) -> bool:
        if not isinstance(arg, int):
            print(f"The {arg_name} must be a int")
            return False
        if arg < 1:
            print(f"The {arg_name} must be greater than 0")
            return False
        return True

    @field_validator("number_pacgum", mode="before")
    @classmethod
    def validate_number_pacgums(cls: Any, arg: Any) -> int:
        if not cls.is_positive_int("number_pacgum", arg):
            return 42
        return int(arg)

    @field_validator("points_per_pacgum", mode="before")
    @classmethod
    def validate_points_per_pacgums(cls: Any, arg: Any) -> int:
        if not cls.is_positive_int("points_per_pacgum", arg):
            return 10
        return int(arg)

    @field_validator("points_per_super_pacgum", mode="before")
    @classmethod
    def validate_points_per_super_pacgums(cls: Any, arg: Any) -> int:
        if not cls.is_positive_int("points_per_super_pacgum", arg):
            return 20
        return int(arg)

    @field_validator("points_per_ghost", mode="before")
    @classmethod
    def validate_points_per_ghost(cls: Any, arg: Any) -> int:
        if not cls.is_positive_int("points_per_ghost", int(arg)):
            return 40
        return int(arg)

    @field_validator("lives", mode="before")
    @classmethod
    def validate_lives(cls: Any, arg: Any) -> int:
        if not cls.is_positive_int("lives", arg):
            return 1
        return int(arg)

    @field_validator("seed", mode="before")
    @classmethod
    def validate_seed(cls: Any, arg: Any) -> int:
        if not isinstance(arg, int):
            print("The seed must be a int")
            return 42
        if arg < 0:
            print("The seed must be positive")
            return 42
        return int(arg)

    @field_validator("level_max_time", mode="before")
    @classmethod
    def validate_level_max_time(cls: Any, arg: Any) -> int:
        if not cls.is_positive_int("level_max_time", arg):
            return 100
        return int(arg)
