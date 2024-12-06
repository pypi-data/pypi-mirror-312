from setuptools import setup, find_packages

setup(
    name='anjali_aws_helper',
    version='1.0.4',
    packages=find_packages(),
    install_requires=['boto3'],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)