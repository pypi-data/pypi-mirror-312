import os

from setuptools import setup, find_packages

# Read requirements from the requirements.txt file
# Use the absolute path to ensure it always works
file_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')

with open(file_path) as f:
    required_packages = f.read().splitlines()

setup(
    name='silcrow-utils',
    version='0.1.0',
    packages=find_packages(include=['silcrow_utils', 'silcrow_utils.*']),
    install_requires=required_packages,  # Automatically load from requirements.txt
    author='Sangsan Prohmvitak',
    description='A package for logging timestamps and executing scripts.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Silcrow/silcrow-utils',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
