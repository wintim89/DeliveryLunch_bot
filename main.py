# -*- coding: utf-8 -*-
import telebot
from telebot import types
from prettytable import PrettyTable
bot = telebot.TeleBot(open("token.txt","r",encoding="utf-8").read())
users = [7261478172,6682897931,1134419527]
shopping_cart = [] #{"price": x , "title": y}, {"price": x , "title": y}
margin = 1.2

def to_cart(user_id, price, product):
    shopping_cart.append({"price": int(price) , "title": product, "id": int(user_id)})
    bot.send_message(chat_id=user_id, text=f'Товар "{product}" был добавлен в вашу корзину\nЦЕНА:{int(price)}')
def del_cart(user_id,cart):
    for i in range(len(cart)):
        if cart[i]["id"] == user_id:
            cart.remove(cart[i])
def draw_cart(list,user_id):
    th = ["Товар", "Цена", "Итого:"]
    pretd = []
    td = []
    sum = 0
    for i in range(len(list)):
        if user_id == list[i]["id"]:
            #td.append(list[i].remove(list[i]["id"]))
            pretd.append(list[i])
    if len(pretd) == 0:
        return "Корзина пуста"
    for i in range(len(pretd)):
        td.append(pretd[i]["title"])
        td.append(pretd[i]["price"])
        sum = sum + int(pretd[i]["price"])
        if i+1 != len(pretd):
            td.append('')
        else: td.append(sum)
    print(pretd)
    columns = len(th)
    table = PrettyTable(th)
    td_data = td[:]
    while td_data:
        table.add_row(td_data[:columns])
        td_data = td_data[columns:]
    return "<pre>" +table.get_string()+ "</pre>"

def total(user_id,cart):
    total_price = 0
    for i in range(len(cart)):
        if cart[i]["id"] == user_id:
            total_price += cart[i]["price"]
    return  total_price

def checking_cart(user_id):
    a = 0
    for i in range(len(shopping_cart)):
        if shopping_cart[i]["id"] == user_id:
            a += 1
    if a == 0:
        return False
    else: return True


@bot.message_handler(commands=['start'])
def get_command_messages(message):
    photo = open("photo.png", 'rb')
    if (message.from_user.id in users):

        current_user = message.from_user.id


        markup = types.InlineKeyboardMarkup()

        key_fast_menu = types.InlineKeyboardButton(text='🍽️ Быстрое Меню', callback_data="Fast_menu")
        key_cart = types.InlineKeyboardButton(text='🛒 Корзина', callback_data="Сart")
        key_long_menu = types.InlineKeyboardButton(text='📋 Долгое меню', callback_data="Long_menu")

        markup.row(key_fast_menu)
        markup.row(key_cart)
        markup.row(key_long_menu)

        bot.send_photo(current_user, photo, reply_markup=markup, caption =
        'Из быстрого меню можно добавить товары в корзину.\nДля заказа товаров которых нет в быстром меню нажмите:\n"📋 Долгое меню"')
        photo.close()
    else:
        print(f"в бота написал новый человек id: {message.from_user.id}")
        users.append(message.from_user.id)

@bot.callback_query_handler(func=lambda c: c.data == 'Delete')
def Delete(call):
    if checking_cart(call.from_user.id):
        del_cart(call.from_user.id, shopping_cart)
        Cart(call)
    else:
        bot.send_message(chat_id=call.from_user.id, text="Корзина и так пустая\nнахер ты сюда нажимаешь?")
        bot.answer_callback_query( call.id , text="Button clicked!")
@bot.callback_query_handler(func=lambda c: c.data == 'Pay_confirm')
def Confirm(call):
    global user_idd
    bot.send_message(chat_id=user_idd,
                     text=f"✔️ Ваш платеж был одобрен\n"
                          f"ожидайте свой заказ",)
    bot.answer_callback_query(call.id, show_alert=False)
@bot.callback_query_handler(func=lambda c: c.data == 'Pay_cancel')
def Cancel(call):
    global user_idd
    bot.send_message(chat_id=user_idd,
                     text=f"❌ Ваш платеж был отклонен\n"
                          f"не ожидайте свой заказ", )
    bot.answer_callback_query(call.id, show_alert=False)

@bot.callback_query_handler(func=lambda c: c.data == 'Pay_correct')
def Pay_correct(call):
    global user_idd
    user_idd = call.from_user.id
    bot.send_message(chat_id=call.from_user.id,
                     text="Подождите ваш платеж на обработке",
                     parse_mode="html")
    markup = types.InlineKeyboardMarkup()
    key_confirm = types.InlineKeyboardButton(text='💸 Подтвердить платеж', callback_data="Pay_confirm")
    key_cancel = types.InlineKeyboardButton(text='❌ Отменить платеж', callback_data="Pay_cancel")

    markup.row(key_confirm)
    markup.row(key_cancel)
    msg = bot.send_message(chat_id=7261478172,text=draw_cart(shopping_cart,user_id = call.from_user.id )+
                                             f"\nПроверяй СБЕР должен поступить платеж на сумму {total(call.from_user.id,shopping_cart)}р\n"
                                             f"от пользователя по имени {call.from_user.first_name}\n"
                                             f"@{call.from_user.username}",parse_mode="html",reply_markup=markup)


@bot.callback_query_handler(func=lambda c: c.data == 'Paying')
def Paying(call):
    if checking_cart(call.from_user.id):
        markup = types.InlineKeyboardMarkup()
        key_paying = types.InlineKeyboardButton(text='💸 Я оплатил(а)', callback_data="Pay_correct")
        key_back = types.InlineKeyboardButton(text='❌ Отмена', callback_data="Menu")
        markup.row(key_paying, key_back)
        bot.send_message(chat_id=call.from_user.id,
                         text=f"<pre>{total(call.from_user.id, shopping_cart)}</pre>",
                         parse_mode="html")
        bot.send_message(chat_id=call.from_user.id,
                         text=f"<pre>89538737075</pre>",
                         parse_mode="html")
        bot.send_message(chat_id=call.from_user.id,
                         text=f"Для оплаты вам нужно перевести {total(call.from_user.id, shopping_cart)}р\nпо номеру 89538737075 на сбер",
                         reply_markup=markup)
        bot.answer_callback_query(call.id, show_alert = False)
    else:
        bot.send_message(chat_id=call.from_user.id, text="Корзина пустая\nнахер ты сюда нажимаешь?")
        bot.answer_callback_query(call.id, show_alert = False)
@bot.callback_query_handler(func=lambda c: c.data == 'Сart')
def Cart(call):
    markup = types.InlineKeyboardMarkup()
    key_paying = types.InlineKeyboardButton(text='💸 Оплатить', callback_data="Paying")
    key_delete = types.InlineKeyboardButton(text='🗑️ Очистить корзину', callback_data="Delete")
    key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Menu")
    markup.row(key_delete)
    markup.row(key_paying, key_back)
    bot.edit_message_caption(chat_id=call.from_user.id, message_id=call.message.id,
                             caption=draw_cart(shopping_cart,user_id = call.from_user.id ),
                             reply_markup=markup, parse_mode="html")
    # print(draw_cart(shopping_cart))
@bot.callback_query_handler(func=lambda c: c.data == 'Fast_menu' or c.data == 'Back')
def Menu(call):
    markup = types.InlineKeyboardMarkup()
    key_eats = types.InlineKeyboardButton(text='🍽️ Еда', callback_data="Eats")
    key_drinks = types.InlineKeyboardButton(text='🥂 Напитки', callback_data="Drinks")
    key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Menu")

    markup.row(key_eats)
    markup.row(key_drinks)
    markup.row(key_back)

    bot.edit_message_caption(chat_id=call.from_user.id, message_id=call.message.id, caption="Выберите раздел товаров:",
                             reply_markup=markup)
@bot.callback_query_handler(func=lambda c: c.data == 'Drinks')
def Drinks(call):
    markup = types.InlineKeyboardMarkup()

    key_cola = types.InlineKeyboardButton(text='🥤 Кола', callback_data="Cola")
    key_water = types.InlineKeyboardButton(text='💧 Вода', callback_data="Water")
    key_juice = types.InlineKeyboardButton(text='🧃 Сок', callback_data="Juice")
    key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Back")

    markup.row(key_cola)
    markup.row(key_water)
    markup.row(key_juice)
    markup.row(key_back)

    bot.edit_message_caption(chat_id=call.from_user.id, message_id=call.message.id, caption="Выберите товар, затем спецификацию:",
                             reply_markup=markup)
@bot.callback_query_handler(func=lambda c: c.data == 'Cola')
def Cola(call):
    markup = types.InlineKeyboardMarkup()

    key_kind_cola = types.InlineKeyboardButton(text='🥤 Добрый кола', callback_data="Kind_cola")
    key_kind_cola_zero = types.InlineKeyboardButton(text='🥤 Добрый кола зеро', callback_data="Kind_cola_zero")
    key_black_cola = types.InlineKeyboardButton(text='🥤 Кола черноголовка', callback_data="Black_cola")
    key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Back")

    markup.row(key_kind_cola)
    markup.row(key_kind_cola_zero)
    markup.row(key_black_cola)
    markup.row(key_back)

    bot.edit_message_caption(chat_id=call.from_user.id, message_id=call.message.id,
                             caption="Пейте без остановки колу из черноголовки\nНажмите чтобы добавить товар в корзину:",
                             reply_markup=markup)
@bot.callback_query_handler(func=lambda c: c.data == 'Kind_cola')
def Kind_cola(call):
    to_cart(call.from_user.id, 100 * margin, "Добрый кола")
    bot.answer_callback_query(call.id, show_alert = False)
@bot.callback_query_handler(func=lambda c: c.data == 'Kind_cola_zero')
def Kind_cola_zero(call):
    to_cart(call.from_user.id, 100 * margin, "Добрый кола зеро")
    bot.answer_callback_query(call.id, show_alert = False)
@bot.callback_query_handler(func=lambda c: c.data == 'Black_cola')
def Black_cola(call):
    to_cart(call.from_user.id, 100 * margin, "Кола черноголовка")
    bot.answer_callback_query(call.id, show_alert = False)
@bot.callback_query_handler(func=lambda c: c.data == 'Water')
def Water(call):
    markup = types.InlineKeyboardMarkup()

    key_still_water = types.InlineKeyboardButton(text='💦 Вода still', callback_data="Still")
    key_sparkling_water = types.InlineKeyboardButton(text='💦 Вода sparkling', callback_data="Sparkling")
    key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Back")

    markup.row(key_still_water)
    markup.row(key_sparkling_water)
    markup.row(key_back)

    bot.edit_message_caption(chat_id=call.from_user.id, message_id=call.message.id,
                             caption="Это стил вотер, стил вотер\nНажмите чтобы добавить товар в корзину:",
                             reply_markup=markup)
@bot.callback_query_handler(func=lambda c: c.data == 'Still')
def Still(call):
    to_cart(call.from_user.id, 100 * margin, "Вода still")
    bot.answer_callback_query(call.id, show_alert = False)
@bot.callback_query_handler(func=lambda c: c.data == 'Sparkling')
def Sparkling(call):
    to_cart(call.from_user.id, 100 * margin, "Вода sparkling")
    bot.answer_callback_query(call.id, show_alert = False)
@bot.callback_query_handler(func=lambda c: c.data == 'Juice')
def Juice(call):
    markup = types.InlineKeyboardMarkup()

    key_orange_juice = types.InlineKeyboardButton(text='🧃 Апельсиновый сок', callback_data="Orange_juice")
    key_apple_juice = types.InlineKeyboardButton(text='🧃 Яблочный сок', callback_data="Apple_juice")
    key_random_juice = types.InlineKeyboardButton(text='🧃 Рандомный сок нахуй', callback_data="Random_juice")
    key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Back")

    markup.row(key_orange_juice)
    markup.row(key_apple_juice)
    markup.row(key_random_juice)
    markup.row(key_back)

    bot.edit_message_caption(chat_id=call.from_user.id, message_id=call.message.id,
                             caption="Пейте без остановки колу из черноголовки\nНажмите чтобы добавить товар в корзину:",
                             reply_markup=markup)
@bot.callback_query_handler(func=lambda c: c.data == 'Orange_juice')
def Orange_juice(call):
    to_cart(call.from_user.id, 100 * margin, "Апельсиновый сок")
    bot.answer_callback_query(call.id, show_alert = False)
@bot.callback_query_handler(func=lambda c: c.data == 'Apple_juice')
def Apple_juice(call):
    to_cart(call.from_user.id, 100 * margin, "Яблочный сок")
    bot.answer_callback_query(call.id, show_alert = False)
@bot.callback_query_handler(func=lambda c: c.data == 'Random_juice')
def Random_juice(call):
    to_cart(call.from_user.id, 100 * margin, "Рандомный сок")
    bot.answer_callback_query(call.id, show_alert = False)
@bot.callback_query_handler(func=lambda c: c.data == 'Eats')
def Eats(call):
    markup = types.InlineKeyboardMarkup()

    key_onigiri = types.InlineKeyboardButton(text='🍙 Онигири', callback_data="Onigiri")
    key_pizza = types.InlineKeyboardButton(text='🍕 Пицца', callback_data="Pizza")
    key_bun = types.InlineKeyboardButton(text='🥐 Слойка с ...', callback_data="Bun")
    key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Back")

    markup.row(key_onigiri)
    markup.row(key_pizza)
    markup.row(key_bun)
    markup.row(key_back)

    bot.edit_message_caption(chat_id=call.from_user.id, message_id=call.message.id, caption="Выберите товар, затем спецификацию:",
                             reply_markup=markup)
@bot.callback_query_handler(func=lambda c: c.data == 'Onigiri')
def Onigiri(call):
    markup = types.InlineKeyboardMarkup()

    key_onigiri_shrimp = types.InlineKeyboardButton(text='🍙 Онигири с Креветкой', callback_data="Shrimp")
    key_onigiri_gentle = types.InlineKeyboardButton(text='🍙 Онигири Нежный', callback_data="Gentle")
    key_onigiri_philadelphia = types.InlineKeyboardButton(text='🍙 Онигири Филадельфия', callback_data="Philadelphia")
    key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Back")

    markup.row(key_onigiri_shrimp)
    markup.row(key_onigiri_gentle)
    markup.row(key_onigiri_philadelphia)
    markup.row(key_back)

    bot.edit_message_caption(chat_id=call.from_user.id, message_id=call.message.id,
                             caption="Нажмите чтобы добавить товар в корзину:",
                             reply_markup=markup)
@bot.callback_query_handler(func=lambda c: c.data == 'Shrimp')
def Shrimp(call):
    to_cart(call.from_user.id, 100 * margin, "Онигири с Креветкой")
    bot.answer_callback_query(call.id, show_alert = False)
@bot.callback_query_handler(func=lambda c: c.data == 'Gentle')
def Gentle(call):
    to_cart(call.from_user.id, 100 * margin, "Онигири Нежный")
    bot.answer_callback_query(call.id, show_alert = False)
@bot.callback_query_handler(func=lambda c: c.data == 'Philadelphia')
def Philadelphia(call):
    to_cart(call.from_user.id,100*margin,"Онигири Филадельфия")
    bot.answer_callback_query(call.id, show_alert = False)
@bot.callback_query_handler(func=lambda c: c.data == 'Pizza')
def Pizza(call):
    markup = types.InlineKeyboardMarkup()

    key_pizza = types.InlineKeyboardButton(text='🍕 Пицца', callback_data="Pizza_Cart")
    key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Back")

    markup.row(key_pizza)
    markup.row(key_back)

    bot.edit_message_caption(chat_id=call.from_user.id, message_id=call.message.id,
                             caption="Нажмите чтобы добавить товар в корзину:",
                             reply_markup=markup)
@bot.callback_query_handler(func=lambda c: c.data == 'Pizza_Cart')
def Pizza_Cart(call):
    to_cart(call.from_user.id,100*margin,"Пицца")
    bot.answer_callback_query(call.id, show_alert = False)
@bot.callback_query_handler(func=lambda c: c.data == 'Bun')
def Bun(call):
    markup = types.InlineKeyboardMarkup()

    key_bun_cherry = types.InlineKeyboardButton(text='🥐 Слойка с вишней', callback_data="Cherry")
    key_bun_apple = types.InlineKeyboardButton(text='🥐 Слойка с яблоком', callback_data="Apple")
    key_bun_blueberry = types.InlineKeyboardButton(text='🥐 Слойка с голубикой', callback_data="Blueberry")
    key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Back")

    markup.row(key_bun_cherry)
    markup.row(key_bun_apple)
    markup.row(key_bun_blueberry)
    markup.row(key_back)

    bot.edit_message_caption(chat_id=call.from_user.id, message_id=call.message.id,
                             caption="Мои руки как слойка с вишней...\nЕсли нужной слойки не будет она будет заменена на любую слойку без творога\nНажмите чтобы добавить товар в корзину:",
                             reply_markup=markup)
@bot.callback_query_handler(func=lambda c: c.data == 'Cherry')
def Cherry(call):
    to_cart(call.from_user.id, 100 * margin, "Слойка с вишней")
    bot.answer_callback_query(call.id, show_alert = False)
@bot.callback_query_handler(func=lambda c: c.data == 'Apple')
def Apple(call):
    to_cart(call.from_user.id,100*margin,"Слойка с яблоком")
    bot.answer_callback_query(call.id, show_alert = False)
@bot.callback_query_handler(func=lambda c: c.data == 'Blueberry')
def Blueberry(call):
    to_cart(call.from_user.id,100*margin,"Слойка с голубикой")
    bot.answer_callback_query(call.id, show_alert = False)
@bot.callback_query_handler(func=lambda c: c.data == 'Menu')
def Menu(call):
    markup = types.InlineKeyboardMarkup()

    key_fast_menu = types.InlineKeyboardButton(text='🍽️ Быстрое Меню', callback_data="Fast_menu")
    key_cart = types.InlineKeyboardButton(text='🛒 Корзина', callback_data="Сart")
    key_long_menu = types.InlineKeyboardButton(text='📋 Долгое меню', callback_data="Long_menu")

    markup.row(key_fast_menu)
    markup.row(key_cart)
    markup.row(key_long_menu)

    bot.edit_message_caption(chat_id=call.from_user.id, message_id=call.message.id,
                             caption='Из быстрого меню можно добавить товары в корзину,\n для заказа товаров которых нет в быстром меню нажмите: "Долгое меню"',
                             reply_markup=markup)


# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     user_id = call.from_user.id
#     message_id = call.message.id
#     if call.data == "Сart":
#         markup = types.InlineKeyboardMarkup()
#         key_paying = types.InlineKeyboardButton(text='💸 Оплатить', callback_data="Paying")
#         key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Menu")
#         markup.row(key_paying,key_back)
#         bot.edit_message_caption(chat_id=user_id, message_id = call.message.id,caption= "<pre>"+draw_cart(shopping_cart)+"</pre>",
#                                  reply_markup=markup,parse_mode="html")
#         #print(draw_cart(shopping_cart))
#     elif call.data == "Fast_menu" or call.data == "Back":
#         ...
#     elif call.data == "Drinks":
#         markup = types.InlineKeyboardMarkup()
#
#         key_cola = types.InlineKeyboardButton(text='🥤 Кола', callback_data="Cola")
#         key_water = types.InlineKeyboardButton(text='💧 Вода', callback_data="Water")
#         key_juice = types.InlineKeyboardButton(text='🧃 Сок', callback_data="Juice")
#         key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Back")
#
#         markup.row(key_cola)
#         markup.row(key_water)
#         markup.row(key_juice)
#         markup.row(key_back)
#
#         bot.edit_message_caption(chat_id=user_id, message_id= message_id, caption="Выберите товар, затем спецификацию:", reply_markup=markup)
#     elif call.data == "Cola":
#         markup = types.InlineKeyboardMarkup()
#
#         key_kind_cola = types.InlineKeyboardButton(text='🥤 Добрый кола', callback_data="Kind_cola")
#         key_kind_cola_zero = types.InlineKeyboardButton(text='🥤 Добрый кола зеро', callback_data="Kind_cola_zero")
#         key_black_cola = types.InlineKeyboardButton(text='🥤 Кола черноголовка', callback_data="Black_cola")
#         key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Back")
#
#         markup.row(key_kind_cola)
#         markup.row(key_kind_cola_zero)
#         markup.row(key_black_cola)
#         markup.row(key_back)
#
#         bot.edit_message_caption(chat_id=user_id, message_id=message_id,
#                                  caption="Пейте без остановки колу из черноголовки\nНажмите чтобы добавить товар в корзину:",
#                                  reply_markup=markup)
#
#     elif call.data == "Kind_cola":
#         to_cart(user_id, 100 * margin, "Добрый кола")
#     elif call.data == "Kind_cola_zero":
#         to_cart(call.from_user.id, 100 * margin, "Добрый кола зеро")
#     elif call.data == "Black_cola":
#         to_cart(call.from_user.id, 100 * margin, "Кола черноголовка")
#     elif call.data == "Water":
#         markup = types.InlineKeyboardMarkup()
#
#         key_still_water = types.InlineKeyboardButton(text='💦 Вода still', callback_data="Still")
#         key_sparkling_water = types.InlineKeyboardButton(text='💦 Вода sparkling', callback_data="Sparkling")
#         key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Back")
#
#         markup.row(key_still_water)
#         markup.row(key_sparkling_water)
#         markup.row(key_back)
#
#         bot.edit_message_caption(chat_id=user_id, message_id=message_id,
#                                  caption="Это стил вотер, стил вотер\nНажмите чтобы добавить товар в корзину:",
#                                  reply_markup=markup)
#     elif call.data == "Still":
#         to_cart(call.from_user.id, 100 * margin, "Вода still")
#     elif call.data == "Sparkling":
#         to_cart(call.from_user.id, 100 * margin, "Вода sparkling")
#
#     elif call.data == "Juice":
#         markup = types.InlineKeyboardMarkup()
#
#         key_orange_juice = types.InlineKeyboardButton(text='🧃 Апельсиновый сок', callback_data="Orange_juice")
#         key_apple_juice = types.InlineKeyboardButton(text='🧃 Яблочный сок', callback_data="Apple_juice")
#         key_random_juice = types.InlineKeyboardButton(text='🧃 Рандомный сок нахуй', callback_data="Random_juice")
#         key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Back")
#
#         markup.row(key_orange_juice)
#         markup.row(key_apple_juice)
#         markup.row(key_random_juice)
#         markup.row(key_back)
#
#         bot.edit_message_caption(chat_id=user_id, message_id=message_id,
#                                  caption="Пейте без остановки колу из черноголовки\nНажмите чтобы добавить товар в корзину:",
#                                  reply_markup=markup)
#
#     elif call.data == "Orange_juice":
#         to_cart(user_id, 100 * margin, "Апельсиновый сок")
#     elif call.data == "Apple_juice":
#         to_cart(user_id, 100 * margin, "Яблочный сок")
#     elif call.data == "Random_juice":
#         to_cart(user_id, 100 * margin, "Рандомный сок")
#
#     if call.data == "Eats":
#         markup = types.InlineKeyboardMarkup()
#
#         key_onigiri = types.InlineKeyboardButton(text='🍙 Онигири', callback_data="Onigiri")
#         key_pizza = types.InlineKeyboardButton(text='🍕 Пицца', callback_data="Pizza")
#         key_bun = types.InlineKeyboardButton(text='🥐 Слойка с ...', callback_data="Bun")
#         key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Back")
#
#         markup.row(key_onigiri)
#         markup.row(key_pizza)
#         markup.row(key_bun)
#         markup.row(key_back)
#
#         bot.edit_message_caption(chat_id=user_id, message_id= message_id, caption="Выберите товар, затем спецификацию:", reply_markup=markup)
#
#     elif call.data == "Onigiri":
#         markup = types.InlineKeyboardMarkup()
#
#         key_onigiri_shrimp = types.InlineKeyboardButton(text='🍙 Онигири с Креветкой', callback_data="Shrimp")
#         key_onigiri_gentle = types.InlineKeyboardButton(text='🍙 Онигири Нежный', callback_data="Gentle")
#         key_onigiri_philadelphia = types.InlineKeyboardButton(text='🍙 Онигири Филадельфия', callback_data="Philadelphia")
#         key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Back")
#
#         markup.row(key_onigiri_shrimp)
#         markup.row(key_onigiri_gentle)
#         markup.row(key_onigiri_philadelphia)
#         markup.row(key_back)
#
#         bot.edit_message_caption(chat_id=user_id, message_id=message_id,
#                                  caption="Нажмите чтобы добавить товар в корзину:",
#                                  reply_markup=markup)
#
#     elif call.data == "Shrimp":
#         to_cart(call.from_user.id, 100 * margin, "Онигири с Креветкой")
#     elif call.data == "Gentle":
#         to_cart(call.from_user.id,100*margin,"Онигири Нежный")
#     elif call.data == "Philadelphia":
#         to_cart(call.from_user.id,100*margin,"Онигири Филадельфия")
#     elif call.data == "Pizza":
#         markup = types.InlineKeyboardMarkup()
#
#         key_pizza = types.InlineKeyboardButton(text='🍕 Пицца', callback_data="Pizza_Cart")
#         key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Back")
#
#         markup.row(key_pizza)
#         markup.row(key_back)
#
#         bot.edit_message_caption(chat_id=user_id, message_id=message_id,
#                                  caption="Нажмите чтобы добавить товар в корзину:",
#                                  reply_markup=markup)
#
#     elif call.data == "Pizza_Cart":
#         to_cart(user_id,100*margin,"Пицца")
#
#     elif call.data == "Bun":
#         markup = types.InlineKeyboardMarkup()
#
#         key_bun_cherry = types.InlineKeyboardButton(text='🥐 Слойка с вишней', callback_data="Cherry")
#         key_bun_apple = types.InlineKeyboardButton(text='🥐 Слойка с яблоком', callback_data="Apple")
#         key_bun_blueberry = types.InlineKeyboardButton(text='🥐 Слойка с голубикой', callback_data="Blueberry")
#         key_back = types.InlineKeyboardButton(text='❌ Назад', callback_data="Back")
#
#         markup.row(key_bun_cherry)
#         markup.row(key_bun_apple)
#         markup.row(key_bun_blueberry)
#         markup.row(key_back)
#
#         bot.edit_message_caption(chat_id=user_id, message_id=message_id, caption="Мои руки как слойка с вишней...\nЕсли нужной слойки не будет она будет заменена на любую слойку без творога\nНажмите чтобы добавить товар в корзину:",
#                                  reply_markup=markup)
#
#     elif call.data == "Cherry":
#         to_cart(call.from_user.id,100*margin,"Слойка с вишней")
#     elif call.data == "Apple":
#         to_cart(call.from_user.id,100*margin,"Слойка с яблоком")
#     elif call.data == "Blueberry":
#         to_cart(call.from_user.id,100*margin,"Слойка с голубикой")
#
#
#     if call.data == "Menu":
#         markup = types.InlineKeyboardMarkup()
#
#         key_fast_menu = types.InlineKeyboardButton(text='🍽️ Быстрое Меню', callback_data="Fast_menu")
#         key_cart = types.InlineKeyboardButton(text='🛒 Корзина', callback_data="Сart")
#         key_long_menu = types.InlineKeyboardButton(text='📋 Долгое меню', callback_data="Long_menu")
#
#         markup.row(key_fast_menu)
#         markup.row(key_cart)
#         markup.row(key_long_menu)
#
#         bot.edit_message_caption(chat_id=user_id, message_id=message_id, caption='Из быстрого меню можно добавить товары в корзину,\n для заказа товаров которых нет в быстром меню нажмите: "Долгое меню"',
#                                  reply_markup=markup)
#
#     elif call.data == "Kill_browser":
#         ...













bot.polling(none_stop=True, interval=0)
