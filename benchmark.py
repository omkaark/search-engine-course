# Import required modules
import sys
import time
from RankedRetrieval import rank_documents

# List of benchmark queries
benchmark_queries = [
    "History of the Internet",
    "Climate change effects and solutions",
    "List of Nobel Prize winners in Physics",
    "Comparison of programming languages",
    "Cultural impact of The Beatles",
    "Quantum mechanics and its applications",
    "Ancient civilizations of the Mediterranean",
    "Future of space exploration",
    "Artificial intelligence in healthcare",
    "Impact of social media on mental health"
]

def run_benchmarks():
    total_time = 0
    
    # Iterate through each query and calculate the time taken to rank documents
    for query in benchmark_queries:
        start_time = time.time()
        rank_documents(query, optimized=True)
        end_time = time.time()

        query_time = end_time - start_time
        total_time += query_time

        print(f"Time for '{query}': {query_time:.4f} seconds")

    # Print the total time taken for all queries
    print(f"\nTotal time for all queries: {total_time:.4f} seconds")

# Main entry point of the script
if __name__ == "__main__":
    run_benchmarks()