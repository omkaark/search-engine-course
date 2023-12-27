import json
import os
import math
from collections import defaultdict
import traceback
from constants import B, INDEX_PATH, K1, K2
from utils import get_file_paths, print_metadata, tokenize_text

inverted_index_file = os.path.join(INDEX_PATH, 'inverted_index.json')
with open(inverted_index_file, 'r') as file:
    inverted_index = json.load(file)

lexicon_file = os.path.join(INDEX_PATH, 'token_to_token_id.json')
with open(lexicon_file, 'r') as file:
    lexicon = json.load(file)

total_doc_length = 39395100
total_docs = 16230
avdl = total_doc_length / total_docs

def get_document_ids_for_term(term: str) -> list:
    token_id = str(lexicon.get(term, ''))
    if not token_id or token_id not in inverted_index:
        return []
    postings = inverted_index[token_id]
    doc_ids = postings[::2]
    return doc_ids

def calculate_term_frequency(term: str, document_id: int, optimized = False) -> int:
    token_id = str(lexicon.get(term, ''))
    if not token_id or token_id not in inverted_index:
        return 0
    postings = inverted_index[token_id]

    if optimized:
        left, right = 0, len(postings) // 2
        while left < right:
            mid = left + (right - left) // 2
            mid_doc_id = postings[2 * mid]
            if mid_doc_id == document_id:
                return postings[2 * mid + 1]
            elif mid_doc_id < document_id:
                left = mid + 1
            else:
                right = mid
    else:
        for i in range(0, len(postings), 2):
            if postings[i] == document_id:
                return postings[i + 1]
    return 0

def get_doc_length(doc_id):
    metadata_path, _ = get_file_paths(doc_id)
    with open(metadata_path) as f:
        metadata = json.load(f)
        return metadata['doc_length']

def calculate_bm25(doc_id, query_terms, N=total_docs, k1=K1, b=B, k2=K2, optimized = False):
    total = 0
    for term in query_terms:
        fi = calculate_term_frequency(term, doc_id, optimized)
        ni = len(get_document_ids_for_term(term))
        qfi = query_terms.count(term)
        dl = get_doc_length(doc_id)
        K = k1 * ((1 - b) + b * dl / avdl)
        total += ((k1 + 1) * fi / (K + fi)) * ((k2 + 1) * qfi / (k2 + qfi)) * math.log((N - ni + 0.5) / (ni + 0.5) + 1)
    return total

def rank_documents(query: str, optimized = False) -> list:
    query_terms = tokenize_text(query, remove_stop_words=True)
    document_scores = defaultdict(float)
    unique_document_ids = set()

    for term in query_terms:
        doc_ids = get_document_ids_for_term(term)
        unique_document_ids.update(doc_ids)

    for document_id in unique_document_ids:
        score = calculate_bm25(document_id, query_terms, optimized=optimized)
        document_scores[document_id] = score

    ranked_documents = [{'internal_id': doc_id, 'score': score} for doc_id, score in sorted(document_scores.items(), key=lambda item: item[1], reverse=True)]
    return ranked_documents

def main():
    query = input('Query: ')
    while query and query != '-1':
        try:
            top_documents = rank_documents(query)[:10]
            for i in top_documents:
                print_metadata(i['internal_id'])
                print()
        except Exception as e:
            print(traceback.format_exc())
        query = input('Query: ')

if __name__ == "__main__":
    main()