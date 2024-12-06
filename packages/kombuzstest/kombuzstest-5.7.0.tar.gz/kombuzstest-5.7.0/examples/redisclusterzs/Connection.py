from collections import defaultdict


class Client:
    def __init__(self, *args, **kwargs):
        self.sets = defaultdict(set)

    def sadd(self, key, member):
        self.sets[key].add(member)

    def smembers(self, key):
        return self.sets.get(key, set())

    def srem(self, key):
        self.sets.pop(key, None)


class ClusterConnection:
    def __init__(self, *args, **kwargs):
        super(ClusterConnection, self).__init__(*args, **kwargs)


class ClusterConnectionPool:
    def __init__(self, startup_nodes=None, **connection_kwargs):
        if startup_nodes is None:
            if 'port' in connection_kwargs and 'host' in connection_kwargs:
                startup_nodes = [{
                    'host': connection_kwargs.pop('host'),
                    'port': str(connection_kwargs.pop('port')),
                }]
        self.nodes = NodeManager(startup_nodes)
        self.nodes.initialize()


class NodeManager:
    REDIS_CLUSTER_HASH_SLOTS = 4  # 16384

    def __init__(self, startup_nodes=None, **connection_kwargs):
        self.nodes = {}
        self.slots = {}
        self.startup_nodes = startup_nodes

    def initialize(self):
        cluster_slots = [[0, 1, ['127.0.0.1', 7021, 'b75a1c22edbfbfcf1f86482cd450ab4be54b3143', []],
                          ['127.0.0.1', 7023, '23d899702115e558e2dfd663b8c7c63fd817b7dd', []]],
                         [2, 3, ['127.0.0.1', 7022, 'b5ace1afdd06e07196b92c56d104285b5a325535', []],
                          ['127.0.0.1', 7024, '8f30df96ee4b79704985b87a95ec6d070e1d7004', []]]]
        self.slots = {0: [{'host': '127.0.0.1', 'name': '127.0.0.1:7021', 'port': 7021, 'server_type': 'master'},
                          {'host': '127.0.0.1', 'name': '127.0.0.1:7023', 'port': 7023, 'server_type': 'slave'}],
                      1: [{'host': '127.0.0.1', 'name': '127.0.0.1:7021', 'port': 7021, 'server_type': 'master'},
                          {'host': '127.0.0.1', 'name': '127.0.0.1:7023', 'port': 7023, 'server_type': 'slave'}],
                      2: [{'host': '127.0.0.1', 'name': '127.0.0.1:7022', 'port': 7022, 'server_type': 'master'},
                          {'host': '127.0.0.1', 'name': '127.0.0.1:7024', 'port': 7024, 'server_type': 'slave'}],
                      3: [{'host': '127.0.0.1', 'name': '127.0.0.1:7022', 'port': 7022, 'server_type': 'master'},
                          {'host': '127.0.0.1', 'name': '127.0.0.1:7024', 'port': 7024, 'server_type': 'slave'}]}
        self.nodes = {
            '127.0.0.1:7021': {'host': '127.0.0.1', 'name': '127.0.0.1:7021', 'port': 7021, 'server_type': 'master'},
            '127.0.0.1:7022': {'host': '127.0.0.1', 'name': '127.0.0.1:7022', 'port': 7022, 'server_type': 'master'},
            '127.0.0.1:7023': {'host': '127.0.0.1', 'name': '127.0.0.1:7023', 'port': 7023, 'server_type': 'slave'},
            '127.0.0.1:7024': {'host': '127.0.0.1', 'name': '127.0.0.1:7024', 'port': 7024, 'server_type': 'slave'}}


class RedisCluster(Client):
    def __init__(self, **kwargs):
        self.connection_pool = kwargs.pop('connection_pool')
        super().__init__(**kwargs)

    def pipeline(self):
        return ClusterPipeline(self.connection_pool)


class ClusterPipeline(RedisCluster):

    def __init__(self, connection_pool):
        self.connection_pool = connection_pool

    def __repr__(self):
        return "{0}".format(type(self).__name__)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass


startup_nodes = [{"host": "127.0.0.1", "port": 7024}]
pool = ClusterConnectionPool(startup_nodes=startup_nodes, password='myredis', skip_full_coverage_check=True)
r = RedisCluster(connection_pool=pool)
r.sadd("name", "test")
print(r.smembers("name"))

r.pubsub
