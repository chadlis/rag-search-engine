import string
from collections.abc import Iterator

from nltk.stem import PorterStemmer

PUNCTUATION_TABLE = str.maketrans(string.punctuation, len(string.punctuation) * " ")
STEMMER = PorterStemmer()

def tokenize(text: str) -> list[str]:
    return text.lower().translate(PUNCTUATION_TABLE).split()

def stem_and_filter(text: str, stopwords: set[str]) -> list[str]:
    return [STEMMER.stem(t) for t in tokenize(text) if t not in stopwords]

def matches_query(query_stems: list[str], text: str, stopwords: list[str]) -> bool:
    text_stems = stem_and_filter(text, stopwords)
    return any(q == t for q in query_stems for t in text_stems)

def search_query(query: str, movies: list[dict], stopwords: set[str]) -> Iterator[dict]:
    query_stems = stem_and_filter(query, stopwords)
    return (m for m in movies if matches_query(query_stems, f"{m['title']} {m['description']}", stopwords))
