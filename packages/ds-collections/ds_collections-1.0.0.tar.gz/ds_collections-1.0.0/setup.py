from setuptools import setup, find_packages

setup(
    name='ds_collections',             # Your package name
    version='1.0.0',                   # Version of the package
    packages=find_packages(),          # Automatically find all sub-packages
    description='Data Structures Collections: BST and Linked Lists.',
    author='Bhuyan Md Anowarul Kairm',                # Replace with your name
    author_email='anowarulkarim8@gmail.com', # Replace with your email
    url='https://github.com/anowarulkarim/ds_collections',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',           # Minimum Python version requirement
)
