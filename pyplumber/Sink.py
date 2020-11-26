__all__ = ["Sink"]

import dill
import redis
import struct
import pickle
from typing import Union
from pyplumber.exceptions import SerializationError, DeserializationError


class Sink(redis.Redis):
    def __init__(self, *args, **kwargs) -> None:
        super(Sink, self).__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return "<PyPlumber Sink<pool={}>>".format(self.connection_pool)

    def __str__(self) -> str:
        return self.__repr__()

    def _serialize(self, o: object) -> object:
        if isinstance(o, (str, bytes, int, float)):
            return o
        else:
            try:
                return pickle.dumps(o)
            except:
                try:
                    return dill.dumps(o)
                except:
                    raise SerializationError("Failed to serialize object {}".format(o))

    def _deserialize(self, e: Union[str, int, float, bytes]) -> object:
        if isinstance(e, (str, int, float)):
            return e
        else:
            try:
                return e.decode()
            except UnicodeDecodeError:
                try:
                    return pickle.loads(e)
                except:
                    try:
                        return dill.loads(e)
                    except:
                        raise DeserializationError("Failed to deserialize {}".format(e))

    def set(self, key, value, *args, **kwargs):
        return super(Sink, self).set(
            name=key, value=self._serialize(value), *args, **kwargs
        )

    def get(self, key, *args, **kwargs):
        return self._deserialize(super(Sink, self).get(name=key, *args, **kwargs))