class UserMenu:
    def __init__(self, db):
        self.db = db

    def show(self):
        while True:
            print("\n------ Меню користувача ------")
            print("1. Переглянути всі книги")
            print("2. Пошук книги за назвою")
            print("3. Створити клієнта")
            print("4. Створити замовлення (потрібен Customer ID)")
            print("5. Додати товар до замовлення")
            print("6. Показати суму замовлення")
            print("7. Вихід")
            choice = input("Ваш вибір: ")
            if choice == "1":
                self.list_books()
            elif choice == "2":
                self.search_books()
            elif choice == "3":
                self.create_customer()
            elif choice == "4":
                self.create_order()
            elif choice == "5":
                self.add_item_to_order()
            elif choice == "6":
                self.show_order_total()
            elif choice == "7":
                break
            else:
                print("Невідомий вибір")

    def list_books(self):
        rows = self.db.list_books()
        for row in rows:
            print(f"{row.title} - {row.name}, Ціна: {row.price}, Наявність: {row.stock}")

    def search_books(self):
        title = input("Введіть назву книги або частину: ")
        rows = self.db.search_books_by_title(title)
        if not rows:
            print("Нічого не знайдено")
        else:
            for row in rows:
                print(f"[{row.book_id}] {row.title} - {row.name}, Ціна: {row.price}, Наявність: {row.stock}")

    def create_customer(self):
        fullname = input("Ваше ім'я: ")
        email = input("Ваш email: ")
        self.db.create_customer(fullname, email)
        print("Клієнта створено!")

    def create_order(self):
        cid = int(input("Введіть ID клієнта: "))
        order_id = self.db.create_order(cid)
        print(f"Створено замовлення #{order_id}")

    def add_item_to_order(self):
        oid = int(input("Введіть ID замовлення: "))
        bid = int(input("Введіть ID книги: "))
        qty = int(input("Кількість: "))
        success, error = self.db.add_item_to_order(oid, bid, qty)
        if success:
            print("Товар додано до замовлення!")
        else:
            print("Помилка при додаванні:", error)

    def show_order_total(self):
        oid = int(input("Введіть ID замовлення: "))
        total = self.db.get_order_total(oid)
        print(f"Сума замовлення #{oid}: {total} грн.")


class AdminMenu:
    def __init__(self, db):
        self.db = db

    def show(self):
        while True:
            print("\n------ Адмін меню ------")
            print("1. Додати автора")
            print("2. Додати книгу")
            print("3. Переглянути всі книги")
            print("4. Вихід")
            choice = input("Ваш вибір: ")
            if choice == "1":
                self.add_author()
            elif choice == "2":
                self.add_book()
            elif choice == "3":
                self.list_books()
            elif choice == "4":
                break
            else:
                print("Невідомий вибір")

    def add_author(self):
        name = input("Ім'я автора: ")
        self.db.add_author(name)
        print("Автора додано!")

    def add_book(self):
        title = input("Назва книги: ")
        author_id = int(input("ID автора: "))

        if not self.db.author_exists(author_id):
            print("Автор з таким ID не існує. Спочатку додайте автора.")
            return

        price = float(input("Ціна: "))
        stock = int(input("Кількість на складі: "))
        self.db.add_book(title, author_id, price, stock)
        print("Книгу додано!")

    def list_books(self):
        rows = self.db.list_books()
        for row in rows:
            print(f"{row.title} - {row.name}, Ціна: {row.price}, Наявність: {row.stock}")
