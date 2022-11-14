import pymysql

# Variables para la conexion a la base de datos
HOST = 'database-crud.cc79gsfunagy.us-east-1.rds.amazonaws.com'
USER = 'admin'
PASS = 'admin1234'
PORT = 3306
DATABASE = 'crud_flask'


class Database:
    def connect(self):
        return pymysql.connect(host=HOST, user=USER, password=PASS, db=DATABASE, port=PORT)

    def read(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            if id == None:
                cursor.execute("SELECT * FROM phone_book order by name asc")
            else:
                cursor.execute(
                    "SELECT * FROM phone_book WHERE id_account in (SELECT id FROM accounts) WHERE id = %s order by name asc", (id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def insert(self, data, id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO phone_book(name,phone,address, id_account) VALUES(%s, %s, %s)",
                           (data['name'], data['phone'], data['address'], id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def update(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("UPDATE phone_book set name = %s, phone = %s, address = %s where id = %s",
                           (data['name'], data['phone'], data['address'], id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def delete(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM phone_book where id = %s", (id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def login(self, usernam, password):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM accounts WHERE username = %s AND password = %s", (usernam, hash(password),))
            return cursor.fetchone()
        except:
            return ()
        finally:
            con.close()

    def register(self, username, email, password):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO accounts(username, email, password) VALUES(%s, %s, %s)",
                           (username, email, hash(password),))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def validate_if_account_exists(self, username, email):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute(
                "SELECT * FROM accounts where username = %s or email = %s", (username, email,))
            return cursor.fetchone()
        except:
            return ()
        finally:
            con.close()
