from setuptools import setup

setup(
    name='ChemE',
    version='0.0.3',
    description='Various functions and data for Chemical Engineering Students',
    url='https://github.com/ConciseVerbosity18/ChemE_CV.git',
    author='ol-<(',
    include_package_data=True,
    package_data={'':['Data_files/*.txt']},
    packages=['ChemE']
)
