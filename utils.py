import json
import os
import re
from bs4 import BeautifulSoup

from constants import DOCUMENTS_PATH, METADATA_PATH

def get_file_paths(internal_id):
    # Constructing file paths based on internal ID
    thousands = f"{(internal_id // 1000):03d}"
    hundreds = f"{(internal_id % 1000) // 100}"
    file_number = f"{(internal_id % 100):02d}"

    # Paths for metadata and document files
    metadata_file_path = os.path.join(METADATA_PATH, thousands, hundreds, f"{file_number}.json")
    document_file_path = os.path.join(DOCUMENTS_PATH, thousands, hundreds, f"{file_number}.txt")

    return metadata_file_path, document_file_path

def print_metadata(internal_id: str):
    # Printing metadata for a given internal ID
    metadata_file_path, documents_file_path = get_file_paths(internal_id)
    if os.path.exists(metadata_file_path):
        with open(metadata_file_path, 'r') as mf:
            metadata = json.load(mf)
            print(f"{metadata['internal_id']}: {metadata['title']}")
            print("Metadata file:", metadata_file_path)
            print("Document file:", documents_file_path)

def extract_categories(content):
    # Extracting categories from the content
    categories_raw = content.split('>Category:')[1:]
    categories = [category.split('</a>')[0] for category in categories_raw]
    return categories

def extract_title(content):
    # Extracting the title from the content
    match = re.search('<title>(.*?)</title>', content, re.IGNORECASE)
    return match.group(1) or ""