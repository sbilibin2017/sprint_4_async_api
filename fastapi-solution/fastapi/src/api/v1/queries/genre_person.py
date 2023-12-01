from core.config import Settings

CONFIG = Settings().dict()


def query_genre_person() -> dict:
    return {
        "size": CONFIG["ELASTIC_SCROLL_SIZE"],
        "query": {"match_all": {}},
        "sort": [{"film.imdb_rating": {"order": "desc"}}],
    }
