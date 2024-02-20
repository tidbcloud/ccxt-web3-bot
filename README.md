# Introduction
Welcome to the Web3 Data Importer Tool, a utility designed to facilitate the importing of a Web3 demo data into your database. This tool streamlines the process of setting up your development and testing environments by populating your database with necessary data. Follow the instructions below to set up and use this tool efficiently.

# Getting Started

## Step 1: Install Dependencies
To install all required dependencies listed in the `requirements.txt` file, run the following command in your terminal:
```
python3 -m pip install -r requirements.txt
```

## Step 2: Configure Database Connection
Open the config.json file in a text editor of your choice. For instance, to use the vi editor, enter:
```
vi config.json
```
Fill in your database connection information in the designated fields and save the changes. Replace the placeholders with your actual connection details:
```
{
    "db_host": "<TiDB_cluster_host>",
    "db_port": 4000,
    "db_user": "<TiDB_cluster_user>",
    "db_password": "<TiDB_cluster_password>"
}
```
## Step 3: Run the Importer
To start the data import process, execute the script by running the following command in a terminal window:
```bash
python3 ./main.py
```
# Usage
Once the setup is complete, the tool will begin importing data into your specified database. Ensure that your database service is operational and accessible throughout this process.

You can see the test data in your database as below:
```
mysql> select * from crypto_demo.crypto_trends limit 1\G
*************************** 1. row ***************************
         id: 1
     crypto: BTC/USDT:USDT
       time: 2023-11-02 00:00:00
 open_price: 35437.5
 high_price: 35999.9
  low_price: 34300
close_price: 34940.1
1 row in set (0.25 sec)
```
