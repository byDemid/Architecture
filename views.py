"""views"""
from datetime import date

from architecture_framework.templator import render
from patterns.structural_patterns import AppRoute, Debug
from patterns.сreational_patterns import Engine, Logger

site = Engine()
logger = Logger('main')

routes = {}

@AppRoute(routes=routes, url='/')
class Index:
    """Главная"""
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', data=request.get('date', None))


@AppRoute(routes=routes, url='/admin/')
class Admin:
    """Админка"""
    @Debug(name='Admin')
    def __call__(self, request):
        return '200 OK', 'admin'


@AppRoute(routes=routes, url='/register/')
class Register:
    """Регистрация"""
    @Debug(name='Register')
    def __call__(self, request):
        return '200 OK', 'register'


@AppRoute(routes=routes, url='/products/')
class Products:
    """Продукты"""
    @Debug(name='Products')
    def __call__(self, request):
        return '200 OK', 'products'


@AppRoute(routes=routes, url='/send_recipe/')
class SendRecipe:
    """Отправить рецепт"""
    @Debug(name='SendRecipe')
    def __call__(self, request):
        return '200 OK', render('send_recipe.html')


@AppRoute(routes=routes, url='/recipes/')
class Recipes:
    """Рецепты"""
    @Debug(name='Recipes')
    def __call__(self, request):
        return '200 OK', render('recipes.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/sport/')
class Sport:
    """Спорт"""
    @Debug(name='Sport')
    def __call__(self, request):
        return '200 OK', 'sport'


@AppRoute(routes=routes, url='/delivery/')
class Delivery:
    """Доставка"""
    @Debug(name='Delivery')
    def __call__(self, request):
        return '200 OK', 'delivery'


@AppRoute(routes=routes, url='/profile/')
class Profile:
    """Профиль"""
    @Debug(name='Profile')
    def __call__(self, request):
        return '200 OK', 'profile'


class NotFound404:
    """PAGE Not Found"""
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@AppRoute(routes=routes, url='/dishes_list/')
class DishesList:
    """контроллер - список блюд"""
    @Debug(name='DishesList')
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


@AppRoute(routes=routes, url='/create_dish/')
class CreateDish:
    """контроллер - создать блюдо"""
    category_id = -1

    @Debug(name='CreateDish')
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                dish = site.create_dish('keto', name, category)
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


@AppRoute(routes=routes, url='/create_category/')
class CreateCategory:
    """контроллер - создать категорию"""
    @Debug(name='CreateCategory')
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


@AppRoute(routes=routes, url='/category_list/')
class CategoryList:
    """контроллер - список категорий"""
    @Debug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/copy_dish/')
class CopyDish:
    """контроллер - копировать блюда"""
    @Debug(name='CopyDish')
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
