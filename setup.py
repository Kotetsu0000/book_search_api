from setuptools import setup, find_packages

setup(
    name='book_search_api',
    version='1.0.6',
    packages=find_packages(),
    install_requires=["requests", "xmltodict"],
)