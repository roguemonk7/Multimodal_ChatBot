import os

root_dir = "."
excluded_files = {"autoplay.py", "bot_voice.py","brain.py","human_voice.py","app.py"}  # Add more files if needed

for foldername, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.lower().endswith(".py") and filename not in excluded_files:
            file_path = os.path.join(foldername, filename)
            
            # Ask for confirmation to delete
            delete = input(f"Do you want to delete the file: {file_path}? (y/n): ").strip().lower()
            
            if delete == 'y':
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            else:
                print(f"Skipped: {file_path}")

