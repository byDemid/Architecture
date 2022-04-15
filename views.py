"""views"""
from architecture_framework.templator import render
from patterns.сreational_patterns import Engine, Logger

site = Engine()
logger = Logger('main')


class Index:
    """Главная"""

    def __call__(self, request):
        return '200 OK', render('index.html', data=request.get('data', None))


class Admin:
    """Админка"""

    def __call__(self, request):
        return '200 OK', 'admin'


class Register:
    """Регистрация"""

    def __call__(self, request):
        return '200 OK', 'register'


class Products:
    """Продукты"""

    def __call__(self, request):
        return '200 OK', 'products'


class SendRecipe:
    """Отправить рецепт"""

    def __call__(self, request):
        return '200 OK', render('send_recipe.html')


class Recipes:
    """Рецепты"""

    def __call__(self, request):
        return '200 OK', render('recipes.html', objects_list=site.categories)


class Sport:
    """Спорт"""

    def __call__(self, request):
        return '200 OK', 'sport'


class Delivery:
    """Доставка"""

    def __call__(self, request):
        return '200 OK', 'delivery'


class Profile:
    """Профиль"""

    def __call__(self, request):
        return '200 OK', 'profile'


class NotFound404:
    """PAGE Not Found"""

    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class DishesList:
    """контроллер - список блюд"""

    def __call__(self, request):
        logger.log('Список блюд')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('dish_list.html',
                                    objects_list=category.dishes,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No dishes have been added yet'


class CreateDish:
    """контроллер - создать блюдо"""
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                dish = site.create_dish('record', name, category)
                site.dishes.append(dish)

            return '200 OK', render('dish_list.html',
                                    objects_list=category.dishes,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_dish.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


class CreateCategory:
    """контроллер - создать категорию"""

    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('recipes.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


class CategoryList:
    """контроллер - список категорий"""

    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', objects_list=site.categories)


class CopyDish:
    """контроллер - копировать блюда"""

    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_dish= site.get_dish(name)
            if old_dish:
                new_name = f'copy_{name}'
                new_dish = old_dish.clone()
                new_dish.name = new_name
                site.dishes.append(new_dish)

            return '200 OK', render('dish_list.html', objects_list=site.dishes)
        except KeyError:
            return '200 OK', 'No dishes have been added yet'
