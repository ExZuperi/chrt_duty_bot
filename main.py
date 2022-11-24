import requests.exceptions
import telebot
from Database import *
from telebot import types

bot = telebot.TeleBot("")
myId = 457037353
historyGroupId = -1001642646649


@bot.message_handler(commands=["start"])
def start(message):
    try:
        get_who_am_i(message.chat.id)[0][1]

        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        item_duty = types.KeyboardButton("Назначить дежурных")
        item_rate = types.KeyboardButton("Рейтинг дежурств")
        item_profile = types.KeyboardButton("Мой профиль")
        item_duty_add = types.KeyboardButton("Поставить мне дежурство")

        markup_reply.add(item_duty_add, item_rate, item_profile, item_duty)

        bot.send_message(message.chat.id,
                         "Привет! Этого бота разработал @ExStaroth\n\nТы можешь спокойно распространять бота в том или ином виде, но с указанием моего авторства)",
                         reply_markup=markup_reply)
    except IndexError as error:
        bot.send_message(message.chat.id,
                         "Вас нет в списке бота, если произошла ужасная ошибка, Вы можете написать мне @ExStaroth")
        print(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    global rez, amount, group

    markup_inline = types.InlineKeyboardMarkup()

    def send_list_of_duty():
        global names
        names = ""
        for i in range(amount):
            names += rez[i][4] + " "
            item_cant = types.InlineKeyboardButton(text=f"{rez[i][4]} занят", callback_data=f"{rez[i][0]}" + f"{group}")
            markup_inline.add(item_cant)

        item_accept_list = types.InlineKeyboardButton(text="Готово", callback_data="accept_duty_list")
        markup_inline.add(item_accept_list)

        bot.send_message(call.message.chat.id, f"Дежурные/й - {names}", reply_markup=markup_inline)

    try:
        if (call.data == "1" or call.data == "2" or call.data == "3"
                or call.data == "4" or call.data == "5" or call.data == "6"):
            amount = int(call.data)

            item_first = types.InlineKeyboardButton(text="Первая", callback_data="11")
            item_second = types.InlineKeyboardButton(text="Вторая", callback_data="12")
            item_lonely = types.InlineKeyboardButton(text="Нет", callback_data="lonely")
            markup_inline.add(item_first, item_second, item_lonely)

            bot.send_message(call.message.chat.id,
                             "Самый лучший\n Нужна определённая группа?",
                             reply_markup=markup_inline)

        if (call.data == "11" or call.data == "12"):
            group = int(call.data[1])
            rez = get_choose_from_group(amount, group)
            send_list_of_duty()

        if (call.data == "lonely"):
            group = 0
            rez = get_choose_from_all(amount)
            send_list_of_duty()

        # Кто-то не может
        if (9 < len(call.data) < 12):
            who_cant_duty = int(call.data[:-1])
            set_priority_plus_one(who_cant_duty)
            bot.edit_message_text(text="Подберём других...", chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
            if call.data[-1] == "0":  # Если группы нет
                rez = get_choose_from_all(amount)
                send_list_of_duty()
            else:  # Если группа есть
                rez = get_choose_from_group(amount, group)
                send_list_of_duty()

        if (call.data == "accept_duty_list"):
            if group == 0:
                item_reject_list_lonely = types.InlineKeyboardButton(text="Назад", callback_data="lonely")
                markup_inline.add(item_reject_list_lonely)

            else:
                group += 10  # из call-data вычитается 10 чтобы не путать с количеством человек

                item_reject_list_group = types.InlineKeyboardButton(text="Назад", callback_data=f"{str(group)}")
                markup_inline.add(item_reject_list_group)

            item_accept = types.InlineKeyboardButton(text="Подтвердить", callback_data="accept")
            markup_inline.add(item_accept)

            bot.send_message(call.message.chat.id,
                             f"Нажми на кнопку 'Подтвердить', когда {names} отдежурят",
                             reply_markup=markup_inline)

        if (call.data == "accept"):
            set_priority_to_zero()
            bot.send_message(historyGroupId,
                             text=f'{get_who_am_i(call.message.chat.id)[0][0]} поставил дежурства для: {names}')
            for i in range(amount):
                set_circles(rez[i][0])
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="Принято!")
            bot.send_message(call.message.chat.id, text="Дежурства проставлены. Спасибо!")
    except NameError as error:  # Ошибка перезапуска
        bot.send_message(call.message.chat.id,
                         text='Произошла ошибка из-за того что бот перезапускался, проставьте дежурства вручную или перезапустите меня командой /start')

    # Принимаем запрос TODO Ошибка перезапуска почему-то нет?
    if (len(call.data) == 18 or len(call.data) == 20):
        if len(call.data) == 18:
            good_person = int(call.data[:-9])
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=f"Принято! Для {get_who_am_i(good_person)[0][0]} БУДЕТ проставлено дежурство")
            set_circles(good_person)
            bot.send_photo(good_person, 'https://i.ibb.co/6mYvDBN/kitajskie-memy-1.jpg',
                           caption='Парень Иван город Тверь молодец! Вам проставлено дежурство')
        elif len(call.data) == 20:
            good_person = int(call.data[:-10])
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=f"Принято! Для {get_who_am_i(good_person)[0][0]} БУДЕТ проставлено дежурство")
            set_circles(good_person)
            bot.send_photo(good_person, 'https://i.ibb.co/6mYvDBN/kitajskie-memy-1.jpg',
                           caption='Парень Иван город Тверь молодец! Вам проставлено дежурство')

    # Отклоняем запрос
    if (len(call.data) == 27 or len(call.data) == 30):
        if len(call.data) == 27:
            bad_person = int(call.data[:-18])
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=f"Принято! Для {get_who_am_i(bad_person)[0][0]} НЕ будет поставлено дежурство.")
            bot.send_photo(bad_person, 'https://i.ibb.co/zFm3zvj/Powd-Vg9-X-t-A.jpg',
                           caption='О нет! Вы обмануть верховный лидер')
        elif len(call.data) == 30:
            bad_person = int(call.data[:-20])
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=f"Принято! Для {get_who_am_i(bad_person)[0][0]} НЕ будет поставлено дежурство.")
            bot.send_photo(bad_person, 'https://i.ibb.co/zFm3zvj/Powd-Vg9-X-t-A.jpg',
                           caption='О нет! Вы обмануть верховный лидер')


@bot.message_handler(content_types='text')
def message_reply(message):
    try:
        person = get_who_am_i(message.chat.id)
        person[0][1]
        # Проверка на наличие в бд, хотел еще вынести сюда все итемы, но при любом тексте хендлер будет вызываться, так что оставил только инлайн и юзера
        markup_inline = types.InlineKeyboardMarkup()

        if message.text == "Назначить дежурных":
            item_one = types.InlineKeyboardButton(text="1", callback_data="1")
            item_two = types.InlineKeyboardButton(text="2", callback_data="2")
            item_three = types.InlineKeyboardButton(text="3", callback_data="3")
            item_four = types.InlineKeyboardButton(text="4", callback_data="4")
            item_five = types.InlineKeyboardButton(text="5", callback_data="5")
            item_six = types.InlineKeyboardButton(text="6", callback_data="6")

            markup_inline.add(item_one, item_two, item_three, item_four, item_five, item_six)
            bot.send_message(message.chat.id,
                             "Сколько дежурных нужно?",
                             reply_markup=markup_inline)

        if message.text == "Мой профиль":
            bot.send_message(message.chat.id,
                             f"Вы - {person[0][0]} \n\nКоличество ваших дежурств - {person[0][1]} \n\nВаша группа - {person[0][2]}")

        if message.text == "Рейтинг дежурств":
            rate = get_rate()
            text = ''
            for i in range(27):
                text += f"{rate[i][0]} - {rate[i][1]}\n"
            bot.send_message(message.chat.id,
                             f"{text}")

        if message.text == "Поставить мне дежурство":
            bot.send_message(message.chat.id,
                             "Вам будет добавлено дежурство, когда @ExStaroth или @polyaaars это подтвердят.")

            item_accept = types.InlineKeyboardButton(text="Поставить", callback_data=f"{str(message.chat.id)}" * 2)
            item_decline = types.InlineKeyboardButton(text="Отклонить", callback_data=f"{message.chat.id}" * 3)

            markup_inline.add(item_accept, item_decline)

            bot.send_message(historyGroupId,
                             f"{person[0][0]} хочет чтобы ему поставили дежурство.",
                             reply_markup=markup_inline)

    except IndexError as error:
        bot.send_message(message.chat.id,
                         "Вас нет в списке бота, если произошла ужасная ошибка, Вы можете написать мне @ExZuperi")


try:
    bot.polling(none_stop=True, interval=0)
except:
    print("Произошла ошибка, но я все восстановил")
    continue

# TODO Сделать что если приоритет 2 отправлялось сообщение о том что по 2 кругу?
# TODO Можно: Дата последнего дежурства
