from setuptools import setup, find_packages

setup(
    name='mol2chemfigPy3',
    version='1.4',
    url='https://github.com/Augus1999/mol2chemfigPy3',
    description='python3 version of mol2chemfig',
    license='MIT licence',
    package_dir={'mol2chemfigPy3': 'mol2chemfigPy3'},
    author='Nianze A. Tao',
    author_email='TaoN@cardiff.ac.uk',
    scripts=['mol2chemfig.py'],
    packages=find_packages(),
    python_requires='>=3',
    install_requires=['epam.indigo'],
)
