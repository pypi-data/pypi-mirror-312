from setuptools import setup, find_packages

setup(
    name='sort_prices',
    version='1.0.0',
    description='A library to sort prices from low to high for Django or other Python applications.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Snehal Kolhe',
    author_email='x23339438@student.ncirl.ie',
    url='https://github.com/SnehalKolhe10/sort_prices',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
