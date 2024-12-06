import os
from setuptools import setup, find_packages

setup(
    name="WTG",
    version="0.1.1",
    packages=find_packages(),
    install_requires=['PyQt5', ' PyQtWebEngine'],
    author="Amfetaminchik",
    author_email="sponge-bob@krusty-krab.ru",
    description="This package can you help to move WEB to GUI",
    long_description=open("README.md", encoding="utf-8").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
