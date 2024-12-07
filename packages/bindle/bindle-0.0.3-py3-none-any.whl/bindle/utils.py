import os
import shutil
import yaml
from datetime import datetime
import pandas as pd


class Config:
    def __init__(self, data: dict):
        for key, value in data.items():
            if isinstance(value, dict):
                value = Config(value)  # Recursively create Config objects for nested dictionaries
            setattr(self, key, value)

    def __repr__(self):
        return f"Config({self.__dict__})"

def _ensure_config_directory(package_name: str):
    """Ensure the configuration directory exists for the package."""
    config_dir = os.path.expanduser(f"~/.config/{package_name}")
    os.makedirs(config_dir, exist_ok=True)
    return config_dir

def write_config(package_name: str, **kwargs):
    """Write configuration to a YAML file."""
    config_dir = _ensure_config_directory(package_name)
    config_path = os.path.join(config_dir, "config.yaml")
    
    with open(config_path, 'w') as file:
        yaml.dump(kwargs, file)

def read_config(package_name: str) -> dict:
    """Read configuration from the YAML file and return as a dictionary."""
    config_dir = os.path.expanduser(f"~/.config/{package_name}")
    config_path = os.path.join(config_dir, "config.yaml")
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found for package: {package_name}")
    
    with open(config_path, 'r') as file:
        config_data = yaml.safe_load(file)

    return Config(config_data)

def read_file(filepath: str) -> str:
    """Reads the contents of a file and returns it as a single string."""
    with open(filepath, 'r') as file:
        return file.read()

def select_sheet_interactively(filepath: str) -> str:
    """
    Lists the sheet names of an Excel file and prompts the user to select one interactively.
    
    Args:
        filepath: The path to the Excel file.
        
    Returns:
        The selected sheet name as a string.
    """
    sheet_names = pd.ExcelFile(filepath).sheet_names
    print("Available sheets:")
    for index, sheet in enumerate(sheet_names, start=1):
        print(f"{index}. {sheet}")
    
    while True:
        try:
            choice = int(input("Select a sheet number: "))
            if 1 <= choice <= len(sheet_names):
                return sheet_names[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(sheet_names)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def move_recent_downloads(target_dir=os.getcwd()):
    downloads_dir = os.path.expanduser("~/Downloads")
    today = datetime.today().date()
    
    # List recent files
    recent_files = []
    for file_name in os.listdir(downloads_dir):
        file_path = os.path.join(downloads_dir, file_name)
        if os.path.isfile(file_path):
            file_date = datetime.fromtimestamp(os.path.getmtime(file_path)).date()
            if file_date == today:
                recent_files.append(file_name)
    
    # Display files for selection
    if not recent_files:
        print("No files downloaded today.")
        return
    
    print("Select files to move by entering their numbers separated by space:")
    for i, file_name in enumerate(recent_files):
        print(f"{i + 1}: {file_name}")
    
    # Get user selection
    selected_indices = input("Enter file numbers: ").strip()
    selected_indices = selected_indices.split()
    
    # Move selected files
    for index in selected_indices:
        try:
            file_index = int(index) - 1
            if 0 <= file_index < len(recent_files):
                source_path = os.path.join(downloads_dir, recent_files[file_index])
                shutil.move(source_path, target_dir)
                print(f"Moved: {recent_files[file_index]}")
            else:
                print(f"Invalid selection: {index}")
        except ValueError:
            print(f"Invalid input: {index}")
