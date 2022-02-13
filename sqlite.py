import sqlite3
from datetime import datetime


class SQLite:

    def __init__(self, database_file):
        """ Подключаемся к БД """
        self.database = sqlite3.connect(database_file)
        self.cursor = self.database.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                user_id INT,
                username TEXT,
                referer TEXT,
                status INT, 
                warns INT,
                total_spend_time TEXT,
                time_register TEXT
            )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS rooms (
                room_id INT,
                first_user_id INT,
                second_user_id INT,
                started TEXT
            )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS queue (
                user_id INT,
                started TEXT
            )""")
        self.database.commit()

    def get_user_in_base(self, user_id):
        return self.cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'").fetchone()

    def get_user_in_queue(self, user_id):
        return self.cursor.execute(f"SELECT user_id FROM queue WHERE user_id = '{user_id}'").fetchone()

    def get_user_in_room(self, user_id):
        first_user = self.cursor.execute(f"SELECT first_user_id FROM rooms WHERE first_user_id = '{user_id}'").fetchone()
        second_user = self.cursor.execute(f"SELECT second_user_id FROM rooms WHERE second_user_id = '{user_id}'").fetchone()
        return [first_user, second_user]

    def get_room_mate_id(self, room_id, user_id):
        users_id = self.cursor.execute(f"SELECT first_user_id, second_user_id FROM rooms WHERE room_id = '{room_id}'").fetchall()
        return users_id[0][0] if user_id == users_id[0][1] else users_id[0][1]

    def get_queue(self):
        return self.cursor.execute(f"SELECT user_id FROM queue LIMIT 2").fetchall()

    def get_user_id_room(self, user_id):
        return self.cursor.execute(f"SELECT room_id FROM rooms WHERE first_user_id = '{user_id}' OR second_user_id = '{user_id}'").fetchone()

    def get_count_rooms(self):
        return self.cursor.execute(f"SELECT room_id FROM rooms").fetchall()

    def add_user_in_base(self, user_id, username):
        self.cursor.execute("INSERT INTO users "
                            "(`user_id`, `username`, `referer`, `status`, `warns`, `total_spend_time`, `time_register`) "
                            "VALUES (?,?,?,?,?,?,?)",
                            (user_id, username, 0, 1, 0, 0, datetime.now())
                            )
        self.database.commit()

    def add_user_in_queue(self, user_id):
        self.cursor.execute(f"INSERT INTO queue (`user_id`, `started`) VALUES (?,?)",
                            (user_id, datetime.now()))
        self.database.commit()

    def add_new_room(self, room_id, first_user_id, second_user_id):
        self.cursor.execute(f"INSERT INTO rooms (`room_id`, `first_user_id`, `second_user_id`, `started`) VALUES (?,?,?,?)",
                            (room_id, first_user_id, second_user_id, datetime.now()))
        self.database.commit()

    def delete_user_from_queue(self, user_id):
        self.cursor.execute(f"DELETE FROM queue WHERE user_id = '{user_id}'")
        self.database.commit()

    def delete_room(self, room_id):
        self.cursor.execute(f"DELETE FROM rooms WHERE room_id = '{room_id}'")
        self.database.commit()

    def close(self):
        self.database.close()
