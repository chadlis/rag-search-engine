from pathlib import Path
import json

def load_movies(filepath: Path) -> list[dict]:
    try:
        with open(filepath) as f:
            return json.load(f)["movies"]
    except FileNotFoundError as e:
        print(f"Error: {e.filename} not found")
        return

def load_stopwords(filepath: Path) -> set[str]:
    try:
        with open(filepath) as f:
            return set(f.read().splitlines())
    except FileNotFoundError as e:
        print(f"Error: {e.filename} not found")
        return
