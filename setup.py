"""Setup script for CoomerDL."""
from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read dev requirements from requirements-dev.txt
try:
    with open('requirements-dev.txt', 'r', encoding='utf-8') as f:
        dev_requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
except FileNotFoundError:
    dev_requirements = []

# Read long description from README
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="coomerdl",
    version="2.1.0",
    author="CoomerDL Contributors",
    description="Universal media downloader with support for 1000+ sites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/primoscope/CoomerDL",
    project_urls={
        "Bug Reports": "https://github.com/primoscope/CoomerDL/issues",
        "Source": "https://github.com/primoscope/CoomerDL",
        "Documentation": "https://github.com/primoscope/CoomerDL/tree/main/docs",
    },
    packages=find_packages(exclude=['tests', 'tests.*', 'scripts', 'scripts.*']),
    package_data={
        'resources': [
            'img/**/*',
            'screenshots/*',
            'config/*.json',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements,
    },
    entry_points={
        'console_scripts': [
            'coomerdl=main:main',
        ],
    },
    include_package_data=True,
    keywords='downloader media coomer kemono youtube scraper',
    zip_safe=False,
)
