from sqlalchemy import create_engine, text

engine = create_engine("postgresql://sa:sa@localhost:35432/MinimalVDB")
# Create a connection
with engine.connect() as connection:
    # Use `text` for raw SQL queries
    result = connection.execute(text("SELECT * FROM kube1.deployment"))

    # Iterate through results
    for row in result:
        print(row)

    query = text("""
            SELECT Name
            FROM SYS.Tables
            WHERE SchemaName = :schema
            """)
    result = connection.execute(query, {"schema": "kube1" or "public"})
    for row in result:
        print(row)

    query = text("""
                SELECT Name, DataType, (CASE WHEN NullType = 'Nullable' THEN true ELSE false END) as nullable
                FROM SYS.COLUMNS 
                WHERE TableName = :table_name AND SchemaName = :schema
                """)
    result = connection.execute(query, {"schema": "kube1" or "public", "table_name": "deployment"})
    for row in result:
        print(row)