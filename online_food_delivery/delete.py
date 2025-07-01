import os

for root, dirs, files in os.walk("."):
    if "migrations" in root:
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                file_path = os.path.join(root, file)
                print(f"Deleting: {file_path}")
                os.remove(file_path)
