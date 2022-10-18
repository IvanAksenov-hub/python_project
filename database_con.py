import psycopg2

con = psycopg2.connect(
    database="project",
    user="admin",
    password="admin",
    host="192.168.0.109",
    port="5432"
)

print("Database opened successfully")

cur = con.cursor()
postgres_insert_query = """ insert into scheme_1.users (man,status) values (%s,%s)"""
record_to_insert = ('admin', 'active')
cur.execute(postgres_insert_query,record_to_insert)

con.commit()
print("Record inserted successfully")

con.close()