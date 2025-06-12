import os
import shutil
from pathlib import Path

SCREENSHOTS_DIRECTORY = "C:/Users/CHRISTOPHER/Pictures/Screenshots"

def get_newest_screenshot() -> str:
    files = [f for f in os.listdir(SCREENSHOTS_DIRECTORY) if f.endswith(".png")]
    if not files:
        return ""
    newest_file = max(files, key=lambda f: os.path.getctime(os.path.join(SCREENSHOTS_DIRECTORY, f)))
    return newest_file

def list_categories() -> str:
    categories = "["
    for category in os.listdir(SCREENSHOTS_DIRECTORY):
        category_path = os.path.join(SCREENSHOTS_DIRECTORY, category)
        if os.path.isdir(category_path):
            categories += f"'{category}', "
    categories += "]"
    return categories

def create_directory(directory_name: str) -> None:
    new_directory_path = os.path.join(SCREENSHOTS_DIRECTORY, directory_name)
    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path)

def rename_and_move_screenshot(filename: str, new_name: str) -> None:
    """
    Rename and move a screenshot file.
    """
    screenshots_dir = Path(SCREENSHOTS_DIRECTORY)
    source_path = screenshots_dir / filename
    destination_path = screenshots_dir / new_name
    
    print(f"Attempting to move:")
    print(f"  From: {source_path}")
    print(f"  To: {destination_path}")
    
    # Check if source exists, if not, try to find similar files
    if not source_path.exists():
        print(f"Source file not found: {filename}")
        
        # List all PNG files in the directory
        png_files = list(screenshots_dir.glob("*.png"))
        print(f"Available PNG files: {[f.name for f in png_files]}")
        
        # Try to find a file with similar name
        similar_files = [f for f in png_files if any(word in f.name.lower() for word in filename.lower().split('_'))]
        if similar_files:
            print(f"Similar files found: {[f.name for f in similar_files]}")
            # You might want to use the most recent or ask user to confirm
            source_path = similar_files[0]  # Use first match
            print(f"Using file: {source_path.name}")
        else:
            raise FileNotFoundError(f"No file found matching: {filename}")
    
    # Create destination directory if needed
    if destination_path.parent != screenshots_dir:
        print(f"\nCreating directory: {destination_path.parent}\n")
        destination_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Perform the move
    try:
        shutil.move(str(source_path), str(destination_path))
        print(f"✅ Successfully moved to: {destination_path}\n")
    except Exception as e:
        print(f"❌ Error during move: {e}\n")
        raise