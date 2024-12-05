"""
locan installation: pip install -e .

Upload to PyPI

python setup.py sdist
twine upload --repository pypitest dist/infrasonar-appliance-X.X.X.tar.gz
twine upload --repository pypi dist/infrasonar-appliance-X.X.X.tar.gz
"""
from setuptools import setup, find_packages

__version__ = '0.2.2'  # Update version in appliance/appliance.py as well

try:
    with open('README.md', 'r') as f:
        long_description = f.read()
except IOError:
    long_description = ''

setup(
    name='infrasonar-appliance',
    version=__version__,
    description='InfraSonar Appliance Manager',
    url='https://github.com/infrasonar/appliance-manager',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jeroen van der Heijden',
    author_email='jeroen@cesbit.com',
    entry_points={
        'console_scripts': ['appliance=appliance.appliance:main'],
    },
    license='GPLv3',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    install_requires=[
        'aiohttp',
        'pyyaml',
        'configobj',
        'setproctitle',
    ],
    keywords='infrasonar monitoring toolkit util',
)
