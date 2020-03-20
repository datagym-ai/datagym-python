import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['requests>=2.22.0', ]

test_requirements = ['pytest>=3', ]

setuptools.setup(
   name='datagym',
   version='0.1.2a',
   description='Datagym Python API Wrapper',
   author='Alexej Penner, Johannes Pflugmacher',
   author_email='support@datagym.ai',
   license="BSD license",
   python_requires='>=3.6',
   classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
   long_description=long_description + "\n\n" + history,
   url='https://www.datagym.ai/',
   packages=setuptools.find_packages(include=['datagym', 'datagym.*']),
   install_requires=requirements,
   test_suite='tests',
   tests_require=test_requirements,
   include_package_data=True
)