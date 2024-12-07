import json
import os
from pathlib import Path
from typing import Any


def _file_exists(year: int, day: int, part: int, sub_part: str = "") -> bool:
    file_path: Path = (
        Path(os.environ["SUGARPLUM_BASE_PATH"])
        / f"{year}/{day:02}/test-{part}{sub_part}.in"
    )

    return file_path.exists()


def _read_file(file_path: str) -> str:
    with open(os.environ["SUGARPLUM_BASE_PATH"] + "/" + file_path) as f:
        return f.read()


def get_input(year: int, day: int) -> str:
    return _read_file(f"{year}/{day:02}/data.in")


def _get_single_test_data(year: int, day: int, part: int) -> tuple[str, str]:
    input_data: str = _read_file(f"{year}/{day:02}/test-{part}.in")
    result: Any = json.loads(_read_file(f"{year}/{day:02}/test-{part}.out"))

    return (input_data, result)


def _get_multiple_test_data(year, day, part) -> list[tuple[str, str]]:
    sub_part: str = "a"
    test_data: list[tuple[str, Any]] = []
    while _file_exists(year, day, part, sub_part):
        test_data.append(
            (
                _read_file(f"{year}/{day:02}/test-{part}{sub_part}.in"),
                json.loads(_read_file(f"{year}/{day:02}/test-{part}{sub_part}.out")),
            )
        )
        sub_part = chr(ord(sub_part) + 1)

    return test_data


def get_test_data(
    year: int, day: int, part: int
) -> tuple[str, Any] | list[tuple[str, Any]]:
    if _file_exists(year, day, part):
        return _get_single_test_data(year, day, part)
    else:
        return _get_multiple_test_data(year, day, part)
