import os
from telegram import Update
import psycopg2
from telegram.ext import CallbackContext, ConversationHandler


def runSQLSelect(command):
    try:

        connection = psycopg2.connect(
            host=os.getenv('RM_HOST'),  # IP-адрес или доменное имя удалённого сервера
            database=os.getenv('DB_DATABASE'),  # Имя базы данных
            user=os.getenv('DB_USER'),  # Имя пользователя PostgreSQL
            password=os.getenv('DB_PASSWORD'),  # Пароль
            port=os.getenv('DB_PORT')  # Порт PostgreSQL, по умолчанию 5432
        )
        cursor = connection.cursor()
        cursor.execute(command)
        records = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при подключении к PostgreSQL", error)
        return "Ошибка подключения"

    # Закрываем курсор и соединение с базой данных
    if connection:
        cursor.close()
        connection.close()

    data = ""
    for i, record in enumerate(records):
        data = data + f"{i+1}. {record[1]}\n"
    return data


def runSQLInsert(command, data):
    try:

        connection = psycopg2.connect(
            host=os.getenv('RM_HOST'),
            database=os.getenv('DB_DATABASE'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT')
        )
        cursor = connection.cursor()
        cursor.executemany(command, data)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при подключении к PostgreSQL", error)
        return False

    # Закрываем курсор и соединение с базой данных
    if connection:
        cursor.close()
        connection.close()
    return True



def writeData(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    callback_data = query.data

    data = context.user_data.get(callback_data, [])
    if data:
        if callback_data == "phone": sqlquery = f"insert into phone (phone_number) values (%s);"
        elif callback_data == "email": sqlquery = f"insert into mail (email) values (%s);"
        res = [[numb] for numb in data]
        stdout = runSQLInsert(sqlquery, res)
        if stdout:
            query.edit_message_text(text="Данные успешно записаны")
        else:
            query.edit_message_text(text="Данные не записаны. Ошибка.")
    else:
        query.edit_message_text(text="Данные не найдены")

    context.user_data.clear()
    return ConversationHandler.END


def getEmailsCommand(update: Update, context):
    message = runSQLSelect("select * from mail")
    update.message.reply_text(message)


def getPhoneNumbersCommand(update: Update, context):
    message = runSQLSelect("select * from phone")
    update.message.reply_text(message)