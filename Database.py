import sqlite3

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

def set_another_one(user_id):
    cur.execute(f"UPDATE users SET priority = priority + 1 WHERE userid = {user_id}")
    Database.commit()


def set_priority_to_zero():
    cur.execute("UPDATE users SET priority = 0 WHERE priority > 0")
    Database.commit()


def set_priority_to_max(user_id):
    cur.execute(f"UPDATE users SET priority = priority + 9999 WHERE userid = {user_id}")
    Database.commit()


def set_priority_to_last():
    cur.execute(f"UPDATE users SET priority = priority - 9999 WHERE priority > 9998")
    Database.commit()


def get_choose_from_group(amount, group): #TODO костыль?
    cur.execute(
        f"SELECT * FROM users WHERE in_group = {group} ORDER BY priority, circles LIMIT {amount}")
    pretender = cur.fetchall()

    for i in range(len(pretender)):
        if pretender[i][5] != 0:
            cur.execute(
                f"SELECT * FROM users WHERE in_group = {group} AND priorityDuty = {pretender[i][5]} AND priority = {pretender[i][2]} ORDER BY circles LIMIT {amount - 1}")
            prerez = cur.fetchall()
            #Выбираем ему подобных и уменьшаем количество также ставим приоритет выбранным, чтобы их не задело снова
            amount -= len(prerez)
            for j in range(len(prerez)):
                set_priority_to_max(prerez[j][0])
            #Выбираем оставшихся
            cur.execute(
                f"SELECT * FROM users WHERE in_group = {group} ORDER BY priority, circles LIMIT {amount}")
            pretender = cur.fetchall()
            #Убираем приоритеты после выбора и объединяем листы
            set_priority_to_last()
            pretender.extend(prerez)
            return pretender
    #Если нет тех кто хочет дежурить вместе
    return pretender


def get_choose_from_all(amount):
    cur.execute(f"SELECT * FROM users ORDER BY priority, circles LIMIT {amount}")
    pretender = cur.fetchall()

    for i in range(len(pretender)):
        if pretender[i][5] != 0:
            cur.execute(
                f"SELECT * FROM users WHERE priorityDuty = {pretender[i][5]} AND priority = {pretender[i][2]} ORDER BY circles LIMIT {amount - 1}")
            prerez = cur.fetchall()
            #Выбираем ему подобных и уменьшаем количество также ставим приоритет выбранным, чтобы их не задело снова
            amount -= len(prerez)
            for j in range(len(prerez)):
                set_priority_to_max(prerez[j][0])
            #Выбираем оставшихся
            cur.execute(
                f"SELECT * FROM users ORDER BY priority, circles LIMIT {amount}")
            pretender = cur.fetchall()
            #Убираем приоритеты после выбора и объединяем листы
            set_priority_to_last()
            pretender.extend(prerez)
            return pretender
    #Если нет тех кто хочет дежурить вместе
    return pretender


def get_who_am_i(user_id):
    cur.execute(f"SELECT name, circles, in_group FROM users WHERE userid = {user_id}")
    who = cur.fetchall()
    return who


def get_priority_duty():
    cur.execute("SELECT priorityDuty FROM users ")


def get_rate():
    cur.execute("SELECT name, circles FROM users ORDER BY circles DESC")
    rate = cur.fetchall()
    return rate


def get_minimal_priority(group):
    if group == 0:
        cur.execute("SELECT min(priority) FROM users")
        rate = cur.fetchall()#TODO IDK HOW
    else:
        cur.execute(f"SELECT min(priority) FROM users WHERE group = {group}")
        rate = cur.fetchall()
    return rate[0][0]


def set_circles(user_id):
    cur.execute(f"UPDATE users SET circles = circles + 1 WHERE userid = {user_id}")
    Database.commit()
