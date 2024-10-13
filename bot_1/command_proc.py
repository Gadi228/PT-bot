from telegram.ext import ConversationHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import re


def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')
    return 'findPhoneNumbers'


def findPhoneNumbers(update: Update, context):
    user_input = update.message.text  # Получаем текст, содержащий(или нет) номера телефонов
    phoneNumRegex = re.compile(r'(?:\+7|8)[-\s]?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2}[ -]?\d{2}')

    phoneNumberList = phoneNumRegex.findall(user_input)

    if not phoneNumberList:  # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Телефонные номера не найдены')
        return ConversationHandler.END

    phoneNumbers = ''
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i + 1}. {phoneNumberList[i]}\n'

    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data='phone'),
            InlineKeyboardButton("Нет", callback_data='dont_write'),
        ],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(phoneNumbers + "\n\nЗаписать ответ в базу данных?", reply_markup=reply_markup)
    context.user_data['phone'] = phoneNumberList
    return ConversationHandler.END


def findEmailsCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска email\'ов: ')
    return 'findEmails'


def findEmails(update: Update, context):
    user_input = update.message.text
    phoneNumRegex = re.compile(r'\b\w{1,50}@[a-z]{1,7}\.[a-z]{1,7}\b')

    emailList = phoneNumRegex.findall(user_input)

    if not emailList:
        update.message.reply_text('email\'ы не найдены')
        return ConversationHandler.END

    emails = ''
    for i in range(len(emailList)):
        emails += f'{i + 1}. {emailList[i]}\n'

    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data='email'),
            InlineKeyboardButton("Нет", callback_data='dont_write'),
        ],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(emails + "\n\nЗаписать ответ в базу данных?", reply_markup=reply_markup)
    context.user_data['email'] = emailList
    return ConversationHandler.END


def VerifyPasswordCommand(update: Update, context):
    update.message.reply_text('Введите пароль для проверки валидации: ')
    return 'VerifyPassword'


def VerifyPassword(update: Update, context):
    user_input = update.message.text

    validations = [r'.{8,}', r'[A-Z]', r'[a-z]', r'[0-9]', r'[!@#$%^&*()]']

    if not all(re.search(v, user_input) for v in validations):
        update.message.reply_text('Пароль простой')
        return

    update.message.reply_text('Пароль сложный')
    return ConversationHandler.END


def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Саламалейкум {user.full_name}!')


def echo(update: Update, context):
    update.message.reply_text(update.message.text)