
from setuptools import setup, find_packages

setup(
    name="DA-Map-Zoom",
    version="0.1.0",
    description="A tool to adjust the scale of maps in JSON files for Foundry VTT.",
    author="Rory Burke",
    author_email="norraist+DAMapToll@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.2.3",
    ],
    entry_points={
        'console_scripts': [
            'foundry-map-tool=Zoom_Map:main',
        ],
    },
)

setup()