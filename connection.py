from cassandra.cluster import Cluster

# Connect to the Cassandra database
cluster = Cluster(['127.0.0.1'])  # Replace with 'localhost' or '127.0.0.1'
session = cluster.connect()

# Create and use the keyspace
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS test
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
""")
session.set_keyspace('test')

