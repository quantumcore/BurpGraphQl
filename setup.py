from setuptools import setup, find_packages
import pypandoc
try:
    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='BurpGraphQl',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='1.5',
    license='MIT',
    author="QuantumCore",
    author_email='quantumcore@protonmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/quantumcore/BurpGraphQl',
    install_requires=[
          'python_graphql_client',
          'colorama',
          'json'
      ],

)