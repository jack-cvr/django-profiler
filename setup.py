import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


APP_NAME = '%app_name%'
LICENSE = 'MPL 2.0'


setup(
    name='django-{0}'.format(APP_NAME),
    version='0.1',
    packages=[APP_NAME],
    include_package_data=True,
    license=LICENSE,
    description='app description',
    long_description=README,
    #url='http://www.example.com/',
    author='Andrey Kuzmin',
    author_email='jack.cvr@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: {0}'.format(LICENSE),
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)