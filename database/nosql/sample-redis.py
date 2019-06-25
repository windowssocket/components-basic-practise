from redis import StrictRedis, ConnectionPool

pool = ConnectionPool(host='localhost', port=6379, db=0, password=None)
redis = StrictRedis(connection_pool=pool)
redis.set('name', 'Bob')
redis.set('count', 0)
redis.incr('count')
redis.incr('count')
redis.rpush(1, [1,2],[3,4])
print(redis.lrange(1, 0, 2))
redis.rpush('list', 1, 2, 3)
print(redis.get('count'))
print(redis.lrange('list', 0, 5))
print(redis.llen('list'))

redis.sadd('set', "flight")
redis.sadd('set', "flight")
print(redis.smembers('set'))

redis.hset("userid:100", "name", "smith")
redis.hset("userid:100", "name", "smiths")
redis.hset("userid:100", "userid", 200)
print(redis.hmget("userid:100", "name"))