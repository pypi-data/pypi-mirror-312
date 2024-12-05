# doctor_trans/setup.py

from setuptools import setup, Extension
from Cython.Build import cythonize
import pathlib
import os

# Create the extension for Cython file
pyx_file = "doctor_trans/trans.pyx"
c_file = "doctor_trans/trans.c"

# Check if the .pyx file exists; otherwise, use the .c file
source_file = pyx_file if os.path.exists(pyx_file) else c_file
ext_modules = [
    Extension(
        name="doctor_trans.trans",
        sources=[source_file],  # Use the available source file
    ),
]

# Read the contents of README.md
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name='doctor_trans',
    version='1.0.0',
    packages=['doctor_trans'],
    ext_modules=cythonize(ext_modules),
    include_package_data=True,
    package_data={"doctor_trans": ["*.pyd", "*.so"]},
    install_requires=[
        'pandas',
        'requests'
    ],
    author='Nirmal Patel',
    author_email='nirmalpatel1705@gmail.com',
    description='This package translate whole dataframe in any language without any limits.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=''
)
