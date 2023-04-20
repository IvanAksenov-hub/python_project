from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

@app.route("/")
def index():
    conn = psycopg2.connect("dbname=work user=admin password=admin host=192.168.1.101 port=5433")
    cur = conn.cursor()
    sql_select_query = """select * from work.some_test"""
    records = cur.execute(sql_select_query)
    conn.close()
    return render_template('index.html', records=records)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
