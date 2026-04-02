from pathlib import Path
import pickle

from search import tokenize

INDEX_FILENAME = "index.pkl"
DOCMAP_FILENAME = "docmap.pkl"


class InvertedIndex:
    def __init__(self):
        self.index: dict[str, set[int]] = {}
        self.docmap: dict[int, list[str]] = {}

    def __add_document(self, doc_id, tokens):
        self.docmap.setdefault(doc_id, []).extend(tokens)
        for token in tokens:
            self.index.setdefault(token, set()).add(doc_id)

    def get_documents(self, term):
        return sorted(self.index.get(term, []), reverse=True)

    def build(self, movies):
        for movie in movies:
            doc_id, text = movie["id"], f"{movie['title']} {movie['description']}"
            tokens = tokenize(text)
            self.__add_document(doc_id, tokens)

    @classmethod
    def load(cls, cache_directory: Path) -> "InvertedIndex":

        index_filepath = Path(cache_directory) / INDEX_FILENAME
        docmap_filepath = Path(cache_directory) / DOCMAP_FILENAME

        if not index_filepath.exists():
            raise FileNotFoundError(f"{index_filepath} not found!")

        if not docmap_filepath.exists():
            raise FileNotFoundError(f"{docmap_filepath} not found!")

        instance = cls()
        with open(index_filepath, "rb") as f:
            instance.index = pickle.load(f)
        with open(docmap_filepath, "rb") as f:
            instance.docmap = pickle.load(f)
        return instance

    def save(self, cache_directory):
        cache_directory.mkdir(parents=True, exist_ok=True)
        with open(cache_directory / INDEX_FILENAME, "wb") as f:
            pickle.dump(self.index, f)
        with open(cache_directory / DOCMAP_FILENAME, "wb") as f:
            pickle.dump(self.docmap, f)
