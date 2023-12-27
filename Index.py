from collections import defaultdict
import json
import struct
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
    token_id = 1

    lexicon = {}
    inverted_index = defaultdict(list)
    total_doc_length = 0
    
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
                            filtered_content = get_filtered_content(content)
                            tokens = tokenize_text(filtered_content, remove_stop_words=True)
                            total_doc_length += len(tokens) 

                            # Count word frequency
                            word_counts = defaultdict(int)
                            for token in tokens:
                                if not (token in lexicon):
                                    token_id += 1
                                    lexicon[token] = token_id
                                word_counts[token_id] += 1

                            # Update inverted index
                            for token_id, freq in word_counts.items():
                                inverted_index[str(token_id)].extend([internal_id, freq])

                            # Save metadata and document content
                            with open(metadata_file_path, 'w+') as mf:
                                json.dump({'internal_id': internal_id, 'title': title, 'categories': categories, 'doc_length': len(tokens)}, mf, indent=2)
                            with open(document_file_path, 'w+') as df:
                                df.write(content)

                            file.close()
                            internal_id += 1

    # Print statistics
    print("Total doc length: {}, Total docs: {}, Average doc length: {}".format(total_doc_length, internal_id - 1, total_doc_length / (internal_id - 1)))

    # Save lexicon and inverted index
    with open(LEXICON_PATH, "w+") as f:
        json.dump(lexicon, f, indent=2)
    with open(INVERTED_LEXICON_PATH, "w+") as f:
        lexicon_inverted = {str(token_id): token for token, token_id in lexicon.items()}
        json.dump(lexicon_inverted, f, indent=2)
    with open(INVERTED_INDEX_PATH, 'w+') as f:
        json.dump(inverted_index, f, indent=2)

def main():
    # Check for command line arguments
    if len(sys.argv) != 2:
        print("Usage: python3 Index.py <enwiki gz folder path>")
        sys.exit(1)

    data_path = sys.argv[1]
    build_index(data_path=data_path)

if __name__ == "__main__":
    main()