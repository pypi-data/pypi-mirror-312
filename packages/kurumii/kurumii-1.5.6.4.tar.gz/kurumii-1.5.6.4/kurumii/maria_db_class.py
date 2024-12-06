import mariadb as mdb
from print_additions import *


class Database():
    def __init__(self):
        self.connections = {}
        self.current_connection = None

    def add_connection(self, user, password, host="localhost"):
        conn_params = {
            "user": user,
            "password": password,
            "host": host
        }
        try:
            connection = mdb.connect(**conn_params)
            print_green(f"Successfully connected as '{user}'")
        except mdb.OperationalError as e:
            print_warning(f"Failed to connect as '{user}': {e}")
            connection = None

        if connection:
            try:
                # Use single quotes inside f-string for the dictionary key
                self.connections[f"{conn_params['user']}"] = connection
                self.current_connection = connection
            except KeyError as e:
                print_red("Failed to add connection to connections dictionary")
                raise Exception("Failed to add connection") from e
        
        return connection
    def select_user(self, name):
        print(type(self.connections))
        for username, conn in self.connections.items():  
            print(type(conn))
            if username == name:
                self.current_connection = {"user":username,}
                print_green(f"Selected user: '{name}'")
                return conn
        print_warning(f"Connection not found{f", Current connection: '{self.current_connection}'" if self.current_connection != None else ""}")


db = Database()
db.add_connection(password="20190582",user="root")
db.add_connection(password="20190582",user="admin1")
print(db.current_connection.user)
print((db.connections))

db.select_user("root")
print(db.current_connection.user)