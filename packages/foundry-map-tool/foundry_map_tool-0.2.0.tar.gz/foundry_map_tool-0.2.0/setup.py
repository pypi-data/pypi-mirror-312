from setuptools import setup




setup(
    name="foundry_map_tool",
    version="0.2.0",
    description="A tool to adjust the scale of maps in JSON files for Foundry VTT.",
    author="Rory Burke",
    author_email="RoryABurke+DAMapTool@gmail.com",
    py_modules=['foundry_map_tool'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'foundry-map-tool=foundry_map_tool:adjust_map',
        ],
    },
)