from flask import Flask, render_template
import psycopg2
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    records = []
    conn = psycopg2.connect("dbname=work user=admin password=admin host=192.168.1.101 port=5433")
    cur = conn.cursor()
    sql_select_query = """select * from work.some_test"""
    cur.execute(sql_select_query)
    for row in cur:
        records.append(row)
    conn.close()
    df = pd.DataFrame.from_dict(records)
    tables = df.to_html(index=False, classes='mystyle')
    titles = ['id', 'message', 'date']
    text_file = open("frame.html", "w")
    text_file.write(tables)
    text_file.close()
    return render_template('index.html', titles=titles, tables=tables)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
