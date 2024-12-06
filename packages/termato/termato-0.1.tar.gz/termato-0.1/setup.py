from setuptools import setup, find_packages
from termoto import __version__

# Read the long description from README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="termato",
    version=__version__,
    author="Darshan P.",
    author_email="drshnp@outlook.com",
    license="MIT",
    description="A simple CLI Pomodoro timer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/1darshanpatil/termato",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "termato=termoto.cli:main",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "Topic :: Office/Business :: Scheduling",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "colorama",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    keywords="pomodoro, cli, time, productivity",
    project_urls={
        "Documentation": "https://github.com/1darshanpatil/termoto#readme",
        "Source": "https://github.com/1darshanpatil/termoto",
        "Tracker": "https://github.com/1darshanpatil/termoto/issues",
    },
)
