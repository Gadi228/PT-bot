from dotenv import load_dotenv
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler, CallbackContext, CommandHandler, Updater
from command_proc import *
from command_proc_linux import *
from command_proc_sql import *

from telegram import Update

load_dotenv()

TOKEN = os.getenv('TOKEN')


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    choice = query.data
    if choice == 'main_menu':
        query.edit_message_text(text="Возвращаемся в главное меню...")
    else:
        query.edit_message_text(text=f"Вы выбрали пополнение на {choice} ₽")




def main():
    # Создайте программу обновлений и передайте ей токен вашего бота
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Регистрируем обработчики команд

    commands = {"start": start, "get_release": getReleaseCommand, "get_uname": getUnameCommand,
                "get_uptime": getUptimeCommand, "get_df": getDfCommand, "get_free": getFreeCommand,
                "get_mpstat": getMpstatCommand, "get_w": getWCommand, "get_auths": getAuthsCommand,
                "get_critical": getCriticalCommand, "get_ps": getPsCommand, "get_ss": getSsCommand,
                "get_services": getServicesCommand, "get_repl_logs": getReplLogsCommand,
                "get_emails": getEmailsCommand, "get_phone_numbers": getPhoneNumbersCommand}

    dp.add_handler(CallbackQueryHandler(writeData, pattern="^email"))
    dp.add_handler(CallbackQueryHandler(writeData, pattern="^phone"))
    dp.add_handler(CallbackQueryHandler(dontWriteEmails, pattern="^dont_write"))
    for command in commands:
        dp.add_handler(CommandHandler(command, commands[command]))

    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', getAptListCommand)],
        states={
            'getStr': [MessageHandler(Filters.text & ~Filters.command, getAptList)],
            # 'askForWrite': [MessageHandler(Filters.text & ~Filters.command, askForWrite)],
        },
        fallbacks=[]
    )
    dp.add_handler(convHandlerFindPhoneNumbers)

    # Обработка команды поиска номера
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'findPhoneNumbers': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
        },
        fallbacks=[]
    )
    dp.add_handler(convHandlerFindPhoneNumbers)

    # Обработка команды поиска email
    convHandlerFindEmails = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailsCommand)],
        states={
            'findEmails': [MessageHandler(Filters.text & ~Filters.command, findEmails)],
        },
        fallbacks=[]
    )
    dp.add_handler(convHandlerFindEmails)

    # Обработка команды верификации пароля
    convHandlerVerifyPassword = ConversationHandler(
        entry_points=[CommandHandler('verify_password', VerifyPasswordCommand)],
        states={
            'VerifyPassword': [MessageHandler(Filters.text & ~Filters.command, VerifyPassword)],
        },
        fallbacks=[]
    )
    dp.add_handler(convHandlerVerifyPassword)

    # Регистрируем обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запускаем бота
    updater.start_polling()

    # Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
