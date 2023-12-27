import sys
import os
from utils import get_file_paths

def print_file_contents(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            print(file.read())
    else:
        print(f"File not found: {file_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 GetDoc.py <internal_id>")
        sys.exit(1)

    internal_id = int(sys.argv[1])
    metadata_path, document_path = get_file_paths(internal_id)

    print("Metadata:")
    print_file_contents(metadata_path)

    print("\nDocument:")
    print_file_contents(document_path)

if __name__ == "__main__":
    main()
