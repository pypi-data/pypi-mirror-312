import redis
import rediscluster
from redis.client import PubSub
from rediscluster import RedisCluster, ClusterConnectionPool

from kombu import Connection, Producer, Exchange, Queue, Consumer
from t.unit.transport.virtual.test_base import client

URL = 'rediscluster://:myredis@127.0.0.1:7024'

# connection = rediscluster.RedisCluster(host='127.0.0.1', password='myredis', port=7024)
# pool = ClusterConnectionPool(host='127.0.0.1', password='myredis', port=7024)
# ps = connection.pubsub(connection_pool=pool)
# ps.connection = pool.get_connection('_')
# print(ps.connection)

pool = ClusterConnectionPool(host='127.0.0.1', password='myredis', port=7024)
connection = rediscluster.RedisCluster(connection_pool=pool)
print(connection.get("test"))
ps = connection.pubsub()
print(ps.connection)
connection.close()

# pool = redis.ConnectionPool(host='127.0.0.1', password='12345678', port=6379)
# client = redis.Redis(connection_pool=pool)
# c = PubSub(connection_pool=pool)
# c.connection = client.connection_pool.get_connection('_')
# print(c.connection)
# print(c.connection._sock)
