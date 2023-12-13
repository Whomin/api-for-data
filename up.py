import pyodbc
import csv

# Set the connection details
server = '10.10.70.165'
database = 'TLT'
username = 'sa'
password = 'P@ssw0rd'
driver = '{SQL Server Native Client 11.0}' # change this if you are using a different driver

# Create a connection string
conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

# Connect to the database
conn = pyodbc.connect(conn_str)

# Create a cursor object
cur = conn.cursor()

# Open the CSV file and insert data into the table
with open('dataforapi.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # get the header row
    columns = ', '.join(f'[{col}]' for col in header)
    placeholders = ', '.join(['?'] * len(header))  # create placeholders for the values
    for row in reader:
        values = [row[header.index(col)] for col in header]  # map the values to the correct columns
        query = f"INSERT INTO dbo.tlt_security_dashboard ({columns}) VALUES ({placeholders})"
        cur.execute(query, values)

# Commit the changes and close the cursor and database connection
conn.commit()
cur.close()
conn.close()