from .configuration import Config
from typing import Any
from typing import TextIO
import json


COMMENTS_STYLE = [
    "#",
    "//"
]

KEYS = [
    "level_list",
    "number_pacgum",
    "points_per_pacgum",
    "points_per_super_pacgum",
    "points_per_ghost",
    "lives",
    "seed",
    "level_max_time"
]


def chek_file_name(filename: str) -> bool:
    """Vérifie que le fichier porte bien l'extension .json."""
    extension: list[str] = filename.split(".")

    if extension[len(extension) - 1] != "json":
        print("The File must be a [.json] File")
        return False
    return True


def suppress_comment(file: TextIO) -> str:
    """Retourne le contenu du fichier sans les lignes de commentaire."""
    lines_without_comments: list[str] = []
    for line in file:
        if not any(line.strip().startswith(comment)
                   for comment in COMMENTS_STYLE):
            lines_without_comments.append(line)
    return ("".join(lines_without_comments))


def json_without_comment(filename: str) -> tuple[bool, dict[str, Any]]:
    """Charge le fichier JSON une fois les commentaires supprimés.

    Args:
        filename: chemin du fichier de configuration.

    Returns:
        Un tuple (succès de la lecture, données lues).
    """
    datas: dict[str, Any] = {}
    try:
        with open(filename, "r") as file:
            json_text = suppress_comment(file)
            datas = json.loads(json_text)
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error opening the file: {e}")
        return (False, datas)
    except (json.decoder.JSONDecodeError) as e:
        print(f"Error configuration of the json: {e}")
        return (False, datas)
    return (True, datas)


def check_keys(datas: dict[str, Any]) -> None:
    """Signale les clés absentes de la configuration."""
    for key in KEYS:
        if key not in datas.keys():
            print(f"\nKey : {key} is missing. "
                  f"Using default configuration for {key}\n")


def parse(filename: str) -> tuple[bool, Config]:
    """Analyse le fichier de configuration et construit la Config.

    Args:
        filename: chemin du fichier de configuration.

    Returns:
        Un tuple (succès de l'analyse, configuration utilisable).
    """
    datas: dict[str, Any]
    ret_val: tuple[bool, dict[str, Any]]

    if not chek_file_name(filename):
        return (False, Config())
    ret_val = json_without_comment(filename)
    if not ret_val[0]:
        return (False, Config())
    datas = ret_val[1]
    check_keys(datas)
    return (True, Config(**datas))


if __name__ == "__main__":
    config = parse("config.json")
