import sqlite3

Database = sqlite3.connect('users.db', check_same_thread=False)
cur = Database.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
   userid INT PRIMARY KEY,
   circles INT,
   priority INT,
   in_group INT,
   name TEXT);
""")
Database.commit()


def get_choose_from_group(amount, group):
    cur.execute(
        f"SELECT * FROM users WHERE in_group = {group} ORDER BY priority, circles LIMIT {amount}")
    pretender = cur.fetchall()
    return pretender


def get_choose_from_all(amount):
    cur.execute(f"SELECT * FROM users ORDER BY priority, circles LIMIT {amount}")
    pretender = cur.fetchall()
    return pretender


def get_who_am_i(user_id):
    cur.execute(f"SELECT name, circles, in_group FROM users WHERE userid = {user_id}")
    who = cur.fetchall()
    return who


def get_rate():
    cur.execute("SELECT name, circles FROM users ORDER BY circles DESC")
    rate = cur.fetchall()
    return rate


def set_another_one(user_id):
    cur.execute(f"UPDATE users SET priority = priority + 1 WHERE userid = {user_id}")
    Database.commit()


def set_priority_to_zero():
    cur.execute("UPDATE users SET priority = 0 WHERE priority > 0")
    Database.commit()


def set_circles(user_id):
    cur.execute(f"UPDATE users SET circles = circles + 1 WHERE userid = {user_id}")
    Database.commit()
