from examples.redisclusterzs.Connection import ClusterConnectionPool

startup_nodes = [{"host": "127.0.0.1", "port": 7024}]
pool = ClusterConnectionPool(startup_nodes=startup_nodes, password='myredis', skip_full_coverage_check=True)
r = RedisCluster(connection_pool=pool)
r.set("name", "test")
print(r.get("name"))
