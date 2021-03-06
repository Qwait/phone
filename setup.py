import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.md')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'apex',
    'pyramid_jinja2',
    'twilio',
    'paypal',
    'sendgrid-python',
    'webhelpers',
    'mysql-python',
    'cryptacular',
    ]

setup(name='phone',
      version='0.0',
      description='phone',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='phone',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = phone:main
      [console_scripts]
      initialize_phone_db = phone.scripts.initializedb:main
      """,
      )
