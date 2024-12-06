
from setuptools import setup, find_packages

setup(
    name="array_subarray_utils",
    version="0.1.0",
    description="A library for calculating subarray sums for arrays and circular arrays",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ashiqur Rahman Sami",
    author_email="samiashiqur@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
