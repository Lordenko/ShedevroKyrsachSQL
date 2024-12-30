import pyodbc


class Database:
    def __init__(self, server, database, trusted=True):
        if trusted:
            self.conn_str = (
                f"Driver={{ODBC Driver 17 for SQL Server}};"
                f"Server={server};"
                f"Database={database};"
                f"Trusted_Connection=yes;"
            )
        else:
            pass
        self.conn = pyodbc.connect(self.conn_str)
        self.cursor = self.conn.cursor()

    def list_books(self):
        self.cursor.execute(
            "SELECT b.book_id, b.title, a.name, b.price, b.stock FROM Books b JOIN Authors a ON a.author_id=b.author_id;")
        return self.cursor.fetchall()

    def search_books_by_title(self, title):
        self.cursor.execute(
            "SELECT b.book_id, b.title, a.name, b.price, b.stock FROM Books b JOIN Authors a ON a.author_id=b.author_id WHERE b.title LIKE ?",
            f"%{title}%")
        return self.cursor.fetchall()

    def create_customer(self, fullname, email):
        self.cursor.execute("INSERT INTO Customers(fullname, email) VALUES (?,?)", (fullname, email))
        self.conn.commit()

    def create_order(self, customer_id):
        self.cursor.execute("INSERT INTO Orders(customer_id) VALUES (?)", (customer_id,))
        self.conn.commit()
        order_id = self.cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]
        return order_id

    def add_item_to_order(self, order_id, book_id, quantity):
        try:
            self.cursor.execute("INSERT INTO OrderItems(order_id, book_id, quantity) VALUES (?,?,?)",
                                (order_id, book_id, quantity))
            self.conn.commit()
            return True, None
        except pyodbc.Error as e:
            return False, str(e)

    def get_order_total(self, order_id):
        self.cursor.execute("SELECT dbo.fn_OrderTotal(?)", (order_id,))
        return self.cursor.fetchone()[0]

    def author_exists(self, author_id):
        self.cursor.execute("SELECT COUNT(*) FROM Authors WHERE author_id = ?", (author_id,))
        return self.cursor.fetchone()[0] > 0

    def add_author(self, name):
        self.cursor.execute("INSERT INTO Authors(name) VALUES (?)", (name,))
        self.conn.commit()

    def add_book(self, title, author_id, price, stock):
        self.cursor.execute("INSERT INTO Books(title, author_id, price, stock) VALUES (?,?,?,?)",
                            (title, author_id, price, stock))
        self.conn.commit()
