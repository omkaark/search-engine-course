from collections import defaultdict
import json
import struct
import sys
import os
import tarfile

from constants import *
from utils import *

def build_index(data_path):
    if not data_path:
        print("Error: Data file path not provided")
        sys.exit(1)

    os.makedirs(INDEX_PATH, exist_ok=True)
    os.makedirs(METADATA_PATH, exist_ok=True)
    os.makedirs(DOCUMENTS_PATH, exist_ok=True)

    internal_id = 1
    token_id = 1

    lexicon = {}

    inverted_index: dict[str, list] = defaultdict(list)

    total_doc_length = 0
    
    with tarfile.open(data_path, 'r:gz') as tar:
        for member in tar.getmembers():
            if member.isdir():
                for sub_member in [m for m in tar.getmembers() if m.name.startswith(member.name)]:
                    if sub_member.isfile():
                        file = tar.extractfile(sub_member)
                        if file:
                            word_counts = defaultdict(int)

                            file_name = sub_member.name.encode('utf-8', errors='ignore').decode('utf-8')
                            content = file.read().decode('utf-8', errors='ignore')
                            
                            categories = extract_categories(content)
                            title = extract_title(content)

                            thousands = f"{(internal_id // 1000):03d}"
                            hundreds = f"{(internal_id % 1000) // 100}"
                            file_number = f"{(internal_id % 100):02d}"

                            os.makedirs(os.path.join(METADATA_PATH, thousands, hundreds), exist_ok=True)
                            os.makedirs(os.path.join(DOCUMENTS_PATH, thousands, hundreds), exist_ok=True)

                            metadata_file_path = os.path.join(METADATA_PATH, thousands, hundreds, f"{file_number}.json")
                            document_file_path = os.path.join(DOCUMENTS_PATH, thousands, hundreds, f"{file_number}.txt")

                            filtered_content = get_filtered_content(content)
                            tokens = tokenize_text(filtered_content, remove_stop_words=True)

                            total_doc_length += len(tokens) 

                            word_counts = defaultdict(int)

                            for token in tokens:
                                if not (token in lexicon):
                                    lexicon[token] = token_id
                                    token_id += 1
                                word_counts[token] += 1

                            for token, freq in word_counts.items():
                                token_id_for_postings = lexicon[token]
                                inverted_index[str(token_id_for_postings)].extend([internal_id, freq])

                            with open(metadata_file_path, 'w+') as mf:
                                json.dump({
                                    'internal_id': internal_id,
                                    'title': title,
                                    'categories': categories,
                                    'doc_length': len(tokens)
                                }, mf, indent=2)

                            with open(document_file_path, 'w+') as df:
                                df.write(content)

                            file.close()
                            internal_id += 1

    # CASE-DEPENDANT OPTIMIZATION
    # inverted_index = dict(filter(lambda entry: len(entry[1]) // 2 > 10, inverted_index.items()))

    print("Total doc length: {}, Total docs: {}, Average doc length: {}".format(total_doc_length, internal_id - 1, 1.0 * total_doc_length / (internal_id - 1)))
    
    file_path = os.path.join(INDEX_PATH, 'token_to_token_id.json')
    with open(file_path, "w+") as f:
        token_to_token_id_json = json.dumps(lexicon, indent=2)
        f.write(token_to_token_id_json)

    token_id_to_token = {str(token_id): token for token, token_id in lexicon.items()}
    file_path = os.path.join(INDEX_PATH, 'token_id_to_token.json')
    with open(file_path, "w+") as f:
        token_id_to_token_json = json.dumps(token_id_to_token, indent=2)
        f.write(token_id_to_token_json)

    file_path = os.path.join(f'{INDEX_PATH}', f'inverted_index.json')
    with open(file_path, 'w+') as f:
        json.dump(inverted_index, f, indent=2)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 Index.py <enwiki gz folder path>")
        sys.exit(1)

    data_path = sys.argv[1]

    build_index(data_path=data_path)

if __name__ == "__main__":
    main()
