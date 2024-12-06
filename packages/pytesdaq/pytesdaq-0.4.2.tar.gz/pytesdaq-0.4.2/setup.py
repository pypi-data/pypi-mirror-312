from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
      long_description = f.read()


setup(name='pytesdaq',
      version='0.4.2',
      description='DAQ and Intruments control for TES development',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Bruno Serfass',
      author_email='serfass@berkeley.edu',
      url="https://github.com/spice-herald/pytesdaq",
      zip_safe = False,
      include_package_data = True,
      package_data = {
          '': ['*.ini'],
      },
      packages = find_packages(),
      install_requires=[
            'PyQt5',
            'matplotlib',
            'lakeshore',
            'pandas',
            'nidaqmx',
            'pyvisa',
            'paramiko>=3.2.0',
            'walrus',
            'h5py',
            'qetpy>=1.7.2',
            'scipy',
            'seaborn',
            'astropy',
            'lmfit',
            'tables'
      ],
)
