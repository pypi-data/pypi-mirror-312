from setuptools import setup, find_packages

with open('readme.md','r') as f:
  description=f.read()
# Setting up
setup(
    name="PolyNum",
    version="0.2",
    packages=find_packages(),
    author="Muskan Chaurasia",
    long_description=description,
    long_description_content_type="text/markdown",
)