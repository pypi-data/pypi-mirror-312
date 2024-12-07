from setuptools import setup, find_packages

setup(
    name='digitalocean_access_spaces',
    version='1.1.1',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'botocore',
    ],
    url='https://github.com/lupin-oomura/digitalocean_access_spaces.git',
    author='Shin Oomura',
    author_email='shin.oomura@gmail.com',
    description='',
)
