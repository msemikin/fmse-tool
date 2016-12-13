from setuptools import setup, find_packages

setup(name='fmse_tool',
      version='2.0.0',
      packages=find_packages(),
      install_requires=[
          'docopt',
          'graphviz',
          'ply'
      ]
      )
