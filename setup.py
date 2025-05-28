#!/usr/bin/env python3
"""
Setup script for jinn-core economic simulation engine.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_file(filename):
    """Read file contents."""
    with open(os.path.join(os.path.dirname(__file__), filename), 'r', encoding='utf-8') as f:
        return f.read()

# Read requirements
def read_requirements(filename):
    """Read requirements from file."""
    requirements = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                requirements.append(line)
    return requirements

setup(
    name="jinn-core",
    version="0.1.0",
    author="Economic Research Team",
    author_email="research@jinncore.org",
    description="Open-source economic simulation engine for transparent financial risk modeling",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/jinn-core",
    project_urls={
        "Bug Tracker": "https://github.com/your-org/jinn-core/issues",
        "Documentation": "https://jinn-core.readthedocs.io/",
        "Source Code": "https://github.com/your-org/jinn-core",
        "Roadmap": "https://github.com/your-org/jinn-core/blob/main/docs/roadmap.md",
    },
    
    # Package configuration
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    
    # Dependencies
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
        ],
    },
    
    # Python version requirement
    python_requires=">=3.8",
    
    # Package metadata
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Education",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    keywords=[
        "economics", "simulation", "finance", "risk-modeling", 
        "macroeconomics", "policy-analysis", "open-source",
        "federal-reserve", "inflation", "interest-rates"
    ],
    
    # Entry points for command-line tools
    entry_points={
        "console_scripts": [
            "jinn-demo=demo:main",
            "jinn-test=tests.test_engine:main",
        ],
    },
    
    # Package data
    package_data={
        "": ["*.json", "*.md", "*.txt"],
    },
    
    # Additional metadata
    license="MIT",
    platforms=["any"],
    zip_safe=False,
) 