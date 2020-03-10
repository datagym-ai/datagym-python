import setuptools

with open("README", 'r') as f:
    long_description = f.read()

setuptools.setup(
   name='datagym',
   version='0.1',
   description='Datagym Python API Wrapper',
   author='Alexej Penner, Johannes Pflugmacher',
   author_email='support@datagym.ai',
   url='https://www.datagym.ai/',
   packages=setuptools.find_packages(),
   install_requires=["requests>=2.22.0"],
)