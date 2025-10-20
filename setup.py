"""Setup script for Foodler application."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="foodler",
    version="0.1.0",
    author="PrismQDev",
    description="Food management and nutrition calculator application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PrismQDev/Foodler.Research",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Home Automation",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "sqlalchemy>=2.0.0",
        "pandas>=2.0.0",
        "click>=8.1.0",
    ],
    entry_points={
        "console_scripts": [
            "foodler=foodler.cli:cli",
        ],
    },
)
