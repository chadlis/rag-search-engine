import argparse
import os
from pathlib import Path
from typing import Iterator

from dotenv import load_dotenv

from .loader import load_movies, load_stopwords
from .search import search_query
from .indexes import InvertedIndex

load_dotenv()

DATA_DIR = Path(os.environ.get("DATA_DIR", "data"))
CACHE_DIR = Path(os.environ.get("DATA_DIR", "cache"))
MOVIES_FILENAME = "movies.json"
STOPWORDS_FILENAME = "stopwords.txt"


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    search_parser = subparsers.add_parser("search", help="Search movies")
    build_parser = subparsers.add_parser("build", help="Build movies")
    search_parser.add_argument("query", type=str, help="Search query")
    search_parser.add_argument(
        "--limit", type=int, default=5, help="Max results to display"
    )
    
    data = load_movies(DATA_DIR / MOVIES_FILENAME)
    
    args = parser.parse_args()
    match args.command:
        case "build":
            inverted_index = InvertedIndex()
            inverted_index.build(data)
            inverted_index.save(CACHE_DIR)
        case "search":
            print(f"Searching for: {args.query}")
            stopwords = load_stopwords(DATA_DIR / STOPWORDS_FILENAME)
            results = search_query(args.query, data, stopwords)
            display_results(results, limit=args.limit)
        case _:
            parser.print_help()


def display_results(results : Iterator[dict], limit: int = 5) -> None:
    found = False
    for i, result in enumerate(results):
        if i >= limit:
            break
        found = True
        print(f"{i + 1}. {result['title']}")
    if not found:
        print("No results found.")


if __name__ == "__main__":
    main()
