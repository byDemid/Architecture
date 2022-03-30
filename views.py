"""views"""
from architecture_framework.templator import render


class Index:
    """Главная"""

    def __call__(self, request):
        return '200 OK', render('index.html', data=request.get('data', None))


class Admin:
    """Админка"""

    def __call__(self, request):
        return '200 OK', 'about'


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
        return '200 OK', 'recipes'


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
