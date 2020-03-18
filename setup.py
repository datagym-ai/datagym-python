import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

requirements = ['requests>=2.22.0', ]

test_requirements = ['pytest>=3', ]

setuptools.setup(
   name='datagym',
   version='0.1.1',
   description='Datagym Python API Wrapper',
   author='Alexej Penner, Johannes Pflugmacher',
   author_email='support@datagym.ai',
   license="BSD license",
   long_description=long_description,
   url='https://www.datagym.ai/',
   packages=setuptools.find_packages(include=['datagym', 'datagym.*']),
   install_requires=requirements,
   test_suite='tests',
   tests_require=test_requirements,
)