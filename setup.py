from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyearthquake',
    version='0.0.1',
    description=('PyEarthquake is a Python wrapper for USGS Earthquake Catalog API that manages data querying and '
                 'result processing.'),
    package_dir={'pyearthquake': 'src'},
    packages=['pyearthquake', 'pyearthquake.enum'],
    install_requires=[
        "requests >= 2.15.0"
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/shenjianan97/PyEarthquake'
)
