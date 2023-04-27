import telebot
import psycopg2

bot = telebot.TeleBot('6106479878:AAHmReXNz0RSUoxcolkiJjVu08MTv9jbFds')

delimiter = ', '

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "select messages":
        list_of_rows = []
        conn = psycopg2.connect("dbname=work user=admin password=admin host=192.168.100.101 port=5433")
        cur = conn.cursor()
        sql_select_query = """select message from work.some_test order by id"""
        cur.execute(sql_select_query)
        conn.commit()
        rows = cur.fetchall()
        for i in rows:
            for k in i:
                list_of_rows.append(k)
        rows_str = delimiter.join(map(str, list_of_rows))
        bot.send_message(message.from_user.id, rows_str )
    elif message.text == "add message":
        bot.send_message(message.from_user.id, "what message")
        bot.register_next_step_handler(message, input_message)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

def input_message(message):
        bot.reply_to(message, f" add  {message.text} message to DB")
        mess = message.text
        conn = psycopg2.connect("dbname=work user=admin password=admin host=192.168.100.101 port=5433")
        cur = conn.cursor()
        cur.execute("INSERT INTO work.some_test (message) VALUES (%s)", [mess])
        conn.commit()
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)