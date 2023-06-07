from flask import Flask, render_template, request, Response
from prometheus_flask_exporter import PrometheusMetrics
import psycopg2
from loguru import logger
from prometheus_client import Counter
import io

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Создание счетчика Prometheus
log_counter = Counter('logs_total', 'Total number of logs')

# Буфер для хранения логов
log_buffer = io.StringIO()

logger.add(log_buffer.write)
@app.route('/log')
def view_logs():
    logs = log_buffer.getvalue()
    return Response(logs, mimetype='text/plain')

@app.route("/", methods=['GET', 'POST'])
def index():
    conn = psycopg2.connect("dbname=work user=admin password=admin host=192.168.100.101 port=5433")
    cur = conn.cursor()
    message_by_id = [('some text')]
    message_id = ''
    if request.method == 'POST':
        try:
            if request.form['action'] == 'insert_form':
                message = request.form['message']
                cur.execute("INSERT INTO work.some_test (message) VALUES (%s)", [message])
                conn.commit()
                logger.info("insert in table work.some_test - " + str(message))
            elif request.form['action'] == 'id_form':
                message_id = request.form['message_id']
                cur.execute("SELECT message FROM work.some_test where id = (%s)", [message_id])
                message_by_id = cur.fetchone()
                conn.commit()
                logger.info("request message from table work.some_test where id =  " + str(message_id))
            elif request.form['action'] == 'update_form':
                message_id = int(request.form['message_id'])
                update_message = str(request.form['update_message'])
                if 'update_button' in request.form:
                    cur.execute("UPDATE work.some_test SET message = %s WHERE id = %s", (update_message, message_id))
                    logger.info("update message from table work.some_test where id =  " + str(message_id))
                elif 'delete_button' in request.form:
                    cur.execute("DELETE FROM work.some_test WHERE id = %s", (message_id,))
                    logger.info("delete message from table work.some_test where id =  " + str(message_id))
                conn.commit()
        except Exception as e:
            print(e)
    sql_select_query = """select * from work.some_test order by id"""
    cur.execute(sql_select_query)
    rows = cur.fetchall()
    num_cols = len(cur.description)
    table_html = "<table border="'1'" class="'tablestyle'" class="'dataframe'">"
    table_html += "<thead><tr>"
    # динамически создаваемая таблица для результата
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
