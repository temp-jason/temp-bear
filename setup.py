from setuptools import setup

setup(
   name='atm',
   version='1.0',
   description='ATM',
   packages=['app'],  #same as name
   install_requires=['pytest'], #external packages as dependencies
)
