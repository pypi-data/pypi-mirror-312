from os import environ
from pathlib import Path
from sys import base_prefix
import json

def adjust_map(scale_factor=2):
    """
    Adjust the scale of a map in a JSON file.
    This function sets the environment variables for TCL and TK libraries, 
    opens a file dialog to select a JSON file, and adjusts the scale of various 
    elements in the map based on a specified scale factor. The adjusted map is 
    then saved to a new JSON file.
    Raises:
        ValueError: If no file is selected.
    Environment Variables:
        TCL_LIBRARY: Path to the TCL library.
        TK_LIBRARY: Path to the TK library.
    File Dialog:
        Opens a file dialog to select a JSON file from the "data" folder.
    JSON Adjustments:
        - Adjusts the width and height of the map.
        - Adjusts the grid size and sets grid alpha to 0 if in Foundry format.
        - Adjusts the positions of lights, walls, drawings, tokens, notes, and tiles.
    Output:
        Saves the adjusted map to a new JSON file with "_adjusted" appended to the original name.
    """
    environ["TCL_LIBRARY"] = str(Path(base_prefix) / "tcl" / "tcl8.6")
    environ["TK_LIBRARY"] = str(Path(base_prefix) / "tcl" / "tk8.6")
    import tkinter as tk
    from tkinter import filedialog

    # Choose the file to load from data folder
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.askopenfilename(
        initialdir="data",
        title="Select file to convert",
        filetypes=(("JSON files", "*.json"), ("all files", "*.*")),
    )

    if not file_path:
        raise ValueError("No file selected")

    # Load the data
    with open(file_path, "r") as file:
        map_info = json.load(file)

    # Override the width and height in the map_info
    map_info["width"] *= (1 * scale_factor)
    map_info["height"] *= (1 * scale_factor)
    
    #checks if json is in DA format (grid is on the top level) or in Foundry format (grid is in a dictionary)
    if isinstance(map_info["grid"], (int, float)):
        map_info["grid"] *= (1/scale_factor)
    else:
        map_info["grid"]["size"] *= (1/scale_factor)
        map_info["grid"]["alpha"] = 0

    if "lights" in map_info:
        for light in map_info["lights"]:
            light["x"] *= (1 * scale_factor)
            light["y"] *= (1 * scale_factor)

    if "walls" in map_info:
        for wall in map_info["walls"]:
            wall["c"] = [value * (1 * scale_factor) for value in wall["c"]]

    if "drawings" in map_info:
        for drawing in map_info["drawings"]:
            drawing["x"] *= (1 * scale_factor)
            drawing["y"] *= (1 * scale_factor)

    if "tokens" in map_info:
        for token in map_info["tokens"]:
            if "token-attacher" in token:
                token["token-attacher"]["pos"]["xy"]["x"] *= (1 * scale_factor)
                token["token-attacher"]["pos"]["xy"]["y"] *= (1 * scale_factor)
                token["token-attacher"]["center"]["x"] *= (1 * scale_factor)
                token["token-attacher"]["center"]["y"] *= (1 * scale_factor)

            token["x"] *= (1 * scale_factor)
            token["y"] *= (1 * scale_factor)
 
    if "notes" in map_info:
        for note in map_info["notes"]:
            note["x"] *= (1 * scale_factor)
            note["y"] *= (1 * scale_factor)
            
    if "tiles" in map_info:
        for tile in map_info["tiles"]:
            tile["x"] *= (1 * scale_factor)
            tile["y"] *= (1 * scale_factor)

            
    name = map_info["name"] + "_adjusted.json"
    with open(rf"data\{name}", "w") as file:
        json.dump(map_info, file, indent=(1 * scale_factor))

    return

def main():
    adjust_map()

if __name__ == "__main__":
    main()
