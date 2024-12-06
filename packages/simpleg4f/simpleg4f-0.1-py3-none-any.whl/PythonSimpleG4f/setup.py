from setuptools import setup, find_packages

setup(
    name='PythonSimpleG4f',
    version='0.1',
    packages=find_packages(),
    install_requires=[  # зависимостей от библиотек
        'requests', 'g4f'
    ],
    description="This library will allow you to ease the use of g4f. Suitable for beginners or lazy",
    long_description=open('README.md').read(),  # или 'long_description_content_type="text/markdown"'
    author='Amfetaminchik',
    author_email='sponge-bob@krusty-krab.ru',
    url='https://github.com/babyyousomething/PythonSimpleG4f/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
