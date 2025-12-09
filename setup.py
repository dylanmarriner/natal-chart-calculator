#!/usr/bin/env python3
"""
setup.py
Python package setup for the natal chart calculator.
Provides easy installation via pip install.
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="natal-chart-calculator",
    version="2.0.0",
    author="Dylan Marriner",
    author_email="dylan@example.com",
    description="Professional natal chart calculator with compatibility analysis and astrology readings",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/dylanmarriner/natal-chart-calculator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Religion :: Astrology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    include_package_data=True,
    package_data={
        "": ["*.py", "*.md", "*.txt", "*.bsp"],
    },
    entry_points={
        "console_scripts": [
            "natal-chart=natal_chart_enhanced:main",
        ],
        "gui_scripts": [
            "natal-chart-gui=desktop_gui:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pyinstaller>=4.0",
        ],
        "full": [
            "matplotlib>=3.5.0",
            "pandas>=1.3.0",
        ],
    },
    zip_safe=False,
    keywords="astrology, natal-chart, horoscope, compatibility, astronomy",
    project_urls={
        "Bug Reports": "https://github.com/dylanmarriner/natal-chart-calculator/issues",
        "Source": "https://github.com/dylanmarriner/natal-chart-calculator",
        "Documentation": "https://github.com/dylanmarriner/natal-chart-calculator/blob/main/README.md",
    },
)
