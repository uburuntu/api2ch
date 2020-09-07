import os
from importlib.machinery import SourceFileLoader

import setuptools
from pkg_resources import parse_requirements

module_name = 'api2ch'

module = SourceFileLoader(
    module_name, os.path.join(module_name, '__init__.py')
).load_module()


def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()


def load_requirements(filename: str) -> list:
    requirements = []
    for req in parse_requirements(read(filename)):
        extras = '[{}]'.format(','.join(req.extras)) if req.extras else ''
        requirements.append(
            '{}{}{}'.format(req.name, extras, req.specifier)
        )
    return requirements


setuptools.setup(
    name=module_name,
    version=module.__version__,
    author=module.__author__,
    author_email=module.__email__,
    license=module.__license__,
    description=module.__doc__,
    platforms='all',
    long_description=read('readme.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/uburuntu/{}'.format(module_name),
    download_url='https://github.com/uburuntu/{}/archive/master.zip'.format(module_name),
    packages=setuptools.find_packages(exclude=['examples', 'tests']),
    requires_python='>=3.6',
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
