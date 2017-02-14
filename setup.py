import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = []
with open(os.path.join(here, 'requirements.txt')) as f:
    for line in f.read().splitlines():
        if line.find('--extra-index-url') == -1:
            requires.append(line)

setup(
    name='MBTA Python Library',
    version="0.1.1",
    description='MBTA Python Library',
    author='Doug Morgan',
    author_email='doug.morgan@gmail.com',
    url='https://github.com/dougzor/mbta_python',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
)
