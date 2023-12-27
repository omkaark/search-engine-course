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

def get_filtered_content(content: str) -> str:
    # Filtering content to exclude certain sections
    final_idxs = [idx for idx in [
        content.find('<h2>References</h2>'), 
        content.find('<h2>See also</h2>'), 
        content.find('<h2>Footnotes</h2>'),
        content.find('<h2>External links</h2>'),
        content.find('<h2> External links </h2>')
    ] if idx != -1]
    if final_idxs:
        content = content[:min(final_idxs)] + "</body></html>"

    # Removing styles and scripts from HTML content
    soup = BeautifulSoup(content, 'html.parser')
    body = soup.find('body')
    return body.get_text(separator=' ', strip=True) if body else ''

def tokenize_text(text: str, remove_stop_words: bool = False) -> list[str]:
    # Tokenizing text with optional stop word removal
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text).strip().lower()
    tokens = text.split()

    if remove_stop_words: 
        stop_words = ['call', 'upon', 'still', 'nevertheless', 'down', 'every', 'forty', 'always', 's', 'll', 'm', 'whole', 'side', 'now', 'however', 'an', 'show', 'least', 'give', 'below', 'did', 'sometimes', 'which', 'nowhere', 'per', 'hereupon', 'yours', 'she', 'moreover', 'eight', 'somewhere', 'within', 'whereby', 'few', 'has', 'so', 'have', 'for', 'noone', 'top', 'were', 'those', 'thence', 'eleven', 'after', 'no', 'others', 'ourselves', 'themselves', 'though', 'that', 'nor', 'just', '’s', 'before', 'had', 'toward', 'another', 'should', 'herself', 'and', 'these', 'such', 'elsewhere', 'further', 'next', 'indeed', 'bottom', 'anyone', 'his', 'each', 'then', 'both', 'became', 'third', 'whom', '‘ve', 'mine', 'take', 'many', 'anywhere', 'to', 'well', 'thereafter', 'besides', 'almost', 'front', 'fifteen', 'towards', 'none', 'be', 'herein', 'two', 'using', 'whatever', 'please', 'perhaps', 'full', 'ca', 'we', 'latterly', 'here', 'therefore', 'us', 'how', 'was', 'made', 'the', 'or', 'may',  'namely', 'anyway', 'amongst', 'used', 'ever', 'of', 'there', 'than', 'why', 'really', 'whither', 'in', 'only', 'wherein', 'last', 'under', 'own', 'therein', 'go', 'seems', '‘m', 'wherever', 'either', 'someone', 'up', 'doing', 'on', 'rather', 'ours', 'again', 'same', 'over', 'latter', 'during', 'done', "'re", 'put', "'m", 'much', 'neither', 'among', 'seemed', 'into', 'once', 'my', 'otherwise', 'part', 'everywhere', 'never', 'myself', 'must', 'will', 'am', 'can', 'else', 'although', 'as', 'beyond', 'are', 'too', 'becomes', 'does', 'a', 'everyone', 'but', 'some', 'regarding', '‘ll', 'against', 'throughout', 'yourselves', 'him', "'d", 'it', 'himself', 'whether', 'move', '’m', 'hereafter', 're', 'while', 'whoever', 'your', 'first', 'amount', 'twelve', 'serious', 'other', 'any', 'off', 'seeming', 'four', 'itself', 'nothing', 'beforehand', 'make', 'out', 'very', 'already', 'various', 'until', 'hers', 'they', 'not', 'them', 'where', 'would', 'since', 'everything', 'at', 'together', 'yet', 'more', 'six', 'back', 'with', 'thereupon', 'becoming', 'around', 'due', 'keep', 'somehow', 'n‘t', 'across', 'all', 'when', 'i', 'empty', 'nine', 'five', 'get', 'see', 'been', 'name', 'between', 'hence', 'ten', 'several', 'from', 'whereupon', 'through', 'hereby', "'ll", 'alone', 'something', 'formerly', 'without', 'above', 'onto', 'except', 'enough', 'become', 'behind', '’d', 'its', 'most', 'n’t', 'might', 'whereas', 'anything', 'if', 'her', 'via', 'fifty', 'is', 'thereby', 'twenty', 'often', 'whereafter', 'their', 'also', 'anyhow', 'cannot', 'our', 'could', 'because', 'who', 'beside', 'by', 'whence', 'being', 'meanwhile', 'this', 'afterwards', 'whenever', 'mostly', 'what', 'one', 'nobody', 'seem', 'less', 'do', '‘d', 'say', 'thus', 'unless', 'along', 'yourself', 'former', 'thru', 'he', 'hundred', 'three', 'sixty', 'me', 'sometime', 'whose', 'you', 'quite', '’ve', 'about', 'even']
        tokens = [token for token in tokens if token not in stop_words]

    return tokens
