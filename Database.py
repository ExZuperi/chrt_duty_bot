import sqlite3

import main

Database = sqlite3.connect('users.db', check_same_thread=False)
cur = Database.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
   userid INT PRIMARY KEY,
   circles INT,
   priority INT,
   in_group INT,
   name TEXT,
   priorityDuty);
""")
Database.commit()


def set_priority_plus_one(user_id):
    cur.execute(f"UPDATE users SET priority = priority + 1 WHERE userid = {user_id}")
    Database.commit()


def set_priority_to_zero():
    cur.execute("UPDATE users SET priority = 0 WHERE priority > 0")
    Database.commit()


def set_priority_to_zero_for_user(user_id):
    cur.execute(f"UPDATE users SET priority = 0 WHERE userid = {user_id}")
    Database.commit()


def set_priority_to_max(user_id):
    cur.execute(f"UPDATE users SET priority = priority + 9999 WHERE userid = {user_id}")
    Database.commit()


def set_priority_to_last():
    cur.execute(f"UPDATE users SET priority = priority - 9999 WHERE priority > 9998")
    Database.commit()


def get_choose_from_group(amount, group):  # TODO костыль?
    cur.execute(
        f"SELECT * FROM users WHERE in_group = {group} ORDER BY priority, circles LIMIT {amount}")
    pretender = cur.fetchall()

    for i in range(len(pretender)):
        if pretender[i][5] != 0:
            cur.execute(
                f"SELECT * FROM users WHERE in_group = {group} AND priorityDuty = {pretender[i][5]} AND priority = {pretender[i][2]} ORDER BY circles LIMIT {amount}")
            two_pretenders = cur.fetchall()
            if len(two_pretenders) < 2:
                set_priority_plus_one(two_pretenders[0][0])  # TODO : Bug when another group his member / NoneFix mb
                return get_choose_from_group(amount, group)
            else:
                amount -= 2
                two_pretenders.extend(get_choose_from_group(amount, group))  # TODO: Rename
                return two_pretenders
    return pretender


def get_choose_from_all(amount):
    cur.execute(f"SELECT * FROM users ORDER BY priority, circles LIMIT {amount}")
    pretender = cur.fetchall()

    for i in range(len(pretender)):
        if pretender[i][5] != 0:
            cur.execute(
                f"SELECT * FROM users WHERE priorityDuty = {pretender[i][5]} AND priority = {pretender[i][2]} ORDER BY circles LIMIT {amount}")
            two_pretenders = cur.fetchall()
            if len(two_pretenders) < 2:
                set_priority_plus_one(two_pretenders[0][0])  # TODO : Bug when another group his member / NoneFix mb
                return get_choose_from_all(amount)
            else:
                amount -= 2
                two_pretenders.extend(get_choose_from_all(amount))  # TODO: Rename
                return two_pretenders
    return pretender


def get_who_am_i(user_id):
    try:
        cur.execute(f"SELECT name, circles, in_group FROM users WHERE userid = {user_id}")
        who = cur.fetchall()
        return who
    except sqlite3.ProgrammingError as e:
        main.bot.send_message(user_id, "Вы вызвали ошибку. Вопрос: Как? Напишите мне, Вы - звезда")


def get_priority_duty():
    cur.execute("SELECT priorityDuty FROM users ")


def get_rate():
    cur.execute("SELECT name, circles FROM users ORDER BY circles DESC")
    rate = cur.fetchall()
    return rate


def set_circles(user_id):
    cur.execute(f"UPDATE users SET circles = circles + 1 WHERE userid = {user_id}")
    Database.commit()
