"""templator"""
import os
from jinja2 import Template


def render(template_name, folder='templates', **kwargs):
    """
    template_name: имя шаблона
    folder: папка в которой ищем шаблон
    kwargs: параметры
    """
    file_path = os.path.join(folder, template_name)
    with open(file_path, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)
