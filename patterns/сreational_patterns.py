"""Creational patterns"""
import copy
import quopri
import sqlite3
from patterns.architectural_system_pattern_unit_of_work import DomainObject
from patterns.behavioral_patterns import Subject, ConsoleWriter


class User:
    """Абстрактный пользователь"""

    def __init__(self, name):
        self.name = name


class Moderator(User):
    """Модератор"""
    pass


class Guest(User, DomainObject):
    """Гость"""

    def __init__(self, name):
        self.training = []
        super().__init__(name)


class UserFactory:
    """порождающий паттерн Абстрактная фабрика - фабрика пользователей"""
    types = {
        'guest': Guest,
        'moderator': Moderator
    }

    @classmethod
    def create(cls, type_, name):
        """порождающий паттерн Фабричный метод"""
        return cls.types[type_](name)


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


class TrainingPrototype:
    """Порождающий паттерн Прототип - тренировка"""

    def clone(self):
        """ прототип тренировок"""
        return copy.deepcopy(self)


class Training(TrainingPrototype, Subject):
    def __init__(self, name, categories_training):
        self.name = name
        self.categories_training = categories_training
        self.categories_training.training.append(self)
        self.guests = []
        super().__init__()

    def __getitem__(self, item):
        return self.guests[item]

    def add_guest(self, guest: Guest):
        self.guests.append(guest)
        guest.training.append(self)
        self.notify()


class InteractiveTraining(Training):
    """Интерактивный"""
    pass


class RecordTraining(Training):
    """В записи"""
    pass


class TrainingFactory:
    """Порождающий паттерн Абстрактная фабрика - фабрика тренировок"""
    types = {
        'interactive': InteractiveTraining,
        'record': RecordTraining
    }

    @classmethod
    def create(cls, type_, name, categories_training):
        """порождающий паттерн Фабричный метод"""
        return cls.types[type_](name, categories_training)


class CategoryTraining:
    """Категория Тренировок"""
    auto_id = 0

    def __init__(self, name, categories_training):
        self.id = CategoryTraining.auto_id
        CategoryTraining.auto_id += 1
        self.name = name
        self.categories_training = categories_training
        self.training = []

    def training_count(self):
        """количество тренировок"""
        result = len(self.training)
        if self.categories_training:
            result += self.categories_training.training_count()
        return result


class Engine:
    """Основной интерфейс проекта"""

    def __init__(self):
        self.moderators = []
        self.guests = []
        self.dishes = []
        self.categories = []
        self.categories_training = []
        self.training = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

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
    def create_category_training(name, category=None):
        return CategoryTraining(name, category)

    def find_category_training_by_id(self, id):
        for item in self.categories_training:
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
    def create_training(type_, name, category):
        return TrainingFactory.create(type_, name, category)

    def get_training(self, name) -> Training:
        for item in self.training:
            if item.name == name:
                return item
        return None

    def get_guest(self, name) -> Guest:
        for item in self.guests:
            if item.name == name:
                return item

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

    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    @staticmethod
    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)



# architectural system pattern mappers

class GuestMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'guest'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            guest = Guest(name)
            guest.id = id
            result.append(guest)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Guest(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = sqlite3.connect('patterns.sqlite')


class MapperRegistry:
    """Архитектурный системный паттерн - Data Mapper"""
    mappers = {
        'guest': GuestMapper,
        #'category': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj):

        if isinstance(obj, Guest):

            return GuestMapper(connection)
        #if isinstance(obj, Category):
            #return CategoryMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')

class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')

class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')

class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
