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
    extension: list[str] = filename.split(".")
    err_flag: bool = False

    if len(extension) != 2:
        err_flag = True
    elif extension[1] != "json":
        err_flag = True
    if err_flag:
        print("The File must be a [.json] File")
        print("Using the default configuration")
        return False
    return True


def suppress_comment(file: TextIO) -> str:
    lines_without_comments: list[str] = []
    for line in file:
        if not any(line.strip().startswith(comment)
                   for comment in COMMENTS_STYLE):
            lines_without_comments.append(line)
    return ("".join(lines_without_comments))


def json_without_comment(filename: str) -> dict[str, Any]:
    datas: dict[str, Any] = {}
    try:
        with open(filename, "r") as file:
            json_text = suppress_comment(file)
            datas = json.loads(json_text)
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error opening the file: {e}")
        print("Using the default configuration")
    except (json.decoder.JSONDecodeError) as e:
        print(f"Error configuration of the json: {e}")
        print("Using the default configuration")
    return datas


def check_keys(datas: dict[str, Any]) -> None:
    for key in KEYS:
        if key not in datas.keys():
            print(f"Key : {key} is missing. "
                  f"Using default configuration for {key}")


def parse(filename: str) -> Config:
    if not chek_file_name(filename):
        return Config()
    datas: dict[str, Any] = json_without_comment(filename)
    check_keys(datas)
    return(Config(**datas))


if __name__ == "__main__":
    config = parse("config.json")
