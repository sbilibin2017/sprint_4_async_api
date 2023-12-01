from pathlib import Path

from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parent.parent.parent


api_config = dotenv_values(BASE_DIR / "env/api/.env.dev")
redis_config = dotenv_values(BASE_DIR / "env/redis/.env.dev")
elastic_config = dotenv_values(BASE_DIR / "env/elasticsearch/.env.dev")
docker_config = dotenv_values(BASE_DIR / "env/docker/.env.dev")
postgres_config = dotenv_values(BASE_DIR / "env/postgres/.env.dev")

PROJECT_NAME = api_config["PROJECT_NAME"]

ELASTIC_HOST = docker_config["ELASTIC_HOST"]
ELASTIC_PORT = elastic_config["ELASTIC_PORT"]
ELASTIC_URL = f"http://{ELASTIC_HOST}:{ELASTIC_PORT}"
ELASTIC_MOVIES_MAPPING_FILENAME = elastic_config["ELASTIC_MOVIES_MAPPING_FILENAME"]
ELASTIC_OTHERS_MAPPING_FILENAME = elastic_config["ELASTIC_OTHERS_MAPPING_FILENAME"]
ELASTIC_MOVIES_INDEX = elastic_config["ELASTIC_MOVIES_INDEX"]
ELASTIC_GENRES_INDEX = elastic_config["ELASTIC_GENRES_INDEX"]
ELASTIC_ACTORS_INDEX = elastic_config["ELASTIC_ACTORS_INDEX"]
ELASTIC_WRITERS_INDEX = elastic_config["ELASTIC_WRITERS_INDEX"]
ELASTIC_DIRECTORS_INDEX = elastic_config["ELASTIC_DIRECTORS_INDEX"]

POSTGRES_DB = postgres_config["DB_NAME"]
POSTGRES_USER = postgres_config["DB_USER"]
POSTGRES_PASSWORD = postgres_config["POSTGRES_PASSWORD"]
POSTGRES_HOST = docker_config["POSTGRES_HOST"]
POSTGRES_PORT = postgres_config["POSTGRES_PORT"]
POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
POSTGRES_CHUNK_SIZE = int(postgres_config["POSTGRES_CHUNK_SIZE"])

# redis
REDIS_HOST = docker_config["REDIS_HOST"]
REDIS_PORT = redis_config["REDIS_PORT"]
REDIS_STATE = redis_config["REDIS_STATE"]

# others
SLEEP = 5
