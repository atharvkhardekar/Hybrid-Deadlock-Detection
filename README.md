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

- **If this installation and setup of cassandra doesn't works, you can alternatively use the below method also.**

3. **Install Cassandra Database :**
    - To set up the Cassandra database, you can use Docker for a streamlined installation. Follow the steps below:
    
     ### Using Docker to Install Cassandra
       <!-- 1. Ensure you have Docker installed on your system. If not, download and install it from [Docker's official site](https://www.docker.com/). -->
       
       2. Pull the official Cassandra Docker image:

           ```bash
           docker pull cassandra:latest
     
       3. Start a Cassandra container:
      
           ```bash
           docker run --name cassandra-container -d -p 9042:9042 cassandra

          - This command:

             1.  Names the container cassandra-container.
             2. Exposes the default Cassandra port 9042 for client connections.
             3. Runs Cassandra in detached mode (-d).

       4. Verify that the Cassandra container is running:
             
           ```bash
           docker ps

          - Or you can directly check it from your Docker Desktop.

       5. Connecting to Cassandra with (connection.py)

          1. Ensure your Cassandra Docker container is running.
          2. The connection.py script is preconfigured to connect to Cassandra on 127.0.0.1. This is the default host when using Docker with port mapping (-p 9042:9042).
          
          3. Run the script to set up the connection:

              ```bash
              python connection.py

             - This script will:

                1. Connect to Cassandra on 127.0.0.1.
                2. Create a test keyspace if it doesn't already exist.
                3. Set the test keyspace as active. 
     
       6. Upon successful execution, the script will confirm the connection and keyspace setup.      
  

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

6. **(Additionally) To check the Cassandra Container and logs in the Database**
    1. Enter the Cassandra Container: Use the following command to access the Cassandra container's shell:

       ```bash
       docker exec -it cassandra-container cqlsh

       - cassandra-container is the name of the container. Replace it with your container's name if it's different.
       - cqlsh is the Cassandra Query Language Shell.

    2. Switch to the Keyspace: Once inside cqlsh, set the keyspace you created using connection.py. For example, if your keyspace is test:

       ```sql
       USE test;

    3. List All Tables: Run the following command to display all tables in the keyspace:

       ```sql
       DESCRIBE TABLES;

    4. To check the entries in the table.

       ```sql
       SELECT * FROM table_name;

    5. According to these Detection files there are two tables in Cassandra Container:
       1. cycleDetect (used by the cycleDetect.py)
       2. deadlock_info (used by ml.py and hybrid.py)  

## Dataset

 - File Name: transactions.csv
 - Description: Contains transactional data required for the deadlock detection models.

 - **Structure**:
    - Each row represents a transaction.
    - Columns should include the required transactional attributes.

 - Note: You can upload your custom transactions.csv to the repository for testing.


## Contributing
 - Contributions are welcome! To contribute:

    - 1. Fork the repository.
    - 2. Create a new branch for your feature/bug fix.
    - 3. Submit a pull request with a detailed description.

## License
 - This project is licensed under the MIT License.
