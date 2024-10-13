import os
from telegram import Update
import paramiko
from telegram.ext import ConversationHandler, CallbackContext



def runCommand(command):
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password, port=port)
        if command[0:4] == "sudo":
            stdin, stdout, stderr = client.exec_command(command, get_pty=True)
            stdin.write(password + '\n')
            stdin.flush()
        else:
            stdin, stdout, stderr = client.exec_command(command)
        data = stdout.read().decode() + stderr.read().decode()

        #data = stdout.read() + stderr.read()
        client.close()
    except:
        print("Неудачное соединение")
        return "Не удалось выполнить запрос"

    return str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]


def getAptList(update: Update, context):
    user_input = update.message.text  # Получаем текст, содержащий(или нет) номера телефонов
    if user_input == "all":
        message = runCommand('apt list | head')
    else:
        message = runCommand(f'apt list | grep \"{user_input}\" | tail')
    update.message.reply_text(message)
    return ConversationHandler.END


def getAptListCommand(update: Update, context):
    update.message.reply_text("Введите название пакета, о котором нужна информация. Или введите all")
    return "getStr"


def getUnameCommand(update: Update, context):
    message = runCommand('uname -a')
    update.message.reply_text(message)


def getUptimeCommand(update: Update, context):
    message = runCommand('uptime')
    update.message.reply_text(message)


def getDfCommand(update: Update, context):
    message = runCommand('df')
    update.message.reply_text(message)


def getFreeCommand(update: Update, context):
    message = runCommand('free')
    update.message.reply_text(message)


def getMpstatCommand(update: Update, context):
    message = runCommand('mpstat')
    update.message.reply_text(message)


def getWCommand(update: Update, context):
    message = runCommand('w')
    update.message.reply_text(message)


def getAuthsCommand(update: Update, context):
    message = runCommand('last -n 10')
    update.message.reply_text(message)


def getCriticalCommand(update: Update, context):
    message = runCommand('journalctl -p crit -n 5')
    update.message.reply_text(message)


def getPsCommand(update: Update, context):
    message = runCommand('ps')
    update.message.reply_text(message)


def getSsCommand(update: Update, context):
    message = runCommand('ss | tail')
    update.message.reply_text(message)


def getServicesCommand(update: Update, context):
    message = runCommand('sudo service --status-all | grep +')
    update.message.reply_text(message)


def getReleaseCommand(update: Update, context):
    message = runCommand('lsb_release -a')
    update.message.reply_text(message)


def getReplLogsCommand(update: Update, context):
    message = runCommand('sudo grep -a repl /var/log/postgresql/postgresql-11-main.log | tail')
    update.message.reply_text(message)


def dontWriteEmails(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_reply_markup(reply_markup=None)

