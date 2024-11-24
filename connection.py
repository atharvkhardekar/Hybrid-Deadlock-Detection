from cassandra.cluster import Cluster

# Connect to the Cassandra database
cluster = Cluster(['127.0.0.1'])  # Replace with 'localhost' or '127.0.0.1'
session = cluster.connect()
print("Connection established successfully!")

# Create and use the keyspace
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS test
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
""")
if(session.set_keyspace('test')) :
 print("Keyspace 'test' is now active.")
else :
 print("An error occurred while setting up the keyspace:")


