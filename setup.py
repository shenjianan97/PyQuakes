from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyquakes',
    version='0.0.1',
    author='Jianan Shen, Chen Mo',
    author_email="shenjianan97@gmail.com, mochen1228@gmail.com",
    license_files=('LICENSE.txt',),
    description=('PyQuakes is a Python wrapper for USGS Earthquake Catalog API that manages data querying and '
                 'result processing.'),
    package_dir={'pyquakes': 'src'},
    packages=['pyquakes', 'pyquakes.enum'],
    install_requires=[
        "requests >= 2.15.0"
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/shenjianan97/PyQuakes'
)
