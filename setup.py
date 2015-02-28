import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = []
complex_requires = {
    "forms": [
        'wtforms',
        'jsonschema',
    ],
    'security': ['bcrypt', ],
    'sqlalchemy': ['sqlalchemy', 'psycopg2', 'pycrypto', ],
}
test_requires = [
    'nose',
    'coverage',
]

setup(
    name='web_utils',
    version='0.0.3',
    description='web_utils collection that used in web development process.',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Utilities",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
    ],
    author='winkidney',
    author_email='winkidney@gmail.com',
    url='http://github.com/winkidney/web_utils',
    keywords='web development utils ',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.sh', '*.md'],
    },
    zip_safe=False,
    install_requires=requires,
    extras_require=complex_requires,
    tests_require=test_requires,
    test_suite="web_utils",
    license="GPLv3",
    platform="any",
)
