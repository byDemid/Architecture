"""run"""
from wsgiref.simple_server import make_server
from architecture_framework.main import Architecture
from urls import fronts
from views import routes

application = Architecture(routes, fronts)

with make_server('', 8000, application) as httpd:
    print("Запуск на порту 8000...")
    httpd.serve_forever()
