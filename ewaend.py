import telebot
from telebot import types

# Bot token
TOKEN = "7503142025:AAHvVQAtoVIRDNffTADd5DZ5pgYVAdWX8oI"
bot = telebot.TeleBot(TOKEN, parse_mode='MarkdownV2')

# Constants
makeanorder = '\n\n\n❌Для просмотра товара можно❌\\:\n1️⃣Просмотреть товары в web версии \n2️⃣Просмотреть рекомендованные товары в паблике \\" продукт\\" \n3️⃣Опишите проблему\\, менеджер подберет подходящий вам товар \nВведи /cancel для отмены действий'
testcat = "команда в разработке \nможешь воспользоваться следущими возможностями\\: \n/start \\- главное меню\\. \n/appeals \\- Обращения"

# Функция для записи данных в JSON файл
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    keyaaa = types.InlineKeyboardButton('Web vershion', web_app=telebot.types.WebAppInfo('https://mov001.github.io/testiruem2/'))
    keyd = types.InlineKeyboardButton('public', url='https://t.me/nupizdetshe')
    appeals = types.InlineKeyboardButton('Оформление', callback_data='appeals')
    markup.add(keyd, appeals, keyaaa)
    bot.send_message(message.chat.id, '🫰   ㅤТвой  мирㅤ   🫰', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'appeals')
def show_additional_button(call):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    afrome = telebot.types.InlineKeyboardButton('Оформить отзыв', callback_data='afrome')
    bfrome = telebot.types.InlineKeyboardButton('Оформить заказ', callback_data='bfrome')
    onstart = telebot.types.InlineKeyboardButton('Назад', callback_data='onstart')
    markup.add(afrome, bfrome, onstart)
    # Edit both text and reply_markup in one operation
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, 
                          text='🫰   ㅤТвой  мирㅤ   🫰', reply_markup=markup)
    bot.answer_callback_query(call.id)

admin_id = "6285222102"  # Replace with your Telegram ID

@bot.message_handler(commands=['cancel'])
def cancel_handler(message):
    bot.send_message(message.chat.id, 'Отмена')
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)

@bot.message_handler(commands=['appeals'])
def handle_command(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    afrome = types.InlineKeyboardButton('Оформить отзыв', callback_data='afrome')
    bfrome = types.InlineKeyboardButton('Оформить заказ', callback_data='bfrome')
    onstart = types.InlineKeyboardButton('Назад', callback_data='onstart')
    markup.add(afrome, bfrome, onstart)
    bot.send_message(chat_id=message.chat.id, text='🫰   ㅤТвой  мирㅤ   🫰', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'afrome')
def ask_for_review_name(call):
    bot.send_message(call.message.chat.id, 'Пожалуйста, введите ваше имя')
    bot.register_next_step_handler(call.message, ask_for_review)
    bot.answer_callback_query(call.id)

def ask_for_review(message):
    if message.text.lower() == '/cancel':
        cancel_handler(message)
        return
    name = message.text
    bot.send_message(message.chat.id, 'Пожалуйста, оставьте свой отзыв')
    bot.register_next_step_handler(message, save_review, name)
    return

def save_review(message, name):
    if message.text.lower() == '/cancel':
        cancel_handler(message)
        return
    review = message.text
    user_id = message.from_user.id
    username = message.from_user.username
    with open('reviews.txt', 'a', encoding='utf-8') as file:
        file.write(f"Имя: {name}\nОтзыв: {review}\n\n ID: {user_id}\nUsername: @{username}")
    bot.send_message(message.chat.id, 'Спасибо за отзыв')
    bot.send_message(admin_id, f"Отзыв\\. \nИмя: {name}\nОтзыв: {review}\nID: {user_id}\nUsername: @{username}")

@bot.callback_query_handler(func=lambda call: call.data == 'bfrome')
def ask_for_order_name(call):
    bot.send_message(call.message.chat.id, 'Введите ваше имя, фамилию, город')
    bot.register_next_step_handler(call.message, ask_for_order)
    bot.answer_callback_query(call.id)

def ask_for_order(message):
    if message.text.lower() == '/cancel':
        cancel_handler(message)
        return
    name = message.text
    bot.send_message(message.chat.id, 'Введите товар, который хотите приобрести и его кол\\-во' + makeanorder)
    bot.register_next_step_handler(message, save_order, name)
    return

def save_order(message, name):
    if message.text.lower() == '/cancel':
        cancel_handler(message)
        return
    order = message.text
    user_id = message.from_user.id
    username = message.from_user.username
    with open('orders.txt', 'a', encoding='utf-8') as file:
        file.write(f"Имя: {name}\nПокупка: {order}\n\n ID: {user_id}\nUsername: @{username}")
    bot.send_message(message.chat.id, 'Спасибо за обращение\\. Ожидайте ответа администратора')
    bot.send_message(admin_id, f"ФИГ: {name}\nПокупка: {order}\nID: {user_id}\nUsername: @{username}")

@bot.callback_query_handler(func=lambda call: call.data == 'onstart')
def back_to_start(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    keyaaa = types.InlineKeyboardButton('Web vershion', web_app=telebot.types.WebAppInfo('https://mov001.github.io/testiruem2/'))
    keyd = types.InlineKeyboardButton('public', url='https://t.me/nupizdetshe')
    appeals = types.InlineKeyboardButton('Оформление', callback_data='appeals')
    markup.add(keyd, appeals, keyaaa)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='🫰   ㅤТвой EWA мирㅤ   🫰', reply_markup=markup)
    bot.answer_callback_query(call.id)

bot.polling(none_stop=True, interval=0)