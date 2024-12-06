from setuptools import setup, find_packages

setup(
    name="Asyncio-ZlapiNormal",
    version="1.3",
    packages=find_packages(),
    install_requires=[
        "requests",
        "asyncio"
    ],
    extras_require={
        'telegram': [
            "python-telegram-bot",
            "telebot"
        ]
    },
    author="Lâm Minh Phú",
    author_email="zalochatbot@gmail.com",
    description="Library ZaloData",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)