# Hybrid Deadlock Detection

This Project implements **Hybrid Deadlock Detection** techniques, combining Machine Learning and traditional algorithms with Cassandra integration to analyze and predict deadlocks in transactional systems.This project also gives a comparative analysis of how ML integrated with Traditional methods is give extraordinary results in predicting the potential deadlocks rather than only using a traditional method or just using a ML algorithm.

## Overview

- **Cycle Detection (`cycleDetect.py`)**: Implements graph-based algorithms to detect cycles, which indicate potential deadlocks.
- **ML-Based Approach (`ml.py`)**: Predicts deadlocks using machine learning techniques based on transactional data.
- **Hybrid Approach (`hybrid.py`)**: Combines ML-based predictions with traditional deadlock detection mechanisms to enhance accuracy.
- **Cassandra Integration (`connection.py`)**: Connects to a Cassandra database, sets up a keyspace, and provides integration for transactional data storage and retrieval.

Using the provided `transactions.csv`, the accuracy results are as follows:  
- **Cycle Detection Method**: Outputs results based on graph analysis.
- **ML-Based Method**: 60% accuracy  
- **Hybrid Method**: 80% accuracy  


## Features

- **Deadlock Detection**: 
  - Graph-based cycle detection
  - ML-based prediction
  - Hybrid ML and algorithmic detection

- **Cassandra Integration**:
  - Connect to a local Cassandra instance.
  - Create and use a keyspace named `test` for transactional data.
- **Input Dataset**: Analyze a CSV file containing transactional data.
- **Comparative Results**: Evaluate and compare the accuracy of all approaches.
- **Customizability**: Extendable for additional ML models or detection mechanisms.


## Prerequisites

Ensure you have the following installed:

- Python 3.7+
- Cassandra database (local or remote)
- Required Python libraries (listed in `requirements.txt`)

## Setup

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/atharvkhardekar/Hybrid-Deadlock-Detection.git
   cd Hybrid-Deadlock-Detection

2. **Install Dependencies**

    Use the following command to install the required libraries:

    ```bash
    pip install -r requirements.txt

3. **Install Cassandra Database**

    Download Apache Cassandra and follow the installation steps for your system.
    Start the Cassandra server:

    ```bash
    cassandra -f

4. **Set Up Cassandra Connection**
   
   The connection.py script establishes a connection to Cassandra, creates a test keyspace, and sets it as active. Ensure your local Cassandra instance is running.


## Usage

1. **Run Cassandra Connection (connection.py)**  
   ```bash
   python connection.py

- Connects to Cassandra using the address 127.0.0.1 (default for local installations).
- Creates the test keyspace if it does not exist.
- Outputs a confirmation of connection and keyspace setup.

2. **Run Cycle Detection (cycleDetect.py)**

    ```bash
    python cycleDetect.py

3. **Run ML-Based Deadlock Detection (ml.py)**

    ```bash
    python ml.py

- Loads transactional data from transactions.csv.
- Predicts deadlocks using a machine learning model.
- Displays and logs the accuracy and performance metrics.

4. **Run Hybrid Deadlock Detection (hybrid.py)**
   
   ```bash
    python hybrid.py

- Combines ML predictions with traditional detection mechanisms.
- Outputs more accurate predictions of deadlocks.
- Displays and logs the accuracy and performance metrics.

5. **Compare Results** 
   - All scripts generate accuracy scores and logs for evaluation.
        1. Accuracy of ml.py which uses (Random Forest) is 60% (based on transactions.csv)
        2. Accuracy of hybrid.py which uses (Gradient Boosting + Timestamping) is 80% (based on transactions.csv)  

- Note : You can also use your own Ml models or algorithms with diferent traditional methods.     


## Dataset

- File Name: transactions.csv
- Description: Contains transactional data required for the deadlock detection models.

- **Structure**:
   - Each row represents a transaction.
   - Columns should include the required transactional attributes.

- Note: You can upload your custom transactions.csv to the repository for testing.


## Contributing
Contributions are welcome! To contribute:

- 1. Fork the repository.
- 2. Create a new branch for your feature/bug fix.
- 3. Submit a pull request with a detailed description.

## License
This project is licensed under the MIT License.
