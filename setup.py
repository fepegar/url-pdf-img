from setuptools import setup

setup(
    name='urlpdfimg',
    version='0.1.0',
    py_modules=['urlpdfimg'],
    install_requires=[
        'Click',
        'tqdm',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        urlpdfimg=urlpdfimg:cli
    ''',
)
