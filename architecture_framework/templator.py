"""templator"""
import os
from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    template_name: имя шаблона
    folder: папка в которой ищем шаблон
    kwargs: параметры
    """
    # file_path = os.path.join(folder, template_name)
    # with open(file_path, encoding='utf-8') as f:
    #     template = Template(f.read())
    # return template.render(**kwargs)

    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)