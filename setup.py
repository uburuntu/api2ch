import ast
from pathlib import Path

import setuptools


def read(filename: str) -> str:
    return Path(filename).read_text(encoding='utf-8')


def load_metadata(filename: str) -> dict:
    tree = ast.parse(read(filename))
    metadata = {'__doc__': ast.get_docstring(tree)}

    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if isinstance(target, ast.Name) and target.id.startswith('__'):
            metadata[target.id] = ast.literal_eval(node.value)

    return metadata


def load_requirements(filename: str) -> list:
    return [
        line
        for line in (line.strip() for line in read(filename).splitlines())
        if line and not line.startswith('#')
    ]


module_name = 'api2ch'
metadata = load_metadata(f'{module_name}/__init__.py')

setuptools.setup(
    name=module_name,
    version=metadata['__version__'],
    author=metadata['__author__'],
    author_email=metadata['__email__'],
    license=metadata['__license__'],
    description=metadata['__doc__'],
    platforms='all',
    long_description=read('readme.md'),
    long_description_content_type='text/markdown',
    url=f'https://github.com/uburuntu/{module_name}',
    download_url=f'https://github.com/uburuntu/{module_name}/archive/master.zip',
    packages=setuptools.find_packages(exclude=['examples', 'tests']),
    install_requires=load_requirements('requirements.txt'),
    extras_require={'dev': load_requirements('requirements-dev.txt')},
    keywords=['2ch', 'dvach', 'api'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Typing :: Typed',
    ],
)
