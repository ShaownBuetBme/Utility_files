import os
from pathlib import Path

def generate_directory_map(start_path, output_file=None, max_depth=None):
    """
    Generate a visual map of the directory structure starting from start_path.
    
    Args:
        start_path (str): Path to the directory to map
        output_file (str, optional): File to save the output. If None, prints to console.
        max_depth (int, optional): Maximum depth to traverse. None for unlimited.
    """
    start_path = Path(start_path).expanduser().resolve()
    
    if not start_path.exists():
        print(f"Error: Path '{start_path}' does not exist.")
        return
    
    if not start_path.is_dir():
        print(f"Error: '{start_path}' is not a directory.")
        return
    
    # Prepare the output
    output = []
    output.append(f"Directory Map of: {start_path}")
    output.append("=" * 50)
    
    def _walk_dir(directory, prefix='', depth=0):
        if max_depth is not None and depth > max_depth:
            return
            
        # Sort directories and files separately
        try:
            entries = sorted(os.listdir(directory))
        except PermissionError:
            output.append(f"{prefix}[Permission denied: {directory.name}]")
            return
            
        dirs = [e for e in entries if (directory / e).is_dir()]
        files = [e for e in entries if not (directory / e).is_dir()]
        
        for i, dir_name in enumerate(dirs):
            if i == len(dirs) - 1 and not files:
                new_prefix = prefix + "    "
                connector = "└── "
            else:
                new_prefix = prefix + "│   "
                connector = "├── "
                
            output.append(f"{prefix}{connector}{dir_name}/")
            _walk_dir(directory / dir_name, new_prefix, depth + 1)
        
        for i, file_name in enumerate(files):
            if i == len(files) - 1:
                connector = "└── "
            else:
                connector = "├── "
                
            output.append(f"{prefix}{connector}{file_name}")
    
    _walk_dir(start_path)
    
    # Handle output
    map_str = '\n'.join(output)
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(map_str)
            print(f"Directory map saved to: {output_file}")
        except IOError as e:
            print(f"Error writing to file: {e}")
            print("Printing to console instead:")
            print(map_str)
    else:
        print(map_str)

if __name__ == "__main__":
    # Hardcoded path - CHANGE THIS TO YOUR DESIRED PATH
    target_path = r"D:\shaown\Total project\3D\Human mesh Recovery (HRM)"
    
    # Optional output file - uncomment if you want to save to file
    # output_file = r"D:\directory_map.txt"
    output_file = None  # Set to None to print to console
    
    # Optional depth limit - set to None for unlimited
    max_depth = None
    
    generate_directory_map(target_path, output_file, max_depth)
