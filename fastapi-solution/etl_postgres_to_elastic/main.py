import time

import config
from src.extract import extract
from src.load import load
from src.transform import transform
from utils.db_connections import close_connections, get_min_max_state, setup_connections
from utils.logger import logger


def main():
    # setting connections to
    #   1. postgres
    #   2. elasticsearch
    #   3. redis
    # getting current state of etl
    postgres_cur, es_cur, redis_conn, state = setup_connections()
    # min and max dates from postgres
    min_state, max_state = get_min_max_state(postgres_cur)
    # getting current state
    current_state = state.get_state("updated_at")
    try:
        # setting state if not defiend
        if current_state is None:
            state.set_state(config.REDIS_STATE, max_state)
            current_state = state.get_state(config.REDIS_STATE)
            logger.info("Index was created ...")
            return current_state, min_state
        # run etl if elasticsearch index is not updated
        elif current_state != min_state:
            # extract filmwork, persons for filmwork, genres for filmwork
            # convert to pd.DataFrame
            df, df_fwg, df_fwp = extract(postgres_cur, current_state)
            # if extraction executed unsuccessfully
            if df is None:
                logger.info("Index cant be updated ...")
                return current_state, min_state
            # if its ok
            else:
                data_film, data_genre, data_actor, data_writer, data_director, updated_at = transform(
                    df, df_fwg, df_fwp
                )
                load(data_film, data_genre, data_actor, data_writer, data_director, es_cur, state, updated_at)
                logger.info("Index was updated ...")
                return current_state, min_state
        # exit if elasticsearch index is updated
        else:
            logger.info("Index is up to date ...")
            return current_state, min_state
    except Exception as error:
        logger.error(error)
        return current_state, min_state
    # close postgres connection
    finally:
        close_connections(postgres_cur, es_cur)
        logger.info("Closing postgres connection ...")
        return current_state, min_state


if __name__ == "__main__":
    ITER = 1
    while True:
        current_state, min_state = main()
        logger.info(f"ITERATION {ITER}: current_state={current_state}, min_state={min_state}")
        ITER += 1
        time.sleep(config.SLEEP)
