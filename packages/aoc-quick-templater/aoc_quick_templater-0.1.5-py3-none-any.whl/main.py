import os
from dataclasses import dataclass
from pathlib import Path

import httpx
import typer
from jinja2 import DictLoader, Environment

templates = {
    "sol": """from typing import Any


def solution_one(data: str) -> Any:
    pass


def solution_two(data: str) -> Any:
    pass


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    pass
    """
}

app = typer.Typer()


@dataclass
class State:
    api_key: str
    day: int
    problem_path: Path
    year: int = 2024
    overwrite: bool = False

    @property
    def input_path(self) -> Path:
        return self.problem_path / "input.txt"

    @property
    def solution_path(self) -> Path:
        return self.problem_path / "main.py"

    @property
    def url(self) -> str:
        return f"https://adventofcode.com/{self.year}/day/{self.day}/input"


def setup_input(s: State) -> None:
    input_path = s.problem_path / "input.txt"
    if not s.overwrite and input_path.exists():
        typer.secho(
            "Input already exists at problem location, in order to overwrite it pass in --overwrite"
        )
        return
    resp = httpx.get(s.url, cookies={"session": s.api_key})
    with open(input_path, "w") as f:
        f.write(resp.text)


def setup_solution(s: State) -> None:
    if not s.overwrite and s.solution_path.exists():
        typer.secho(
            "Solution already exists at problem location, in order to overwrite it pass in --overwrite"
        )
        return
    env = Environment(loader=DictLoader(templates))
    template = env.get_template("sol")
    result = template.render()
    with open(s.solution_path, "w") as f:
        f.write(result)


@app.command()
def new(
    day: int,
    year: int = 2024,
    dir_prefix: str = "",
    overwrite: bool = False,
    api_key: str = "",
) -> None:
    api_key = api_key or get_api_key()
    s = State(
        api_key,
        day,
        Path(f"{dir_prefix}{day}"),
        year,
        overwrite,
    )
    os.makedirs(s.problem_path, exist_ok=True)
    setup_input(s)
    setup_solution(s)


def get_api_key() -> str:
    api_key = os.getenv("api_key")
    if api_key:
        return api_key
    try:
        with open(".env", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        typer.secho("Error: Could not find API_KEY", fg="red", err=True)
        raise typer.Exit(1)

    for line in lines:
        key, value = line.split("=")
        if key.lower() == "api_key":
            return value.strip("\n")

    typer.secho("Error: Could not find API_KEY", fg="red", err=True)
    raise typer.Exit(1)


if __name__ == "__main__":
    app()
