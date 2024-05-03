import telebot  
from telebot import types  
from generation import Text_to_image  
import os  
import time  
from threading import Thread  
from queue import Queue  
import schedule  
import re 
import json  
  
  
def read_access_list():  
    try:  
        with open('access_list.json', 'r') as file:  
            return json.load(file)  
    except FileNotFoundError:  
        return {}  
  
def update_access_list(access_user_list):  
    with open('access_list.json', 'w') as file:  
        json.dump(access_user_list, file, indent=4)  
  
# Пример чтения из файла при запуске бота  
access_user_list = read_access_list()  

  


def is_english_or_russian(text):  
    # Проверяем, содержит ли текст исключительно символы английского и русского алфавита, а также пробелы и знаки пунктуации  
    match = re.match(r'^[a-zA-Zа-яА-ЯёЁ\s.,!?-]*$', text)  
    if match:  
        # Считаем количество символов каждого алфавита  
        english_chars = len(re.findall(r'[a-zA-Z]', text))  
        russian_chars = len(re.findall(r'[а-яА-ЯёЁ]', text))  
          
        # Проверяем, преобладает ли один из алфавитов  
        if english_chars > 0 and russian_chars == 0:  
            return 'en'  
        elif russian_chars > 0 and english_chars == 0:  
            return 'ru'  
    return None  


API_TOKEN = 'API_TOKEN'  
bot = telebot.TeleBot(API_TOKEN)  
  
# Очередь для хранения запросов, которые не могут быть обработаны сразу  
request_queue = Queue()  
  
# Словарь для отслеживания времени последних запросов пользователей  
user_requests = {}  
 


    
@bot.message_handler(commands=['start'])    
def send_welcome(message):    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)    
    btn_my_images = types.KeyboardButton('Мои изображения')    
    btn_help = types.KeyboardButton('HELP')  # Добавляем кнопку HELP
    btn_subscription = types.KeyboardButton('Подписка')  # Добавляем кнопку Подписка  
      
    markup.add(btn_my_images, btn_help,btn_subscription)  # Добавляем обе кнопки в клавиатуру  
    bot.send_message(message.chat.id,     
                     "Привет! Я бот для генерации изображений.\n"    
                     "Чтобы сгенерировать изображение, просто отправь мне текст на английском или русском языке.\n"  
                     "Нажмите 'HELP' для получения дополнительной информации.\n"
                     "Выберите 'Подписка', чтобы узнать О подписке.\n"
                     "ВНИМАНИЕ\n"
                     "НЕ НАПИШИТЕ СООБЩЕНИЕ ВНЕ ЦЕНЗУРЫ \n"
                     "(НАСЕЛЕНИЯ, ОСКОРБЛЕНИЕ, 18 + КОНТЕНТ И\n "
                     "ТАК ДАЛЕЕ)  ЭТО ВСЕ РАВНО БУДЕТ  СЧИТАТЬСЯ\n"
                     " ЗАПРОСОМ И  ВАШИ ЗАПРОСЫ БУДУТ  УМЕНЬШАТЬСЯ\n",
                        
                     reply_markup=markup)    
    
    
    
@bot.message_handler(func=lambda message: message.text == "allow_list")  
def show_allow_list(message):  
    # Создаем строку, которая будет содержать информацию обо всех пользователях и их оставшихся запросах  
    allow_list_content = "Список доступа:\n"  
    for user_id, requests_left in access_user_list.items():  
        allow_list_content += f"ID: {user_id}, Оставшиеся запросы: {requests_left}\n"  
      
    # Проверка на пустоту списка доступа  
    if len(access_user_list) == 0:  
        allow_list_content = "Список доступа пуст."  
      
    # Отправляем сформированную строку обратно в чат  
    bot.reply_to(message, allow_list_content)  
    
    
@bot.message_handler(commands=['start', 'help'])      
def handle_commands(message):  
    # Команды /start и /help не уменьшают количество запросов  
    if message.text == '/start':  
        send_welcome(message)  
    elif message.text == '/help':  
        send_help(message)  
  


  
@bot.message_handler(func=lambda message: message.text == "Подписка")  
def subscription_info(message):
    user_id =  str(message.from_user.id)   
    bot.reply_to(message, "Доступ к боту на 10 запросов стоит 1000 драм, платежи принимаются через IDRAM.\n"  
                          "ID - 206898132.\n"  
                          "После оплаты присылайте скриншот чека на аккаунт @Saryan_AI_Admin и ждите подтверждения.\n"
                          f" { 'Запросов осталось '+ str(access_user_list[user_id]) if user_id in access_user_list  else 'У вас  нет подписки '}") 
    
    
      
@bot.message_handler(func=lambda message: message.text == "HELP")    
def send_help(message):
    
    bot.reply_to(message, "Руководство пользователя:\n"  
                          "- Чтобы сгенерировать изображение, отправьте мне текст.\n"  
                          "- Используйте кнопку 'Мои изображения', чтобы увидеть все изображения, которые вы создали.\n"  
                          "Текст должен быть на английском или русском языке.\n"
                          "ВНИМАНИЕ\n"
                          "НЕ НАПИШИТЕ СООБЩЕНИЕ ВНЕ ЦЕНЗУРЫ \n"
                          "(НАСЕЛЕНИЯ, ОСКОРБЛЕНИЕ, 18 + КОНТЕНТ И\n "
                          "ТАК ДАЛЕЕ)  ЭТО ВСЕ РАВНО БУДЕТ  СЧИТАТЬСЯ\n"
                          " ЗАПРОСОМ И  ВАШИ ЗАПРОСЫ БУДУТ  УМЕНЬШАТЬСЯ\n"
                          )  
  
@bot.message_handler(func=lambda message: message.text in ["Мои изображения", "HELP", "Подписка"])  
def handle_special_commands(message):  
    # Обработка специальных команд, которые не уменьшают количество запросов  
    if message.text == "Мои изображения":  
        list_user_images(message)  
    elif message.text == "HELP":  
        send_help(message)  
    elif message.text == "Подписка":  
        subscription_info(message)  
    
    
@bot.message_handler(func=lambda message: message.text == "Мои изображения")    
def list_user_images(message):    
    user_id = str(message.from_user.id)    
    user_dir = os.path.join(os.curdir, user_id)    
    if os.path.exists(user_dir) and os.path.isdir(user_dir):    
        for img_name in os.listdir(user_dir):    
            img_path = os.path.join(user_dir, img_name)    
            with open(img_path, 'rb') as img:    
                bot.send_photo(message.chat.id, img)    
    else:    
        bot.reply_to(message, "Вы еще не сгенерировали ни одного изображения.")    
    
    
    
     
def can_user_request(user_id):  
    """Проверяет, может ли пользователь сделать запрос."""  
    min_interval = 60 / 2  # минимальный интервал между запросами (в секундах)  
    current_time = time.time()  
    if user_id in user_requests:  
        last_request_time = user_requests[user_id]  
        if current_time - last_request_time < min_interval:  
            return False  
    user_requests[user_id] = current_time  
    return True  


  
def process_queue():  
    """Обрабатывает запросы из очереди."""  
    while not request_queue.empty():  
        message = request_queue.get()  
        handle_request(message)  
  
  
def handle_request(message):  
    """Обрабатывает запросы, отправляя изображения."""  
    user_id = message.from_user.id  
    text = message.text  
    
    try:  
        image_path = Text_to_image(text, str(user_id))  # Предполагаемая функция генерации изображения из текста  
        if os.path.exists(image_path):    
            with open(image_path, 'rb') as img:    
                bot.send_photo(message.chat.id, img)    
        else:    
            bot.reply_to(message, "Произошла ошибка при генерации изображения.")  
    except:  
         
        bot.reply_to(message, "возможно ваш запрос контент вне цензуры,  если это не так  пожалуйста попробуйте позже или напишите @Saryan_AI_Admin ") 
  
  
  
  
@bot.message_handler(func=lambda message: message.text.startswith("allow"))  
def allow_user(message):  
    # Разрешаем пользователю отправлять сообщения, добавляя его ID в список с указанным количеством запросов  
    try:  
        parts = message.text.split()  
        user_id = parts[1]  
        # Проверяем, указано ли количество запросов, если нет, используем значение по умолчанию 10  
        requests_count = int(parts[2]) if len(parts) > 2 else 10  
          
        # Добавляем или обновляем пользователя в списке с указанным количеством запросов  
        access_user_list[user_id] = requests_count  
        update_access_list(access_user_list)  # Обновляем список доступа в файле  
          
        bot.reply_to(message, f"Пользователю с ID {user_id} разрешено отправить {requests_count} сообщений.")  
          
    except IndexError:  
        bot.reply_to(message, "Неправильный формат. Используйте: allow <user_id> [количество запросов]")  
    except ValueError:  
        bot.reply_to(message, "Указано неверное количество запросов. Пожалуйста, укажите число.")  

   
  
  
  
  

  
@bot.message_handler(func=lambda message: True)  
def handle_text(message):
    
    lang = is_english_or_russian(message.text)  
      
    if lang is None:  
        bot.reply_to(message, "Извините, ваше сообщение должно быть написано либо на английском, либо на русском языке.")  
        return 


    
    user_id = message.from_user.id
    
    # Проверяем, есть ли пользователь в списке доступа и уменьшаем количество запросов  
    if str(user_id) in access_user_list:  
        if access_user_list[str(user_id)] > 0:  
            access_user_list[str(user_id)] -= 1  # Уменьшаем количество запросов  
               
            if access_user_list[str(user_id)] == 0:  
                bot.reply_to(message, "Вы использовали все свои запросы. Пожалуйста, оформите подписку.")
                return  
        else:  
            bot.reply_to(message, "У вас нет оставшихся запросов. Пожалуйста, оформите подписку.")
            return  
    else:  
        bot.reply_to(message, "У вас нет доступа к этой функции. Пожалуйста, оформите подписку.")
        return
        
    
    if not can_user_request(message.from_user.id):  
        bot.reply_to(message, "Ваш запрос добавлен в очередь. Он будет обработан, как только это станет возможно.")  
        request_queue.put(message)  
        return  
    
    
    
    
    handle_request(message)  
  
# Запускаем фоновый процесс для обработки очереди  
def start_queue_processor():  
    def queue_processor():  
        while True:  
            process_queue()  
            time.sleep(10)  # Ждем некоторое время перед следующей обработкой  
  
    thread = Thread(target=queue_processor)  
    thread.start()  
  
start_queue_processor()  
  

bot.infinity_polling()

