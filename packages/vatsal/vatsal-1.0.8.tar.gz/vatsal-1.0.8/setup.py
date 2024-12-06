import os
from typing import Union, List

from setuptools import setup, find_packages

from vatsal import __version__, __author__, __email__


def get_version(package: str) -> Union[str, RuntimeError]:
    """Get the version number from the __init__.py file."""
    init_py = open(os.path.join(package, '__init__.py')).read()
    for line in init_py.split('\n'):
        if line.startswith('__version__'):
            return line.strip().split()[-1].strip('\'")')
    raise RuntimeError("Unable to find version string.")


def get_long_description() -> str:
    """Get the long description from the README.md file"""
    with open('README.md', 'r') as f:
        return f.read()


# Get the list of dependencies from the requirements.txt file
def get_requirements() -> List[str]:
    with open('requirements.txt', 'r') as f:
        return f.read().splitlines()


# Set up the package
setup(
    name='vatsal',
    version=__version__,
    packages=find_packages(),
    description='Custom utility functions to reuse efficiently.',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author=__author__,
    author_email=__email__,
    url='https://github.com/vatsal1306/vatsal',
    install_requires=get_requirements(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10'
    ],
    python_requires='>=3.10',
)
