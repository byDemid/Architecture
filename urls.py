"""urls"""
from datetime import date
from views import Index, Admin, Recipes, Products, Sport, Delivery, \
    Profile, SendRecipe, Register, DishesList, \
    CreateDish, CreateCategory, CategoryList, CopyDish


def secret_front(request):
    """front controller"""
    request['data'] = date.today()


def other_front(request):
    """front controller"""
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/admin/': Admin(),
    '/recipes/': Recipes(),
    '/products/': Products(),
    '/sport/': Sport(),
    '/delivery/': Delivery(),
    '/profile/': Profile(),
    '/send_recipe/': SendRecipe(),
    '/register/': Register(),

    '/dishes_list/': DishesList(),
    '/create_dish/': CreateDish(),
    '/create_category/': CreateCategory(),
    '/category_list/': CategoryList(),
    '/copy_dish/': CopyDish()
}
