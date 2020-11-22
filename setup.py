from setuptools import setup

setup(
    name='nbtemplater',
    version='0.1',
    py_modules=['nbtemplater'],
    install_requires=[
        'Click',
        'colorama'
    ],
    entry_points='''
        [console_scripts]
        nbtemplater=nbtemplater:run_cmd
    '''
)
