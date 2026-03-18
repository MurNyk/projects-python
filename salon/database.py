import sqlite3
import datetime


class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.insert_user("1", "1")

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                password TEXT NOT NULL
                                )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
                            id INTEGER PRIMARY KEY,
                            ticket_number TEXT NOT NULL,
                            client TEXT NOT NULL,
                            pol TEXT NOT NULL,
                            phone TEXT NOT NULL,
                            service TEXT NOT NULL,
                            status TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            completion_date TIMESTAMP
                                )''')

    def ticket_number_exists(self, ticket_number):
        self.cursor.execute(
            "SELECT 1 FROM tickets WHERE ticket_number=?", (ticket_number,))
        return self.cursor.fetchone() is not None

    def insert_user(self, username, password):
        self.cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

    def check_credentials(self, username, password):
        self.cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return self.cursor.fetchone() is not None

    def insert_ticket(self, ticket_data):
        created_at = ticket_data.get(
            'created_at', datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
        completion_date = ticket_data.get('completion_date', None)
        self.cursor.execute("INSERT INTO tickets (ticket_number, client, pol, phone, service, status, created_at, completion_date) VALUES (?,?,?,?,?,?,?,?)",
                            (ticket_data['ticket_number'], ticket_data['client'], ticket_data['pol'], ticket_data['phone'], ticket_data['service'], ticket_data['status'], created_at, completion_date))
        self.conn.commit()

    def update_ticket(self, ticket_id, ticket_data):
        query = """
            UPDATE tickets
            SET ticket_number=?,
            client=?,
            phone=?,
            service=?,
            pol=?,
            status=?,
            completion_date=?
        WHERE id=?
    """

        values = [
            ticket_data.get('ticket_number', None),
            ticket_data.get('client', None),
            ticket_data.get('phone', None),
            ticket_data.get('service', None),
            ticket_data.get('pol', None),
            ticket_data.get('status', None),
            ticket_data.get('completion_date', None),
            ticket_id
        ]

        self.cursor.execute(query, values)
        self.conn.commit()


    def get_tickets_by_client_and_service(self, client_name, service):
        self.cursor.execute("SELECT * FROM tickets WHERE client =? AND service =?", (client_name, service))
        return self.cursor.fetchall()

    def search_tickets_by_client(self, client_name):
        query = "SELECT * FROM tickets WHERE 1=1"
        params = []

        if client_name:
            query += " AND client = ?"
            params.append(client_name)

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def delete_ticket(self, ticket_id):
        self.cursor.execute("DELETE FROM tickets WHERE id=?", (ticket_id,))
        self.conn.commit()

    def get_latest_ticket(self):
        self.cursor.execute("SELECT * FROM tickets ORDER BY id DESC LIMIT 1")
        return self.cursor.fetchone()

    def get_all_tickets(self):
        self.cursor.execute("SELECT * FROM tickets")
        return self.cursor.fetchall()

    def get_ticket_by_id(self, ticket_id):
        self.cursor.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,))
        return self.cursor.fetchone()

    def search_tickets(self, query):
        self.cursor.execute("SELECT * FROM tickets WHERE ticket_number LIKE ? OR client LIKE ? OR phone LIKE ?",
                            ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
        return self.cursor.fetchall()

    def get_tickets_by_service(self, service):
        self.cursor.execute(
            "SELECT * FROM tickets WHERE service=?", (service,))
        return self.cursor.fetchall()

    def get_tickets_by_gender(self, gender):
        self.cursor.execute("SELECT * FROM tickets WHERE pol=?", (gender,))
        return self.cursor.fetchall()

    def get_tickets_by_date_range(self, date_from, date_to):
        self.cursor.execute(
            "SELECT * FROM tickets WHERE created_at BETWEEN? AND?", (date_from, date_to))
        return self.cursor.fetchall()

    def delete_all_tickets(self):
        self.cursor.execute("DELETE FROM tickets")
        self.conn.commit()

    def get_tickets_by_client(self, client_name):
        tickets = self.get_all_tickets()
        return [ticket for ticket in tickets if ticket[2] == client_name]

    def __del__(self):
        self.conn.close()
