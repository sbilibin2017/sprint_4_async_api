import uuid
from datetime import datetime

import pandas as pd
from utils.logger import logger
from utils.validators import FilmIndexData, GenreWithFilmIndexData, PersonWithFilmIndexData

DEFAULT_NUM = -1.0
DEFAULT_STR = ""
DEFAULT_LIST = []


def build_film_data(
    filmwork_id: uuid.UUID, df: pd.DataFrame, df_fwg: pd.DataFrame, df_fwp: pd.DataFrame
) -> tuple[dict, datetime]:
    """Prepare json data."""

    df["rating"].fillna(DEFAULT_NUM, inplace=True)
    df_sub = df[df["id"] == filmwork_id]
    df_fwg_sub = df_fwg[df_fwg["id"] == filmwork_id]
    df_fwp_sub = df_fwp[df_fwp["id"] == filmwork_id]

    d = {}
    d["id"] = filmwork_id
    d["imdb_rating"] = df_sub["rating"].iloc[0]
    d["genre"] = df_fwg_sub["name"].unique().tolist()
    d["title"] = df_sub["title"].iloc[0] or DEFAULT_STR
    d["description"] = df_sub["description"].iloc[0] or DEFAULT_STR
    subdf_dir = df_fwp_sub[df_fwp_sub["role"] == "director"]
    if len(subdf_dir) > 0:
        d["director"] = subdf_dir["name"].values.tolist()
    else:
        d["director"] = DEFAULT_LIST
    for key in ["actor", "writer"]:
        subdf = df_fwp_sub[df_fwp_sub["role"] == key]
        if len(subdf) > 0:
            d[f"{key}s_names"] = subdf["name"].values.tolist()
            d[f"{key}s"] = subdf[["id", "name"]].to_dict("records")
        else:
            d[f"{key}s_names"] = DEFAULT_LIST
            d[f"{key}s"] = DEFAULT_LIST

    d_validated = FilmIndexData(**d).dict()

    return d_validated, df_sub["updated_at"].iloc[0]


def get_film_info(film):
    return {"film": [{"id": film["id"], "title": film["title"], "imdb_rating": film["imdb_rating"]}]}


def build_genre_data(film: dict, df_fwg: pd.DataFrame) -> tuple[dict, datetime]:
    """Prepare json data."""
    film_info = get_film_info(film)
    genre_list = (
        df_fwg.drop_duplicates(subset=["genre_id"])
        .drop("id", axis=1)
        .rename(columns={"genre_id": "id"})[["id", "name"]]
        .to_dict("records")
    )
    genre_list_validated = []
    for d in genre_list:
        d.update(film_info)
        d_validated = GenreWithFilmIndexData(**d).dict()
        genre_list_validated.append(d_validated)
    return genre_list_validated


def build_person_data(film: dict, df_fwp: pd.DataFrame, role: str) -> tuple[dict, datetime]:
    """Prepare json data."""
    film_info = get_film_info(film)
    person_list = (
        df_fwp[df_fwp["role"] == role]
        .drop_duplicates(subset=["person_id"])
        .drop("id", axis=1)
        .rename(columns={"person_id": "id"})[["id", "name"]]
        .to_dict("records")
    )
    person_list_validated = []
    for d in person_list:
        d.update(film_info)
        d_validated = PersonWithFilmIndexData(**d).dict()
        person_list_validated.append(d_validated)
    return person_list_validated


def update_data(data_genre: list, genres: list) -> None:
    for genre in genres:
        if genre not in data_genre:
            data_genre.append(genre)


def transform(df: pd.DataFrame, df_fwg: pd.DataFrame, df_fwp: pd.DataFrame) -> tuple[list[dict], datetime]:
    """Transforms extracted data."""
    data_film, data_genre, data_actor, data_writer, data_director = [], [], [], [], []
    for filmwork_id in df["id"].values:
        film, updated_at = build_film_data(filmwork_id, df, df_fwg, df_fwp)
        data_film.append(film)
        update_data(data_genre, build_genre_data(film, df_fwg))
        update_data(data_actor, build_person_data(film, df_fwp, "actor"))
        update_data(data_writer, build_person_data(film, df_fwp, "writer"))
        update_data(data_director, build_person_data(film, df_fwp, "director"))
        logger.info(f"\t[TRANSFORM] film:{film}")
    logger.info(f"\t[TRANSFORM] actor:{data_actor[0]}")
    logger.info(f"\t[TRANSFORM] writer:{data_writer[0]}")
    logger.info(f"\t[TRANSFORM] director:{data_director[0]}")
    logger.info(f"\t[TRANSFORM] genre:{data_genre[0]}")
    return data_film, data_genre, data_actor, data_writer, data_director, updated_at
