import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'bcrypt',
    'pysandbox',
]
complex_requires = [
    'sqlalchemy',
    'wtforms',
    'psycopg2',
    'pycrypto',
    'padding',
]
test_requires = [
    'nose',
    'coverage',
]

setup(name='web_utils',
      version='0.0.1',
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
      zip_safe=False,
      install_requires=requires+test_requires,
      tests_require=requires,
      test_suite="web_utils",
      )
