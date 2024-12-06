from typing import List

from setuptools import setup, find_packages

from vatsal import __version__, __author__, __email__


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
