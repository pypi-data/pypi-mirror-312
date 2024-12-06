from setuptools import setup, find_packages

setup(
    name='buco_db_controller',
    version='1.1.16',
    packages=find_packages(),
    install_requires=[
        'PyYAML',
        'RapidFuzz',
        'pymongo',
        'dnspython',
        'Unidecode'
    ],
)
