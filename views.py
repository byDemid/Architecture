"""views"""
from datetime import date
from architecture_framework.templator import render
from patterns.architectural_system_pattern_unit_of_work import UnitOfWork
from patterns.behavioral_patterns import EmailNotifier, \
    SmsNotifier, ListView, CreateView, BaseSerializer
from patterns.structural_patterns import AppRoute, Debug
from patterns.сreational_patterns import Engine, Logger, MapperRegistry

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

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
        return '200 OK', render('sport.html', objects_list=site.categories_training)


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
            old_dish = site.get_dish(name)
            if old_dish:
                new_name = f'copy_{name}'
                new_dish = old_dish.clone()
                new_dish.name = new_name
                site.dishes.append(new_dish)

            return '200 OK', render('dish_list.html', objects_list=site.dishes)
        except KeyError:
            return '200 OK', 'No dishes have been added yet'


# Тренировки

@AppRoute(routes=routes, url='/training_list/')
class TrainingList:
    """контроллер - список тренировок"""

    @Debug(name='TrainingList')
    def __call__(self, request):
        # logger.log('Список тренеровок')
        try:
            category_training = site.find_category_training_by_id(int(request['request_params']['id']))
            return '200 OK', render('training_list.html',
                                    objects_list=category_training.training,
                                    name=category_training.name,
                                    id=category_training.id)
        except KeyError:
            return '200 OK', 'No training have been added yet'


@AppRoute(routes=routes, url='/create_training/')
class CreateTraining:
    """контроллер - создать тренеровку"""
    category_training_id = -1

    @Debug(name='CreateTraining')
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category_training = None
            if self.category_training_id != -1:
                category_training = site.find_category_training_by_id(int(self.category_training_id))
                training = site.create_training('record', name, category_training)
                site.training.append(training)
            return '200 OK', render('training_list.html',
                                    objects_list=category_training.training,
                                    name=category_training.name,
                                    id=category_training.id)
        else:
            try:
                self.category_training_id = int(request['request_params']['id'])
                category_training = site.find_category_training_by_id(int(self.category_training_id))
                return '200 OK', render('create_training.html',
                                        name=category_training.name,
                                        id=category_training.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@AppRoute(routes=routes, url='/create_training_category/')
class CreateTrainingCategory:
    """контроллер - создать категорию тренировок"""

    @Debug(name='CreateTrainingCategory')
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            print(request)
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category_training_id = data.get('category_id')
            category_training = None
            if category_training_id:
                category_training = site.find_category_training_by_id(int(category_training_id))
            new_category = site.create_category_training(name, category_training)
            site.categories_training.append(new_category)
            return '200 OK', render('sport.html', objects_list=site.categories_training)
        else:
            categories_training = site.categories_training
            return '200 OK', render('create_training_category.html', categories=categories_training)


@AppRoute(routes=routes, url='/category_training_list/')
class CategoryTrainingList:
    """контроллер - список категорий"""

    @Debug(name='CategoryTrainingList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_training_list.html', objects_list=site.categories_training)


@AppRoute(routes=routes, url='/copy_training/')
class CopyTraining:
    """контроллер - копировать блюда"""

    @Debug(name='CopyTraining')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_training = site.get_training(name)
            if old_training:
                new_name = f'copy_{name}'
                new_training = old_training.clone()
                new_training.name = new_name
                site.training.append(new_training)

            return '200 OK', render('training_list.html', objects_list=site.training)
        except KeyError:
            return '200 OK', 'No training have been added yet'


@AppRoute(routes=routes, url='/guest_list/')
class GuestListView(ListView):
    # queryset = site.guests
    template_name = 'guest_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('guest')
        return mapper.all()


@AppRoute(routes=routes, url='/create_guest/')
class GuestCreateView(CreateView):
    template_name = 'create_guest.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('guest', name)
        site.guests.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/add_guest/')
class AddGuestByTrainingCreateView(CreateView):
    template_name = 'add_guest.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['training'] = site.training
        context['guests'] = site.guests
        return context

    def create_obj(self, data: dict):
        training_name = data['training_name']
        training_name = site.decode_value(training_name)
        training = site.get_training(training_name)
        guest_name = data['guest_name']
        guest_name = site.decode_value(guest_name)
        guest = site.get_guest(guest_name)
        training.add_guest(guest)


@AppRoute(routes=routes, url='/api/')
class TrainingApi:
    @Debug(name='TrainingApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.training).save()
