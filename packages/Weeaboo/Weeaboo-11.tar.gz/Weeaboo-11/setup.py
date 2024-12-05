from setuptools import find_packages, setup

def long_description():
    with open('README.md') as f:
        return f.read()

setup(
    name = 'Weeaboo',
    version = '11',
    description = 'Shared code for websites',
    long_description = long_description(),
    long_description_content_type = 'text/markdown',
    url = 'https://pypi.org/project/Weeaboo/',
    author = 'Homsar',
    author_email = 'homsar@foyono.com',
    packages = find_packages(),
    py_modules = ['runsite', 'rmexcept'],
    install_requires = ['aridity>=50', 'diapyr>=22', 'Flask>=2.0.3', 'lagoon>=22', 'mod-wsgi>=4.7.1', 'Werkzeug>=2.0.1'],
    package_data = {'': ['*.pxd', '*.pyx', '*.pyxbld', '*.arid', '*.aridt']},
    entry_points = {'console_scripts': ['rmexcept=rmexcept:main', 'runsite=runsite:main']},
)
