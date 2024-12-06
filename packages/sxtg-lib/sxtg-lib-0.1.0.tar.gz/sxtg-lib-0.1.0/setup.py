from setuptools import setup, find_packages

setup(
    name="sxtg-lib",  # Уникальное имя пакета
    version="0.1.0",  # Версия
    packages=find_packages(),  # Автоматически найдет папку lib
    install_requires=[],  # Зависимости, если есть
    python_requires=">=3.11",  # Минимальная версия Python
    description="Утилита для работы с Telegram ботом",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Igor",
    author_email="epicprod@mail.com",
    url="https://github.com/твой-репозиторий",  # Если есть
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    )
