from setuptools import setup, find_packages

long_description = open('README.rst').read()

setup(name="pyHikUp",
      packages=find_packages(),
      version="0.1.4",
      author="John Owen",
      description="Python wrapper for Hik Device Gateway",
      long_description_content_type='text/markdown',
      long_description=long_description,
      maintainer_email="sales@sensoraccess.co.uk",
      install_requires=['validators', 'requests', 'filetype'],
      #packages=['pyGuardPoint'],
      license_files=('LICENSE.txt',),
      zip_safe=False)
