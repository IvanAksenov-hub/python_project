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
#postgres_insert_query = """ insert into scheme_1.users (man,status) values (%s,%s)"""
#record_to_insert = ('show', 'diactivated')
#cur.execute(postgres_insert_query,record_to_insert)
#con.commit()

sql_select_query = """select * from scheme_1.users"""
cur.execute(sql_select_query)
for row in cur:
    print(row)



print("Record inserted successfully")

con.close()