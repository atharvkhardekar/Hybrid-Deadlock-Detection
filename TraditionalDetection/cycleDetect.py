from cassandra.cluster import Cluster
from collections import defaultdict
import uuid
from datetime import datetime
import pandas as pd

# Connect to Cassandra
cluster = Cluster(['127.0.0.1'])  # Replace with your Cassandra cluster IP
session = cluster.connect('test')  # Replace with your keyspace name

# Create cycledetect table (if it doesn't exist already)
session.execute("""
    CREATE TABLE IF NOT EXISTS cycledetect (
        deadlock_id UUID PRIMARY KEY,
        timestamp TIMESTAMP,
        involved_transactions LIST<UUID>,
        status TEXT
    )
""")

# Load the transaction log from a CSV file
csv_file = 'transactions.csv'  # Update this with the correct path to your CSV file
data = pd.read_csv(csv_file)

# Convert data to dictionary format for processing
transaction_data = {
    'transaction_id': data['transaction_id'].tolist(),
    'timestamp': data['timestamp'].tolist(),
    'lock_held': data['lock_held'].astype(bool).tolist(),
    'lock_requested': data['lock_requested'].astype(bool).tolist()
}

# Dependency graph: maps transactions waiting for a lock to transactions holding the lock
dependency_graph = defaultdict(list)

# Build the dependency graph
for i, transaction_id in enumerate(transaction_data['transaction_id']):
    if transaction_data['lock_requested'][i]:  # If a transaction is requesting a lock
        for j, holder_transaction_id in enumerate(transaction_data['transaction_id']):
            if transaction_data['lock_held'][j] and i != j:  # Another transaction is holding a lock
                dependency_graph[transaction_id].append(holder_transaction_id)

# Function to detect cycles in the dependency graph using DFS
def detect_cycle(graph):
    visited = set()  # Track visited nodes
    stack = set()  # Track nodes in the current recursion stack (for cycle detection)
    involved_transactions = []

    def dfs(transaction_id):
        if transaction_id in stack:  # Cycle detected
            return True
        if transaction_id in visited:
            return False

        visited.add(transaction_id)
        stack.add(transaction_id)
        involved_transactions.append(transaction_id)

        # Visit all dependent transactions (those holding the locks this transaction is waiting for)
        for dependent_id in graph[transaction_id]:
            if dfs(dependent_id):
                return True

        stack.remove(transaction_id)
        return False

    # Check for cycles in all components of the graph
    for transaction_id in graph:
        if dfs(transaction_id):
            return True, involved_transactions
    return False, []

# Detecting deadlock and storing information in Cassandra
is_deadlock, involved_transactions = detect_cycle(dependency_graph)

if is_deadlock:
    print("Deadlock detected!")
    
    # Convert involved_transactions to UUIDs
    involved_transactions_uuid = [uuid.UUID(tid) for tid in involved_transactions]

    # Insert the deadlock information into the cycledetect table
    deadlock_id = uuid.uuid4()
    timestamp = datetime.now()

    session.execute("""
        INSERT INTO cycledetect (deadlock_id, timestamp, involved_transactions, status)
        VALUES (%s, %s, %s, %s)
    """, (deadlock_id, timestamp, involved_transactions_uuid, 'active'))

    print(f"Deadlock information stored with ID {deadlock_id}")
else:
    print("No deadlock detected.")