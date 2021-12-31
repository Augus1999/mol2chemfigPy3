from setuptools import setup, find_packages
from mol2chemfigPy3 import __version__


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='mol2chemfigPy3',
    version=__version__,
    url='https://github.com/Augus1999/mol2chemfigPy3',
    description='python3 version of mol2chemfig',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT licence',
    package_dir={'mol2chemfigPy3': 'mol2chemfigPy3'},
    author='Nianze A. Tao',
    author_email='TaoN@cardiff.ac.uk',
    scripts=['mol2chemfig.py'],
    packages=find_packages(),
    python_requires='>=3',
    install_requires=['epam.indigo'],
)
