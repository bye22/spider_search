# coding: utf-8
import redis

def get_redis():
    redis_conf = {
        'host': '127.0.0.1',
        'port': 6379,
	'password': 123456,
        'db': 0
    }
    pool = redis.ConnectionPool(host=redis_conf['host'], port=redis_conf['port'], password=redis_conf['password'], db=redis_conf['db'])
    return redis.StrictRedis(connection_pool=pool)

REDIS = get_redis()

