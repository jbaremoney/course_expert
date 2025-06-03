import sqlite3
#from pathlib import Path

db_path = "/Users/z3u5/AdviseLLM/data_cleaning/courseDatabase.db"
connection = sqlite3.connect(db_path)
cursor = connection.cursor()
'''
sql_query = "SELECT * FROM courses_table WHERE code=MATH_442;"

try:
    cursor.execute(sql_query)
    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]  # column names

    # Convert the result into a list of dicts (optional)
    results = [dict(zip(columns, row)) for row in rows]
    connection.close()
    print(results)

except Exception as e:
    connection.close()
    print(f"Error executing SQL: {e}")
'''
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in DB:", tables)

# If you know the table name, show schema
cursor.execute("PRAGMA table_info(courses_table);")
schema = cursor.fetchall()

print("Schema:")
for col in schema:
    print(col)  # (cid, name, type, notnull, dflt_value, pk)
resp= cursor.execute('SELECT description FROM courses_table WHERE code="MATH 442"')
row = cursor.fetchone()

print(row)

connection.close()