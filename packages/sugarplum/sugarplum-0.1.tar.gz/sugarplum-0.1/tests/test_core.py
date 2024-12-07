from pathlib import Path

import pytest

from sugarplum import get_input, get_test_data

YEAR: int = 2023
DAY: int = 24


@pytest.fixture(autouse=True)
def base_path(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SUGARPLUM_BASE_PATH", str(tmp_path))


@pytest.fixture(autouse=True)
def setup_dirs(tmp_path: Path) -> None:
    (tmp_path / str(YEAR)).mkdir()
    (tmp_path / f"{YEAR}/{DAY}").mkdir()


def create_file(path: Path, data: str) -> None:
    with open(path, "w") as f:
        f.write(data)


def test_puzzle_input_data_is_read(tmp_path: Path) -> None:
    expected: str = "North Pole"
    create_file(tmp_path / f"{YEAR}/{DAY}/data.in", expected)

    assert get_input(YEAR, DAY) == expected


def test_puzzle_day_number_gets_zero_padded(tmp_path: Path) -> None:
    expected: str = "sleigh"
    day: int = 3
    dir_path: Path = tmp_path / f"{YEAR}/{day:02}"
    dir_path.mkdir()
    create_file(dir_path / "data.in", expected)

    assert get_input(YEAR, day) == expected


def test_get_test_data_retrieves_input_and_output_data_for_single_test_case(
    tmp_path: Path,
) -> None:
    expected_input: str = "Christmas"
    expected_output: str = "Tree"
    part: int = 1
    create_file(tmp_path / f"{YEAR}/{DAY}/test-{part}.in", expected_input)
    create_file(tmp_path / f"{YEAR}/{DAY}/test-{part}.out", expected_output)

    assert get_test_data(YEAR, DAY, part) == (expected_input, expected_output)


def test_get_test_data_retrieves_multiple_input_and_output_data_for_multiple_test_cases(
    tmp_path: Path,
) -> None:
    expected_input_a: str = "Santa"
    expected_output_a: str = "Clause"
    expected_input_b: str = "Kris"
    expected_output_b: str = "Kringle"
    part: int = 1
    create_file(tmp_path / f"{YEAR}/{DAY}/test-{part}a.in", expected_input_a)
    create_file(tmp_path / f"{YEAR}/{DAY}/test-{part}a.out", expected_output_a)
    create_file(tmp_path / f"{YEAR}/{DAY}/test-{part}b.in", expected_input_b)
    create_file(tmp_path / f"{YEAR}/{DAY}/test-{part}b.out", expected_output_b)

    assert get_test_data(YEAR, DAY, part) == [
        (expected_input_a, expected_output_a),
        (expected_input_b, expected_output_b),
    ]
