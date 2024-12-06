# setup.py
from setuptools import setup, find_packages

setup(
    name="foop",
    version="60.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple Python package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/foop",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)