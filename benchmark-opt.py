import time
from RankedRetreival import rank_documents

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
    for query in benchmark_queries:
        start_time = time.time()
        rank_documents(query, optimized = True)
        end_time = time.time()

        query_time = end_time - start_time
        total_time += query_time

        print(f"Time for '{query}': {query_time:.4f} seconds")

    print(f"\nTotal time for all queries: {total_time:.4f} seconds")

if __name__ == "__main__":
    run_benchmarks()
