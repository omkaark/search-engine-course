import sys
import os
from utils import get_file_paths

# Function to print contents of a file
def print_file_contents(file_path):
    # Check if file exists
    if os.path.exists(file_path):
        # Open and read file
        with open(file_path, 'r') as file:
            print(file.read())
    else:
        # Print error if file not found
        print(f"File not found: {file_path}")

def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python3 GetDoc.py <internal_id>")
        sys.exit(1)

    # Get internal ID from command line argument
    internal_id = int(sys.argv[1])
    # Retrieve metadata and document paths
    metadata_path, document_path = get_file_paths(internal_id)

    # Print metadata
    print("Metadata:")
    print_file_contents(metadata_path)

    # Print document
    print("\nDocument:")
    print_file_contents(document_path)

# Run main function when script is executed
if __name__ == "__main__":
    main()
