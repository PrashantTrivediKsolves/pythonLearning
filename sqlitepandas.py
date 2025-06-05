# import sqlite3
# import pandas as pd

# # 1. Create a connection (in-memory DB for testing)
# conn = sqlite3.connect(":memory:")

# # 2. Create a table
# conn.execute("""
# CREATE TABLE users (
#     id INTEGER PRIMARY KEY,
#     name TEXT,
#     age INTEGER
# )
# """)

# # 3. Insert data
# conn.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
# conn.execute("INSERT INTO users (name, age) VALUES ('Bob', 25)")
# conn.commit()

# # 4. Query the table using SQL
# result = pd.read_sql_query("SELECT * FROM users", conn)
# print(result)



# Step 2: Using SQLAlchemy (recommended for real databases)


from sqlalchemy import create_engine
import pandas as pd

# Create an engine — here using SQLite file-based DB
engine = create_engine('sqlite:///mydatabase.db')

# Create a table with pandas
df = pd.DataFrame({
    'name': ['Charlie', 'David'],
    'age': [35, 28]
})
df.to_sql('employees', con=engine, if_exists='replace', index=False)

# Query with SQL
query_result = pd.read_sql_query("SELECT * FROM employees", engine)
print(query_result)



# Step 3: Reading SQL into pandas (pd.read_sql_query())

query = "SELECT name, age FROM employees WHERE age > 30"
df_filtered = pd.read_sql_query(query, engine)

print(query)


