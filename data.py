import sqlite3


class Database:

    def __init__(self, file_db):
        self.connection = sqlite3.connect(file_db)
        self.cursor = self.connection.cursor()

    def add_user_id_and_name(self, user_id, user_name):
        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id, user_name) VALUES (?, ?)", (user_id, user_name))

    def user_exist(self, user_id):
        with self.connection:
            # Выполняем SQL-запрос
            self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            count = len(self.cursor.fetchall())
            # Проверяем, есть ли пользователь с данным user_id
            return 0 < count == 1

    def check_data_buy(self, user_id):
        with self.connection:
            data = self.cursor.execute("SELECT data_buy FROM users WHERE user_id = ?", (user_id,)).fetchone()
        if data[0] is not None:
            return data[0]
        else:
            print("data_buy is None")

    def update_data_buy(self, user_id, new_data):
        with self.connection:
            self.cursor.execute("UPDATE users SET data_buy = ? WHERE user_id = ?", (new_data, user_id))
            print("Дата обновлена!")

    def check_price(self, name_goods):
        with self.connection:
            price = self.cursor.execute("SELECT price FROM price WHERE goods = ?", (name_goods,)).fetchone()
        return price[0]

    def check_price_with_data(self, data):
        with self.connection:
            price = self.cursor.execute("SELECT price FROM price WHERE data = ?", (data,)).fetchone()
        return price[0]

    def check_goods_with_data(self, data):
        with self.connection:
            goods = self.cursor.execute("SELECT goods FROM price WHERE data = ?", (data,)).fetchone()
        return goods[0]

    def update_price(self, name_goods, new_price):
        with self.connection:
            self.cursor.execute("UPDATE price SET price = ? WHERE goods = ?", (new_price, name_goods))
            print("Цена обновлена!")

    def admin_status_on(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users SET admin_status = ? WHERE user_id = ?", ("true", user_id))

    def check_admin_status(self, user_id):
        with self.connection:
            admin_status = self.cursor.execute("SELECT admin_status FROM users WHERE user_id = ?",
                                               (user_id,)).fetchone()

            if admin_status is not None:
                if admin_status[0] == "true":
                    print("admin_status = true")
                    return True
                elif admin_status[0] == "false":
                    print("admin_status = false")
                    return False
            else:
                print("admin_status = None")

    def add_data_to_goods(self, user_id, goods_name, goods_cost, screensh, user_name):
        with self.connection:
            self.cursor.execute("INSERT INTO goods (user_id,    user_name, goods_name, cost, screenshot) VALUES (?, "
                                "?, ?,?,?)",
                                (user_id, user_name, goods_name, goods_cost, screensh))

    def get_id(self):
        with self.connection:
            ID = self.cursor.execute("SELECT id FROM goods").fetchone()
            return ID[0]

    def get_goods_by_id(self, goods_id):
        with self.connection:
            goods_data = self.cursor.execute(
                "SELECT user_id, user_name, goods_name, screenshot, cost FROM goods WHERE id = ?",
                (goods_id,)).fetchone()
            return goods_data

    def del_goods_by_id(self, goods_id):
        with self.connection:
            self.cursor.execute(
                "DELETE FROM goods WHERE id = ?", (goods_id,))

    def add_to_approved_goods(self, user_id, user_name, goods_name, screensh, goods_cost):
        with self.connection:
            self.cursor.execute("INSERT INTO approved_goods (user_id, user_name, goods_name, cost, screenshot) VALUES "
                                "(?,?,?,?,?)",
                                (user_id, user_name, goods_name, goods_cost, screensh))

    def get_subs_code_by_data(self, data):
        with self.connection:
            result = self.cursor.execute("SELECT code FROM subscribes_codes WHERE data = ?", (data,)).fetchone()
            print(result)
            if result is not None:
                return result[0]
            else:
                return "Нет данной подписки"

    def del_subs_code_by_code(self, code):
        with self.connection:
            print("code = ", code)
            self.cursor.execute("DELETE FROM subscribes_codes WHERE code = ?", (code,))

    def add_ne_hvatilo_subs(self, user_id, data):
        with self.cursor.connection:
            self.cursor.execute("INSERT INTO dont_hvatilo_potpisok (user_id, data) VALUES "
                                "(?,?)",
                                (user_id, data))

    def count_ne_hvatilo(self):
        with self.cursor.connection:
            self.cursor.execute("SELECT COUNT(*) FROM dont_hvatilo_potpisok")
            row_count = self.cursor.fetchone()[0]
            return row_count

    def get_all_admin_status(self):
        with self.cursor.connection:
            all_admins = self.cursor.execute("SELECT user_id FROM users WHERE admin_status = ?", ('true',)).fetchall()
            return all_admins

    def get_10_feedback(self):
        with self.cursor.connection:
            all_feed = self.cursor.execute('SELECT * FROM feedback ORDER BY id DESC LIMIT 10')
            last_10_records = all_feed.fetchall()
            if not last_10_records:
                return "ПУСТО"
            else:
                return last_10_records

    def add_feedback(self, user_id=None, user_name=None, feedback=None, screen=None):
        with self.cursor.connection:
            result = self.cursor.execute("SELECT * FROM feed").fetchone()
            self.cursor.execute("INSERT INTO feedback (user_id,user_name,feedback, screen) VALUES (?,?,?,?)",
                              (result[1], result[2], result[3], result[4]))

    def add_feed(self, user_id=None, user_name=None, feedback=None, screen=None):
        with self.cursor.connection:
            self.cursor.execute("INSERT INTO feed (user_id,user_name,feedback,screen) VALUES (?,?,?,?)",
                                (user_id, user_name, feedback, screen))

    def update_feed_scr(self, user_id, screen):
        with self.cursor.connection:
            self.cursor.execute("UPDATE feed SET screen = ? WHERE user_id = ?", (screen, user_id))

    def update_feed(self, user_id, feedback):
        with self.cursor.connection:
            self.cursor.execute("UPDATE feed SET feedback = ? WHERE user_id = ?", (feedback, user_id))

    def del_feed_by_user_id(self, user_id):
        with self.cursor.connection:
            self.cursor.execute("DELETE FROM feed WHERE user_id = ?", (user_id,))
