from setuptools import setup

setup(
   name='ITS_us',
   version='1.0.0',
   description='ITS_us is a robust package for performing arbitrary single and two qubit quantum operations, structured to intuitively construct quantum circuits.',
   author='Sara Cender, Theo Iosif, Ivan Shalashilin',
   author_email='sara.cender.24@ucl.ac.uk, theodor.iosif.24@ucl.ac.uk, ivan.shalashilin.24@ucl.ac.uk',
   packages=['its_us'],  #same as name
   install_requires=['numpy'], #external packages as dependencies
   scripts=[]
)