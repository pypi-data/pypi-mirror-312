from setuptools import setup, find_packages

setup(
    name="WTG",  # Название вашего пакета
    version="0.1.0",  # Версия пакета
    packages=find_packages(),  # Автоматический поиск пакетов в директории
    install_requires=[  # Список зависимостей, если они есть
        'PyQt5', 'PyQtWebEngine'
    ],
    author="Ваше имя",
    author_email="sponge-bob@krusty-krab.ru",
    description="That package can you help to Move WEB to GUI",
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/mylibrary",  # URL к репозиторию, если есть
    classifiers=[  # Классификаторы PyPI для лучшей индексации
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
