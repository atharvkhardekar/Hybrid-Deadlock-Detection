from cassandra.cluster import Cluster
from collections import defaultdict
import uuid
from datetime import datetime
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Connect to Cassandra
cluster = Cluster(['127.0.0.1'])  # Replace with your Cassandra cluster IP
session = cluster.connect('test')  # Replace with your keyspace name

# Create deadlock_info table (if it doesn't exist already)
session.execute("""
    CREATE TABLE IF NOT EXISTS deadlock_info (
        deadlock_id UUID PRIMARY KEY,
        timestamp TIMESTAMP,
        involved_transactions LIST<UUID>,
        status TEXT
    )
""")

# Load the transaction log from CSV
df = pd.read_csv('transactions.csv')

# Prepare features and labels
X = df[['lock_held', 'lock_requested']]
y = df['deadlock_occurred']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Dependency graph: maps transactions waiting for a lock to transactions holding the lock
dependency_graph = defaultdict(list)

# Build the dependency graph
for i, transaction_id in enumerate(df['transaction_id']):
    if df['lock_requested'][i]:  # If a transaction is requesting a lock
        for j, holder_transaction_id in enumerate(df['transaction_id']):
            if df['lock_held'][j] and i != j:  # Another transaction is holding a lock
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

# Function to simulate transactions and print their state
def simulate_transaction(transaction_id, resource):
    transaction_uuid = uuid.UUID(transaction_id)
    print(f"Transaction {transaction_uuid} starting, requesting resource {resource}")
    print(f"Transaction {transaction_uuid} acquired lock on resource {resource}")
    print(f"Transaction {transaction_uuid} completed and released lock on resource {resource}")
    return transaction_uuid

# Simulating scenarios with 10 resources
resources = [f'resource_{i}' for i in range(1, 11)]

print("\nScenario 1: Transaction 1 acquires Resource 1")
transaction_1 = simulate_transaction('4e9519ef-27c0-4075-bc20-c51383595ec0', resources[0])

print("\nScenario 2: Transaction 2 acquires Resource 2")
transaction_2 = simulate_transaction('acfb8aa7-f77b-424f-b238-ad79aa89146f', resources[1])

print("\nScenario 3: Transaction 3 acquires Resource 3")
transaction_3 = simulate_transaction('bfe357d8-6f53-4b89-8f4d-91842a65c1e8', resources[2])

print("\nScenario 4: Transaction 4 acquires Resource 4")
transaction_4 = simulate_transaction('5a6c865c-51c6-4d84-bbed-07e7d9077b96', resources[3])

print("\nScenario 5: Transaction 5 acquires Resource 5")
transaction_5 = simulate_transaction('2f1f5d4a-05f3-4d4f-b70e-c1e012f7173a', resources[4])

print("\nScenario 6: Transaction 6 acquires Resource 6")
transaction_6 = simulate_transaction('dc0a2b3c-3b62-4bfc-b251-b7fa0a60cc85', resources[5])

print("\nScenario 7: Transaction 7 acquires Resource 7")
transaction_7 = simulate_transaction('cbef16d3-e9bb-45e9-b1d6-c7098a4cb4bc', resources[6])

print("\nScenario 8: Transaction 8 acquires Resource 8")
transaction_8 = simulate_transaction('cb0f7c50-9b25-4ea7-84b7-4d6ed66bcecf', resources[7])

print("\nScenario 9: Transaction 9 acquires Resource 9")
transaction_9 = simulate_transaction('dd57691c-7c98-4e48-b5fc-c73811e98224', resources[8])

print("\nScenario 10: Transaction 10 acquires Resource 10")
transaction_10 = simulate_transaction('ef3a345d-37b7-41a6-a960-b7d41cf45fb3', resources[9])

# Simulating some deadlock scenarios
print("\nScenario 11: Transaction 1 tries to acquire Resource 2 (will wait)")
transaction_1 = simulate_transaction('4e9519ef-27c0-4075-bc20-c51383595ec0', resources[1])

print("\nScenario 12: Transaction 2 tries to acquire Resource 1 (will wait)")
transaction_2 = simulate_transaction('acfb8aa7-f77b-424f-b238-ad79aa89146f', resources[0])

# Predict deadlock using the ML model based on the last transaction
current_features = [[df['lock_held'].iloc[-1], df['lock_requested'].iloc[-1]]]  # Using the last transaction for prediction
predicted_deadlock = model.predict(current_features)

# Handling deadlock
if is_deadlock or predicted_deadlock[0] == 1:
    print("\nDeadlock occurred. Some transactions are waiting for each other's resources.")
    print("Cassandra does not detect or resolve this deadlock. Transactions remain stuck.")
    
    # Convert involved_transactions to UUIDs
    involved_transactions_uuid = [uuid.UUID(tid) for tid in involved_transactions]

    # Insert the deadlock information into the deadlock_info table
    deadlock_id = uuid.uuid4()
    timestamp = datetime.now()

    session.execute("""
        INSERT INTO deadlock_info (deadlock_id, timestamp, involved_transactions, status)
        VALUES (%s, %s, %s, %s)
    """, (deadlock_id, timestamp, involved_transactions_uuid, 'active'))

    print(f"Deadlock information stored with ID {deadlock_id}")
else:
    print("No deadlock detected.")

# Final state of transactions
print("\nFinal state of transactions:")
print(f"Transaction {transaction_1}: State = COMPLETED, Resource = {resources[1]}")
print(f"Transaction {transaction_2}: State = COMPLETED, Resource = {resources[0]}")