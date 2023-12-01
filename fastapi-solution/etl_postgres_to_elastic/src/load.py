from datetime import datetime

import config
import elasticsearch
from elasticsearch import helpers
from utils.logger import logger
from utils.state import State


def collect_actions(es_cur: elasticsearch.client, data: list[dict], index: str) -> list[dict]:
    """Prepare data to adding to elasticsearch index."""
    actions = []
    for row in data:
        _id = row["id"]
        if not (es_cur.exists(index=index, doc_type="_all", id=_id)):
            action = {"_index": index, "_type": "_doc", "_id": _id, "_source": row}
            actions.append(action)
            logger.info(f"\t[LOAD] action:{row}")
    return actions


def update_index(data: list[dict], es_cur: elasticsearch.client, index: str) -> None:
    # TODO
    # replace with bulk update

    for row in data:
        if not (es_cur.exists(index=index, doc_type="_all", id=row["id"])):
            es_cur.index(index=index, doc_type="_doc", id=row["id"], body=row)
        else:
            es_cur.update(
                index=index,
                id=row["id"],
                body={
                    "script": {
                        "source": "ctx._source.film.addAll(params.film)",
                        "lang": "painless",
                        "params": {"film": row["film"]},
                    }
                },
            )


def load(
    data_film: list[dict],
    data_genre: list[dict],
    data_actor: list[dict],
    data_writer: list[dict],
    data_director: list[dict],
    es_cur: elasticsearch.client,
    state: State,
    updated_at: datetime,
) -> None:
    """Loads transformed data to elasticsearch index."""
    helpers.bulk(es_cur, collect_actions(es_cur, data_film, config.ELASTIC_MOVIES_INDEX))
    update_index(data_genre, es_cur, config.ELASTIC_GENRES_INDEX)
    update_index(data_actor, es_cur, config.ELASTIC_ACTORS_INDEX)
    update_index(data_writer, es_cur, config.ELASTIC_WRITERS_INDEX)
    update_index(data_director, es_cur, config.ELASTIC_DIRECTORS_INDEX)
    new_updated_at = updated_at
    state.set_state(config.REDIS_STATE, new_updated_at)
    logger.info(f"\t[LOAD] new_updated_at:{new_updated_at}")
