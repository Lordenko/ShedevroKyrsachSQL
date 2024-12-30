from Classes.database import Database
from Classes.menus import UserMenu, AdminMenu

if __name__ == "__main__":
    db = Database(server="LORDENKO", database="BookStoreDB", trusted=True)

    print("Привіт, не будь занудою. Ти хто?")
    print("1. Звичайний користувач")
    print("2. Адмін")
    role = input("Введи вибір: ")

    if role == "1":
        user_menu = UserMenu(db)
        user_menu.show()
    elif role == "2":
        admin_menu = AdminMenu(db)
        admin_menu.show()
    else:
        print("Пфф, не жартуй так.")


