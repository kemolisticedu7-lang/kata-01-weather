from pathlib import Path


def ensure_directory(path_str: str) -> None:
    Path(path_str).mkdir(parents=True, exist_ok=True)