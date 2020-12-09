from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='nbtemplater',
    version='0.1.2',
    author='Sebastian Steiner',
    author_email='sebastian.steiner@tuta.io',
    description='A tool to split a template Jupyter notebook into a solution and a task version.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sebastian-steiner/nbtemplater',
    packages=find_packages(),
    package_data={},
    license='MIT',
    install_requires=[
        'Click',
        'colorama'
    ],
    entry_points={
        'console_scripts': ['nbtemplater = nbtemplater.cli:run_cmd']
    },
    python_requires='>=3.5',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=[
        'Notebooks',
        'Grading',
        'Homework',
        'Teaching'
    ]
)
