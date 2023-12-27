import json
import sys
import os
import tarfile

from constants import *
from utils import *

# Builds an index from the provided data path
def build_index(data_path):
    # Check for data path
    if not data_path:
        print("Error: Data file path not provided")
        sys.exit(1)

    # Create necessary directories
    os.makedirs(INDEX_PATH, exist_ok=True)
    os.makedirs(METADATA_PATH, exist_ok=True)
    os.makedirs(DOCUMENTS_PATH, exist_ok=True)

    internal_id = 1
    
    # Process each file in the tar archive
    with tarfile.open(data_path, 'r:gz') as tar:
        for member in tar.getmembers():
            if member.isdir():
                for sub_member in [m for m in tar.getmembers() if m.name.startswith(member.name)]:
                    if sub_member.isfile():
                        file = tar.extractfile(sub_member)
                        if file:
                            content = file.read().decode('utf-8', errors='ignore')
                            
                            # Extract metadata and tokenize content
                            categories = extract_categories(content)
                            title = extract_title(content)
                            metadata_file_path, document_file_path = get_file_paths(internal_id)

                            # Make folders if they do not exist
                            os.makedirs(os.path.dirname(metadata_file_path), exist_ok=True)
                            os.makedirs(os.path.dirname(document_file_path), exist_ok=True)

                            # Save metadata and document content
                            with open(metadata_file_path, 'w+') as mf:
                                json.dump({'internal_id': internal_id, 'title': title, 'categories': categories}, mf, indent=2)
                            with open(document_file_path, 'w+') as df:
                                df.write(content)

                            file.close()
                            internal_id += 1

def main():
    # Check for command line arguments
    if len(sys.argv) != 2:
        print("Usage: python3 Index.py <enwiki gz folder path>")
        sys.exit(1)

    data_path = sys.argv[1]
    build_index(data_path)

if __name__ == "__main__":
    main()