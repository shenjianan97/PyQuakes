from setuptools import setup

setup(
    name='pyearthquake',
    version='0.0.1',
    description=('PyEarthquake is a Python wrapper for USGS Earthquake Catalog API that manages data querying and '
                 'result processing.'),
    package_dir={'': 'src'},
    packages=['pyearthquake', 'pyearthquake.enum']
)