import psycopg2
import os
from dotenv import load_dotenv



load_dotenv()


def runSQLCommand(command):
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
        return ["Ошибка подключения"]

    # Закрываем курсор и соединение с базой данных
    if connection:
        cursor.close()
        connection.close()
    return records



qwe = runSQLCommand("Select * from mail")
print(type (qwe[0]))
ee = "\n".join([str(item) for item in qwe])

print(ee)
