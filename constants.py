# Path definitions
INDEX_PATH = './index'
METADATA_PATH = f'./{INDEX_PATH}/metadata'
DOCUMENTS_PATH = f'./{INDEX_PATH}/documents'
LEXICON_PATH = f'./{INDEX_PATH}/token_to_token_id.json'
INVERTED_LEXICON_PATH = f'./{INDEX_PATH}/token_id_to_token.json'
INVERTED_INDEX_PATH = f'./{INDEX_PATH}/inverted_index.json'

# BM25 tuning parameters
K1 = 1.2
B = 0.75
K2 = 0