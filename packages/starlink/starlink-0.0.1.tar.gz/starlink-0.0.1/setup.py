from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="starlink",
    version="0.0.1",
    packages=find_packages(),
    description="Unofficial Python wrapper for the STARLINK API by Tarmica Chiwara",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tarmica Chiwara",
    author_email="tarimicac@gmail.com",
    url="https://github.com/lordskyzw/starlink",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)