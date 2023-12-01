import orjson
from utils.mixin import DataMixin
from utils.orjson import orjson_dumps


class Writer(DataMixin):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
