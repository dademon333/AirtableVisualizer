import redis

from tokens import Tokens


def get_redis_cursor():
    return redis.Redis(host=Tokens.REDIS_HOST, port=6379, decode_responses=True, db=0)
