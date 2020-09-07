from functools import partial
from pathlib import Path

import requests
from datamodel_code_generator import InputFileType, PythonVersion, generate
from transliterate import translit

output_dir = Path(__file__).parent / 'models_generated'
generate_model = partial(generate, input_file_type=InputFileType.Json, target_python_version=PythonVersion.PY_38)

if __name__ == '__main__':
    """
    Docs: https://2ch.hk/api/res/1.html
    
    -- JSON для тредов и списков
    
    Треды:
    https://2ch.hk/доска/res/номертреда.json
    Список тредов:
    https://2ch.hk/доска/номерстраницы.json (первая страница: index)
    Все треды с сортировкой по последнему посту:
    https://2ch.hk/доска/catalog.json
    Все треды с сортировкой по времени создания треда:
    https://2ch.hk/доска/catalog_num.json
    Все треды с доски(облегченный вариант, с просмотрами и рейтингом для топа тредов):
    https://2ch.hk/доска/threads.json
    
    -- Мобильное API
    
    Получить настройки всех досок:
    Пример: https://2ch.hk/makaba/mobile.fcgi?task=get_boards
    Получить все посты из треда с номера поста по доске:
    Пример: https://2ch.hk/makaba/mobile.fcgi?task=get_thread&board=abu&thread=39220&num=41955
    Получить все посты из треда с номера поста по треду:
    Пример: https://2ch.hk/makaba/mobile.fcgi?task=get_thread&board=abu&thread=39220&post=252
    Получить один пост:
    Пример: https://2ch.hk/makaba/mobile.fcgi?task=get_post&board=abu&post=41955
    """
    methods = (
        ('https://2ch.hk/api/res/1.json', 'thread'),
        ('https://2ch.hk/b/index.json', 'page'),
        ('https://2ch.hk/b/catalog.json', 'catalog'),
        ('https://2ch.hk/b/catalog_num.json', 'catalog_by_date'),
        ('https://2ch.hk/b/threads.json', 'threads'),
        ('https://2ch.hk/boards.json', 'boards'),
        ('https://2ch.hk/makaba/mobile.fcgi?task=get_boards', 'boards_by_types'),
        ('https://2ch.hk/makaba/mobile.fcgi?task=get_thread&board=abu&thread=39220&num=41955', 'posts_by_id'),
        ('https://2ch.hk/makaba/mobile.fcgi?task=get_thread&board=abu&thread=39220&post=252', 'posts_by_num'),
        ('https://2ch.hk/makaba/mobile.fcgi?task=get_post&board=abu&post=41955', 'post'),
    )

    for url, name in methods:
        result = requests.get(url).text
        result = translit(result, 'ru', reversed=True, strict=True)
        generate_model(name, result, output=output_dir / f'_{name}.py')
