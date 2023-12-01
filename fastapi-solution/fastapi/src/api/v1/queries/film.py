from core.config import Settings

CONFIG = Settings().dict()


def query_films() -> dict:
    return {
        "size": CONFIG["ELASTIC_SCROLL_SIZE"],
        "query": {"match_all": {}},
        "sort": [{"imdb_rating": {"order": "desc"}}],
    }


def query_films_by_genre(genres: list[str]) -> dict:
    return {
        "size": CONFIG["ELASTIC_SCROLL_SIZE"],
        "query": {"terms": {"genre": genres}},
        "sort": [{"imdb_rating": {"order": "desc"}}],
    }
