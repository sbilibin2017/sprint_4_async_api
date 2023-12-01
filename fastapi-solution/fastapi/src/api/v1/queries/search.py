from core.config import Settings

CONFIG = Settings().dict()


def query_film_by_title(title: str) -> dict:
    return {"query": {"match": {"title": title}}}
