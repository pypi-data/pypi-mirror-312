from setuptools import setup
import os

# Ensure the 'data' folder exists
def create_data_folder():
    data_folder = "data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        

create_data_folder()


setup(
    name="foundry_map_tool",
    version="0.1.6",
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