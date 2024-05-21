from setuptools import setup, find_packages

# @see https://github.com/pypa/sampleproject/blob/master/setup.py
setup(
    name='wbc',
    version='0.0.0',
    author='Maciej Brencz',
    author_email='maciej.brencz@gmail.com',
    description='Set of scripts used to import and process publications from dLibre in DJVU format',
    url='https://github.com/macbre/wbc',
    packages=find_packages(),
    install_requires=[
        'coverage==4.2',
        'docopt==0.6.2',
        'lxml>=3.4.0',  # use the version provided by python-lxml package
        'pytest==2.9.2',
        'readtime==1.0.5',
        'requests==2.32.0',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'fetch=scripts.fetch:main',
            'generate_xml=scripts.xml:generate',
            'tidy=scripts.tidy:main',
        ],
    }
)
