"""
Python script for testing database connection and initialization.

This script establishes a connection to a MySQL database using configuration
values provided in the 'config' module. It reads an SQL script to create tables
and executes the script. After initialization, it executes a SELECT query to
fetch all rows from the 'recipes' table and prints the results.

Developer: WangPeifeng
Date: 2024-05-28
"""
import pymysql  
import config  

# Establish a connection to the MySQL database using values from the configuration
connection = pymysql.connect(
    host=config.Config.DB_HOST,
    user=config.Config.DB_USERNAME,
    password=config.Config.DB_PASSWORD,
    database=config.Config.DB_NAME,
)

cursor = connection.cursor()  

try:
    # Read and execute the SQL script to create tables
    with open('./mysql_db/create.sql', 'r') as file:
        sql_script = file.read()

    sql_commands = sql_script.split(';')  
    for command in sql_commands:
        if command.strip():  
            cursor.execute(command)

    connection.commit()  
finally:
    pass  

# Execute a SELECT query to fetch all rows from the 'recipes' table
cursor.execute("SELECT * FROM recipes")
results = cursor.fetchall()  # Fetch all rows returned by the query

for row in results:
    print(row)  

cursor.close()  
connection.close()  
