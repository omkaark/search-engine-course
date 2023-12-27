import json
import os
import traceback
from constants import INDEX_PATH
from utils import *

inverted_index_file = os.path.join(INDEX_PATH, 'inverted_index.json')
with open(inverted_index_file, 'r') as file:
    inverted_index = json.load(file)

lexicon_file = os.path.join(INDEX_PATH, 'token_to_token_id.json')
with open(lexicon_file, 'r') as file:
    lexicon = json.load(file)

def boolean_and(text):
    tokens = tokenize_text(text, remove_stop_words=True)

    doc_ids = set()
    token_id = lexicon.get(tokens[0], None)
    if token_id:
        doc_ids = set(inverted_index[str(token_id)][::2])
    
    for token in tokens[1:]:
        token_id = lexicon.get(token, None)
        posting_list = inverted_index[str(token_id)] or []
        local_doc_ids = set(posting_list[::2])
        doc_ids = doc_ids.intersection(local_doc_ids)

    print('doc_ids', len(doc_ids))

    doc_ids = sorted(list(doc_ids))

    for i in range(0, min(len(doc_ids), 10)):
        print_metadata(doc_ids[i])

def main():
    query = input('Query: ')
    while query and query != '-1':
        try:
            boolean_and(query)
        except Exception as e:
            print(traceback.format_exc())
        query = input('Query: ')

if __name__ == "__main__":
    main()
