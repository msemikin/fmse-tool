from setuptools import setup

setup(name='fmse_tool',
      version='2.0.0',
      packages=['fmse_tool'],
      entry_points={
          'console_scripts': [
              'fmse_tool = fmse_tool.__main__:main'
          ]
      },
      install_requires=[
          'docopt',
          'graphviz'
      ]
      )
