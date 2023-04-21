from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

@app.route("/")
def index():
    conn = psycopg2.connect("dbname=work user=admin password=admin host=192.168.1.101 port=5433")
    cur = conn.cursor()
    sql_select_query = """select * from work.some_test order by id"""
    cur.execute(sql_select_query)
    rows = cur.fetchall()
    num_cols = len(cur.description)
    table_html = "<table border="'1'" class="'tablestyle'" class="'dataframe'">"
    table_html += "<thead><tr>"
    for col in cur.description:
        table_html += "<th>" + col.name + "</th>"
    table_html += "</tr></thead>"
    table_html += "<tbody>"
    for row in rows:
        table_html += "<tr>"
        for col_index in range(num_cols):
            table_html += "<td>" + str(row[col_index]) + "</td>"
        table_html += "</tr>"
    table_html += "</tbody></table>"
    return render_template('index.html', table_html=table_html)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
