import os

import redis

r_cache = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379, db=int(os.getenv('REDIS_DB')))
