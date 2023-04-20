from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

def get_db_connection(): 
    conn = psycopg2.connect(
        database="work",
        user="admin",
        password="admin",
        host="192.168.1.101",
        port="5433"
    )

@app.route("/")
def index():
    connection = get_db_connection()
    sql_select_query = """select * from work.some_test"""
    connection.close()
    return render_template('index.html', records=sql_select_query)



if __name__ == "__main__":
    app.run(host='0.0.0.0')
