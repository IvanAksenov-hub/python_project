from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    conn = psycopg2.connect("dbname=work user=admin password=admin host=192.168.1.101 port=5433")
    cur = conn.cursor()
    message_by_id = [('some text')]
    message_id = ''
    if request.method == 'POST':
        try:
            if request.form['action'] == 'insert_form':
                message = request.form['message']
                cur.execute("INSERT INTO work.some_test (message) VALUES (%s)", [message])
                conn.commit()
            elif request.form['action'] == 'id_form':
                message_id = request.form['message_id']
                cur.execute("SELECT message FROM work.some_test where id = (%s)", [message_id])
                message_by_id = cur.fetchone()
                conn.commit()
            elif request.form['action'] == 'update_form':
                message_id = int(request.form['message_id'])
                update_message = str(request.form['update_message'])
                if 'update_button' in request.form:
                    cur.execute("UPDATE work.some_test SET message = %s WHERE id = %s", (update_message, message_id))
                elif 'delete_button' in request.form:
                    cur.execute("DELETE FROM work.some_test WHERE id = %s", (message_id,))
                conn.commit()
        except Exception as e:
            print(e)
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
    return render_template('index.html', table_html=table_html, message_by_id=message_by_id, message_id=message_id)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
