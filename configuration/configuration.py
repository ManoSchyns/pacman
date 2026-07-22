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
    """Configuration du jeu, validée et corrigée par pydantic."""

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
        """Valide la liste des niveaux et complète ceux qui manquent.

        Args:
            arg: valeur brute lue dans la configuration.

        Returns:
            La liste des niveaux valides, complétée à 10 au minimum.
        """

        list_level: list[tuple[int, int]] = []

        if not isinstance(arg, list):
            print("\nLevel list must be a list")
            print("Pacman_42 is using the default configuration for levels")
            return DEFAULT_LIST_LEVEL

        for data in arg:
            if not isinstance(data, (tuple, list)):
                print("\nLevel list must be a list of tuple")

            elif len(data) != 2:
                print("\nEach level must contain only a width and a height.")

            elif not isinstance(data[0], int) or not isinstance(data[1], int):
                print("\nThe width and height of the "
                      "levels must be integer values.")

            elif data[0] < 2 or data[1] < 2 or data[0] > 35 or data[1] > 35:
                print("\nThe width and height of the levels "
                      "must not be less than 2 or greater than 35.")

            else:
                list_level.append((data[0], data[1]))

        curr_n_levels: int = len(list_level)
        if curr_n_levels < 10:
            missings_level: int = 10 - curr_n_levels
            print("\nLevel list must contains at least 10 valid levels")
            print(f"===> Adding {missings_level} levels from "
                  "de default configuration\n")
            list_level.extend(DEFAULT_LIST_LEVEL[:missings_level])
            print(list_level)

        return list_level

    @staticmethod
    def is_positive_int(arg_name: str, arg: Any) -> bool:
        """Vérifie que la valeur est un entier strictement positif.

        Args:
            arg_name: nom du champ affiché dans les messages d'erreur.
            arg: valeur à vérifier.

        Returns:
            True si la valeur est un entier positif, False sinon.
        """
        if not isinstance(arg, int):
            print(f"\nThe {arg_name} must be a int")
            return False
        if arg < 1:
            print(f"\nThe {arg_name} must be greater than 0")
            return False
        return True

    @field_validator("number_pacgum", mode="before")
    @classmethod
    def validate_number_pacgums(cls: Any, arg: Any) -> int:
        """Valide le nombre de pac-gommes, sinon retourne 42."""
        if not cls.is_positive_int("number_pacgum", arg):
            return 42
        return int(arg)

    @field_validator("points_per_pacgum", mode="before")
    @classmethod
    def validate_points_per_pacgums(cls: Any, arg: Any) -> int:
        """Valide les points par pac-gomme, sinon retourne 10."""
        if not cls.is_positive_int("points_per_pacgum", arg):
            return 10
        return int(arg)

    @field_validator("points_per_super_pacgum", mode="before")
    @classmethod
    def validate_points_per_super_pacgums(cls: Any, arg: Any) -> int:
        """Valide les points par super pac-gomme, sinon retourne 20."""
        if not cls.is_positive_int("points_per_super_pacgum", arg):
            return 20
        return int(arg)

    @field_validator("points_per_ghost", mode="before")
    @classmethod
    def validate_points_per_ghost(cls: Any, arg: Any) -> int:
        """Valide les points par fantôme mangé, sinon retourne 40."""
        if not cls.is_positive_int("points_per_ghost", arg):
            return 40
        return int(arg)

    @field_validator("lives", mode="before")
    @classmethod
    def validate_lives(cls: Any, arg: Any) -> int:
        """Valide le nombre de vies du joueur, sinon retourne 1."""
        if not cls.is_positive_int("lives", arg):
            return 1
        return int(arg)

    @field_validator("seed", mode="before")
    @classmethod
    def validate_seed(cls: Any, arg: Any) -> int:
        """Valide la graine aléatoire, sinon retourne 42."""
        if not isinstance(arg, int):
            print("\nThe seed must be a int")
            return 42
        if arg < 0:
            print("\nThe seed must be positive")
            return 42
        return int(arg)

    @field_validator("level_max_time", mode="before")
    @classmethod
    def validate_level_max_time(cls: Any, arg: Any) -> int:
        """Valide le temps maximum par niveau, sinon retourne 100."""
        if not cls.is_positive_int("level_max_time", arg):
            return 100
        return int(arg)
