import sys
sys.path.append('tables')

from project_config import *
from dbconnection import *
from categories_table import *
from dishes_table import *

class Main:

    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        pt = CategoriesTable()
        pht = DishesTable()
        pt.create()
        pht.create()
        return

    def db_insert_somethings(self):
        pt = CategoriesTable()
        pht = DishesTable()
        pt.insert_one(["Первые"])
        pt.insert_one(["Вторые"])
        pt.insert_one(["Салат"])
        pht.insert_one([1, "Борщ" , "Обжарить лук с морковью, добавить мясо, свеклу, воду и тушить до готовности."])
        pht.insert_one([2, "Жаркое",  "Нарежьте баранье мясо и картошку, добавьте нарезанный лук; на сковороде, на подсолнечном масле пожарьте. Посолите по вкусу."])
        pht.insert_one([3, "Салат",  "Нарезать помидоры, огурцы, лук, заливаем подсолнечным маслом и посыпаем солью."])

    def db_drop(self):
        pt = CategoriesTable()
        pht = DishesTable()
        pht.drop()
        pt.drop()
        return

    def show_main_menu(self):
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - просмотр блюд;
    2 - сброс и инициализация таблиц;
    9 - выход."""
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "2":
            self.db_drop()
            self.db_init()
            self.db_insert_somethings()
            print("Таблицы созданы заново!")
            return "0"
        elif next_step != "1" and next_step != "9":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step

    def show_categories(self):
        self.category_id = -1
        menu = """Просмотр списка категорий!
    №\tНазвание"""
        print(menu)
        lst = CategoriesTable().all()
        for i in lst:
            print(str(i[0]) + "\t" + str(i[1]))
        menu = """Дальнейшие операции: 
    0 - возврат в главное меню;
    3 - добавление новой категории;
    4 - удаление категории;
    5 - просмотр блюд категории;
    9 - выход."""
        print(menu)
        return

    def after_show_categories(self, next_step):
        while True:
            if next_step == "4":
                print("Пока не реализовано!")
                return "1"
            elif next_step == "6" or next_step == "7":
                print("Пока не реализовано!")
                next_step = "5"
            elif next_step == "5":
                next_step = self.show_dishes_by_categories()
            elif next_step != "0" and next_step != "9" and next_step != "3":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step

    def show_add_category(self):
        # Не реализована проверка на максимальную длину строк. Нужно доделать самостоятельно!
        data = []
        data.append(input("Введите имя (1 - отмена): ").strip())
        if data[0] == "1":
            return
        while len(data[0].strip()) == 0:
            data[0] = input("Имя не может быть пустым! Введите имя заново (1 - отмена):").strip()
            if data[0] == "1":
                return
        data.append(input("Введите фамилию (1 - отмена): ").strip())
        if data[1] == "1":
            return
        while len(data[1].strip()) == 0:
            data[1] = input("Фамилия не может быть пустой! Введите фамилию заново (1 - отмена):").strip()
            if data[1] == "1":
                return
        data.append(input("Введите отчество (1 - отмена):").strip())
        if data[2] == "1":
            return
        CategoriesTable().insert_one(data)
        return

    def show_dishes_by_categories(self):
        if self.category_id == -1:
            while True:
                num = input("Укажите номер строки, в которой записана интересующая Вас категория (0 - отмена): ")
                while len(num.strip()) == 0:
                    num = input(
                        "Пустая строка. Повторите ввод! Укажите номер строки, в которой записана интересующая Вас категория (0 - отмена): ")
                if num == "0":
                    return "1"
                category = CategoriesTable().find_by_position(int(num))
                if not category:
                    print("Введено число, неудовлетворяющее количеству категорий!")
                else:
                    self.category_id = int(category[0])  # Преобразование в целое число
                    self.category_obj = category
                    break
        print("Выбрана категория: " + self.category_obj[1])
        print("Блюда:")
        lst = DishesTable().all_by_category_id(self.category_id)
        for dish in lst:
            print(dish[1])
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр категорий;
    6 - добавление нового блюда;
    7 - удаление блюда;
    9 - выход."""
        print(menu)
        return self.read_next_step()

        return self.read_next_step()

    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while(current_menu != "9"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_categories()
                next_step = self.read_next_step()
                current_menu = self.after_show_categories(next_step)
            elif current_menu == "2":
                self.show_main_menu()
            elif current_menu == "3":
                self.show_add_category()
                current_menu = "1"
        print("До свидания!")    
        return

    def test(self):
        DbTable.dbconn.test()

m = Main()
# Откоментируйте эту строку и закоментируйте следующую для теста
# соединения с БД
# m.test()
m.main_cycle()
    
