from setuptools import find_packages, setup

setup(
    name='py3cw-am11yfork',
    version='0.0.18',

    description='3commas Python wrapper',

    url='https://github.com/am11y/py3cw-am11yfork',

    author='Bogdan Teodoru',
    author_email='me@bogdanteodoru.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable'
    ],

    keywords='api 3commas trading crypto bitcoin altcoin',

    packages=find_packages(exclude=['tests']),

    install_requires=[
        'requests',
    ],
)
