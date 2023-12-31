# Search Engine Course Project

This project is part of the Search Engine Course By [Omkaar Kamath](https://www.linkedin.com/in/omkaark "Omkaar's Linkedin"). I write no-fluff distributed systems breakdowns for busy engineers at [theblueprint.dev](https://blueprint.interviewpen.com?utm_source=secourse) for 5000+ SWEs!

It demonstrates the implementation of a basic search engine using Python. The project includes scripts for indexing documents, performing boolean retrieval, and ranked retrieval using the BM25 algorithm.

## Project Structure

- `constants.py`: Defines the constants used across the project.
- `GetDoc.py`: Retrieves and displays the metadata and document content based on the internal document ID.
- `Index.py`: Handles the indexing of documents, creating the inverted index, and lexicon.
- `RankedRetreival.py`: Implements ranked retrieval using the BM25 algorithm.
- `Retreival.py`: Performs basic boolean retrieval.
- `utils.py`: Contains utility functions used across the project.

### Where to find the data

Data: http://datasets.opentestset.com/datasets/enwiki_2011/download/enwiki_2012_basic.tar.gz

## How to use

1. Clone the repository:
   ```bash
   git clone https://github.com/omkaark/search-engine-course.git
   ```
2. Ensure Python (version 3.x) is installed on your system and install requirements
   ```bash
   pip install -r requirements.txt
   ```
3. Navigate to the project directory:
   ```bash
   cd search-engine-course-project
   ```
4. Place your downloaded data file (in .gz format) in a designated directory.
5. Run Index.py with the path to your data files:

   ```bash
   python3 Index.py <path-to-data-gz>
   ```

6. To retrieve a document by its internal ID:
   ```bash
   python3 GetDoc.py <internal_id>
   ```
7. To retrieve a document by its internal ID:
   ```
   python3 Retreival.py
   ```
8. To perform ranked retrieval:
   ```
   python3 RankedRetreival.py
   ```
9. Run your benchmark:
   ```
   python3 benchmark.py
   ```

## Contributing

Contributions to this project are welcome. Please follow the standard fork-and-pull request workflow.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

This project is inspired by the teachings of Mark Smucker in MSCI 541 and content from the `Search Engines: Information Retrieval in Practice` Textbook
