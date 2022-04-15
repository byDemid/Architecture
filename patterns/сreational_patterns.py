"""Creational patterns"""
import copy
import quopri


class User:
    """Абстрактный пользователь"""
    pass


class Moderator(User):
    """Модератор"""
    pass


class Guest(User):
    """Гость"""
    pass


class UserFactory:
    """порождающий паттерн Абстрактная фабрика - фабрика пользователей"""
    types = {
        'guest': Guest,
        'moderator': Moderator
    }

    @classmethod
    def create(cls, type_):
        """порождающий паттерн Фабричный метод"""
        return cls.types[type_]()


class DishPrototype:
    """Порождающий паттерн Прототип - Блюдо"""

    def clone(self):
        """ прототип блюд"""
        return copy.deepcopy(self)


class Dish(DishPrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.dishes.append(self)


class KetoDish(Dish):
    """Кето Питание"""
    pass


class VegetarianDish(Dish):
    """Вегетарианство"""
    pass


class DishFactory:
    """Порождающий паттерн Абстрактная фабрика - фабрика блюд"""
    types = {
        'keto': KetoDish,
        'vegetarianism': VegetarianDish
    }

    @classmethod
    def create(cls, type_, name, category):
        """порождающий паттерн Фабричный метод"""
        return cls.types[type_](name, category)


class Category:
    """Категория"""

    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.dishes = []

    def dish_count(self):
        """количество блюд"""
        result = len(self.dishes)
        if self.category:
            result += self.category.dish_count()
        return result


class Engine:
    """Основной интерфейс проекта"""

    def __init__(self):
        self.moderators = []
        self.guests = []
        self.dishes = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_dish(type_, name, category):
        return DishFactory.create(type_, name, category)

    def get_dish(self, name):
        for item in self.dishes:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class SingletonByName(type):
    """порождающий паттерн Синглтон"""

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)
