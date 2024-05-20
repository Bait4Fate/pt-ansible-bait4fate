import logging
import re
import psycopg2
from psycopg2 import Error
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import paramiko
import os

emailList = ''
phoneNumberList = ''
host = os.getenv('RM_HOST')
host_db = os.getenv('DB_HOST')
port_ssh = os.getenv('RM_PORT')
port_db = os.getenv('PORT_DB')
database = os.getenv('DB_DATABASE')
username_ssh = os.getenv('RM_USER')
username_db = os.getenv('DB_USER')
password = os.getenv('RM_PASSWORD')
password_db = os.getenv('DB_PASSWORD')
repl_user = os.getenv('DB_REPL_USER')
repl_password = os.getenv('DB_REPL_PASSWORD')
repl_host = os.getenv('DB_REPL_HOST')
repl_port = os.getenv('DB_REPL_PORT')
logs = os.getenv('LOGS')
TOKEN = os.getenv('TOKEN')

logging.basicConfig(filename='log.txt')
logging.getLogger("paramiko").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)


def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')


def helpCommand(update: Update, context):
    update.message.reply_text('Help!')


def repllogCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username_ssh, password=password, port=port_ssh)
    print(client.exec_command(f'cat {logs} | head -20'))
    stdin, stdout, stderr = client.exec_command(f"cat {logs} | grep -i replication | tail -n 20")

    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def emailsCommand(update: Update, context):
    connection = None
    try:
        connection = psycopg2.connect(user=username_db,
                                      password=password_db,
                                      host=host_db,
                                      port=port_db,
                                      database=database)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM email;")
        data = cursor.fetchall()
        info = ""
        for i in data:
            info += f'{i[0]}. {i[1]}\n'
        update.message.reply_text(info)
        logging.info("Команда успешно выполнена")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            connection.close()


def phoneCommand(update: Update, context):
    connection = None
    try:
        connection = psycopg2.connect(user=username_db,
                                      password=password_db,
                                      host=host_db,
                                      port=port_db,
                                      database=database)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM phone;")
        data = cursor.fetchall()
        info = ""
        for i in data:
            info += f'{i[0]}. {i[1]}\n'
        update.message.reply_text(info)
        logging.info("Команда успешно выполнена")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            connection.close()


def releaseCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username_ssh, password=password, port=port_ssh)
    stdin, stdout, stderr = client.exec_command('cat /etc/os-release')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def unameCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username_ssh, password=password, port=port_ssh)
    stdin, stdout, stderr = client.exec_command('uname -r')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def uptimeCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username_ssh, password=password, port=port_ssh)
    stdin, stdout, stderr = client.exec_command('uptime')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def dfCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username_ssh, password=password, port=port_ssh)
    stdin, stdout, stderr = client.exec_command('df')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def freeCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username_ssh, password=password, port=port_ssh)
    stdin, stdout, stderr = client.exec_command('free')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def mpstatCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username_ssh, password=password, port=port_ssh)
    stdin, stdout, stderr = client.exec_command('mpstat')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def wCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username_ssh, password=password, port=port_ssh)
    stdin, stdout, stderr = client.exec_command('w')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def authCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username_ssh, password=password, port=port_ssh)
    stdin, stdout, stderr = client.exec_command('last -10')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def criticalCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username_ssh, password=password, port=port_ssh)
    stdin, stdout, stderr = client.exec_command('dmesg -l crit | head -20')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def psCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username_ssh, password=password, port=port_ssh)
    stdin, stdout, stderr = client.exec_command('ps aux | head -20')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def ssCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username_ssh, password=password, port=port_ssh)
    stdin, stdout, stderr = client.exec_command('ss | head -10')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def aptlistCommand(update: Update, context):
    user_input = update.message.text
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username_ssh, password=password, port=port_ssh)
    if user_input == "Все":
        stdin, stdout, stderr = client.exec_command('apt list --installed | head -10')
        data = stdout.read() + stderr.read()
        client.close()
        data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
        update.message.reply_text(data)
        return ConversationHandler.END
    else:
        stdin, stdout, stderr = client.exec_command(f'apt show {user_input}')
        data = stdout.read() + stderr.read()
        client.close()
        data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
        update.message.reply_text(data)
        return ConversationHandler.END


def servicesCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username_ssh, password=password, port=port_ssh)
    stdin, stdout, stderr = client.exec_command('systemctl list-units --type=service --state=running')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def getAptList(update: Update, context):
    update.message.reply_text('Введите название пакета или напишите "Все", чтобы вывести все пакеты')

    return 'get_apt_list'


def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'find_phone_number'


def findEmails(update: Update, context):
    update.message.reply_text('Введите текст для поиска электронных адресов: ')

    return 'find_email'


def verifyPassword(update: Update, context):
    update.message.reply_text('Введите пароль для проверки: ')

    return 'verify_password'


def verify_password(update: Update, context):
    user_input = update.message.text

    passwordRegex = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!@#$%^&*()]).{8,}$")

    password = user_input

    if bool(passwordRegex.match(password)) == True:
        update.message.reply_text('Пароль сложный')
        return ConversationHandler.END
    else:
        update.message.reply_text('Пароль простой')
        return ConversationHandler.END


def find_email(update: Update, context):
    user_input = update.message.text

    emailRegex = re.compile(r'\b[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+)*' \
                            r'@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b')
    global emailList
    emailList = emailRegex.findall(user_input)

    if not emailList:
        update.message.reply_text('Электронные адреса не найдены')
        emailList = ''
        return ConversationHandler.END
    emails = ''
    for i in range(len(emailList)):
        emails += f'{i + 1}. {emailList[i]}\n'
    update.message.reply_text(emails)
    update.message.reply_text('Добавить в БД? Введите "Да", чтобы добавить.')
    logging.info(f"{user_input}")
    return 'add_email'


def add_email(update: Update, context):
    global emailList
    logging.info("Попали в add_email")
    user_input = update.message.text
    logging.info(f"{user_input}")
    if user_input == 'Да':
        logging.info("Положительный ответ")
        connection = None
        try:
            connection = psycopg2.connect(user=username_db,
                                          password=password_db,
                                          host=host_db,
                                          port=port_db,
                                          database=database)
            cursor = connection.cursor()
            logging.info("Подключение к БД...")
            for i in range(len(emailList)):
                cursor.execute(f"INSERT INTO email (address) VALUES ('{emailList[i]}');")
                logging.info("Добавлен email в БД")
            connection.commit()
            logging.info("Команда успешно выполнена")
            update.message.reply_text("Адреса добавлены.")
            emailList = ''
            return ConversationHandler.END
        except (Exception, Error) as error:
            emailList = ''
            logging.error("Ошибка при работе с PostgreSQL: %s", error)
        finally:
            if connection is not None:
                connection.close()
                logging.info("Соединение с PostgreSQL закрыто")
            else:
                emailList = ''
                return ConversationHandler.END
    else:
        emailList = ''
        logging.info("Отказ")
        update.message.reply_text("Адреса не будут добавлены в БД.")
        return ConversationHandler.END


def find_phone_number(update: Update, context):
    user_input = update.message.text
    phoneNumRegex = re.compile(
        r"\+?7[ -]?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}|\+?7[ -]?\d{10}|8[ -]?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}|8[ -]?\d{10}")  # regex
    global phoneNumberList
    phoneNumberList = phoneNumRegex.findall(user_input)

    if not phoneNumberList:
        update.message.reply_text('Телефонные номера не найдены')
        phoneNumberList = ''
        return ConversationHandler.END

    phoneNumbers = ''
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i + 1}. {phoneNumberList[i]}\n'

    update.message.reply_text(phoneNumbers)
    update.message.reply_text('Добавить в БД? Введите "Да", чтобы добавить.')
    logging.info(f"{user_input}")
    return 'add_phone_number'


def add_phone_number(update: Update, context):
    global phoneNumberList
    logging.info("Попали в add_phone_number")
    user_input = update.message.text
    logging.info(f"{user_input}")
    if user_input == 'Да':
        logging.info("Положительный ответ")
        connection = None
        try:
            connection = psycopg2.connect(user=username_db,
                                          password=password_db,
                                          host=host_db,
                                          port=port_db,
                                          database=database)
            cursor = connection.cursor()
            logging.info("Подключение к БД...")
            for i in range(len(phoneNumberList)):
                cursor.execute(f"INSERT INTO phone (number) VALUES ('{phoneNumberList[i]}');")
                logging.info("Добавлен номер в БД")
            connection.commit()
            logging.info("Команда успешно выполнена")
            update.message.reply_text("Номера добавлены.")
            phoneNumberList = ''
            return ConversationHandler.END
        except (Exception, Error) as error:
            phoneNumberList = ''
            logging.error("Ошибка при работе с PostgreSQL: %s", error)
        finally:
            if connection is not None:
                connection.close()
                phoneNumberList = ''
                logging.info("Соединение с PostgreSQL закрыто")
            else:
                phoneNumberList = ''
                return ConversationHandler.END
    else:
        phoneNumberList = ''
        logging.info("Отказ")
        update.message.reply_text("Номера не будут добавлены в БД.")
        return ConversationHandler.END


def echo(update: Update, context):
    update.message.reply_text(update.message.text)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'find_phone_number': [MessageHandler(Filters.text & ~Filters.command, find_phone_number)],
            'add_phone_number': [MessageHandler(Filters.text & ~Filters.command, add_phone_number)],
        },
        fallbacks=[]
    )

    convHandlerFindEmails = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmails)],
        states={
            'find_email': [MessageHandler(Filters.text & ~Filters.command, find_email)],
            'add_email': [MessageHandler(Filters.text & ~Filters.command, add_email)],
        },
        fallbacks=[]
    )

    convHandlerVerifyPassword = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verifyPassword)],
        states={
            'verify_password': [MessageHandler(Filters.text & ~Filters.command, verify_password)],
        },
        fallbacks=[]
    )

    convHandlerAptList = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', getAptList)],
        states={
            'get_apt_list': [MessageHandler(Filters.text & ~Filters.command, aptlistCommand)],
        },
        fallbacks=[]
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(CommandHandler("get_repl_logs", repllogCommand))
    dp.add_handler(CommandHandler("get_emails", emailsCommand))
    dp.add_handler(CommandHandler("get_phone_numbers", phoneCommand))
    dp.add_handler(CommandHandler("get_release", releaseCommand))
    dp.add_handler(CommandHandler("get_uname", unameCommand))
    dp.add_handler(CommandHandler("get_uptime", uptimeCommand))
    dp.add_handler(CommandHandler("get_df", dfCommand))
    dp.add_handler(CommandHandler("get_free", freeCommand))
    dp.add_handler(CommandHandler("get_mpstat", mpstatCommand))
    dp.add_handler(CommandHandler("get_w", wCommand))
    dp.add_handler(CommandHandler("get_auths", authCommand))
    dp.add_handler(CommandHandler("get_critical", criticalCommand))
    dp.add_handler(CommandHandler("get_ps", psCommand))
    dp.add_handler(CommandHandler("get_ss", ssCommand))
    dp.add_handler(CommandHandler("get_services", servicesCommand))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmails)
    dp.add_handler(convHandlerVerifyPassword)
    dp.add_handler(convHandlerAptList)
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
