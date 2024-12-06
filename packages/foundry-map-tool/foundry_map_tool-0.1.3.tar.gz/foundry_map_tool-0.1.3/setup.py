from setuptools import setup, find_packages

setup(
    name="foundry_map_tool",
    version="0.1.3",
    description="A tool to adjust the scale of maps in JSON files for Foundry VTT.",
    author="Rory Burke",
    author_email="RoryABurke+DAMapTool@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.2.3",
    ],
    entry_points={
        'console_scripts': [
            'foundry-map-tool=foundry_map_tool.Zoom_Map:adjust_map',
        ],
    },
)

setup()