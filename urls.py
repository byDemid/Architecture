"""urls"""
from datetime import date
from views import Index, Admin, Recipes, Products, Sport, Delivery, Profile, SendRecipe, Register


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
}
