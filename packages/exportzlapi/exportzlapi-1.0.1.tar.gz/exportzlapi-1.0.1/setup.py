from setuptools import setup, find_packages

setup(
    name="exportzlapi",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "python-telegram-bot",
        "requests",
        "telebot",
        "asyncio"       
    ],
    author="Lâm Minh Phú",
    author_email="zalochatbot@gmail.com",
    description="Library ZaloAPI Pro",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)