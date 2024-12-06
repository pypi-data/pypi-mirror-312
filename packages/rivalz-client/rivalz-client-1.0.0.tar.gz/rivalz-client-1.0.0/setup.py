# setup.py

from setuptools import setup, find_packages

setup(
    name='rivalz-client',
    version='1.0.0',
    author='Bui Dinh Ngoc',
    author_email='buidinhngoc.aiti@gmail.com',
    description='A Python client for interacting with Rivalz API',
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Rivalz-ai/pyhon-client/',
    packages=find_packages(),
    install_requires=[
        'requests>=2.28.2',
        'python-dotenv>=1.0.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)