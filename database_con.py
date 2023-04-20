import psycopg2

con = psycopg2.connect(
    database="work",
    user="admin",
    password="admin",
    host="192.168.1.101",
    port="5433"
)

print("Database opened successfully")

cur = con.cursor()
#postgres_insert_query = """ insert into scheme_1.users (man,status) values (%s,%s)"""
#record_to_insert = ('show', 'diactivated')
#cur.execute(postgres_insert_query,record_to_insert)
#con.commit()

sql_select_query = """select * from work.some_test"""
cur.execute(sql_select_query)
for row in cur:
    print(row)



print("successfully")

con.close()