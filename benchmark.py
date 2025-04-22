# benchmark.py

import csv
import os
import time
import random

from hashTable import HashTable
from btree import BTree

DATA_DIR = "data/"
CSV_FILES = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]

#running this file prints out results but the same functions are better displayed in the UI

#load buildings is the function used to retrieve the data and store it
def load_buildings():
    buildings = []
    id_counter = 0  # Use to generate unique keys if needed
    for file in CSV_FILES:
        with open(os.path.join(DATA_DIR, file), "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Cleans the record into usable fields
                try:
                    building = {
                        "id": id_counter,
                        "city": row["city_name"],
                        "county": row["countyname"],
                        "type": row["reported_propertytype"],
                        "subtype": row["reported_propertysubtype"],
                        "sq_ft": float(row["rentablebuildingarea_mean"] or 0),
                        "year_built": int(float(row["yearbuilt_mean"] or 0)),
                        "stories": int(float(row["stories"] or 0)),
                    }
                    buildings.append(building)
                    id_counter += 1
                except Exception as e:
                    print(f"Skipping row due to error: {e}")
    return buildings

#this function times and tests how fast the b tree and hash table run and gives us the values.
def benchmark_structures(buildings):
    print(f"\nLoaded {len(buildings)} building records.\n")

    print("Benchmarking Hash Table...")
    ht = HashTable(size=150000)

    start_time = time.time()
    for b in buildings:
        ht.insert(b["id"], b)
    ht_insert_time = time.time() - start_time

    # This function samples 100 random keys for search
    sample_ids = random.sample([b["id"] for b in buildings], min(100, len(buildings)))

    start_time = time.time()
    for key in sample_ids:
        result = ht.search(key)
    ht_search_time = time.time() - start_time

    print("\nBenchmarking B-Tree...")
    bt = BTree(t=3)

    start_time = time.time()
    for b in buildings:
        bt.insert(b["id"], b)
    bt_insert_time = time.time() - start_time

    start_time = time.time()
    for key in sample_ids:
        result = bt.search(key)
    bt_search_time = time.time() - start_time

    print("\n--- Benchmark Results ---")
    print(f"Hash Table - Insert Time: {ht_insert_time:.4f}s")
    print(f"Hash Table - Search Time (100 keys): {ht_search_time:.4f}s")
    print(f"B-Tree     - Insert Time: {bt_insert_time:.4f}s")
    print(f"B-Tree     - Search Time (100 keys): {bt_search_time:.4f}s")
    print("--------------------------\n")
    return (ht_insert_time, bt_insert_time)


if __name__ == "__main__":
    buildings = load_buildings()
    benchmark_structures(buildings)
