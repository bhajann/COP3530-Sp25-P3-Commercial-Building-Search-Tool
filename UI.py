# UI.py
import tkinter as tk
from tkinter import ttk
import time

from hashTable import HashTable
from btree import BTree
from benchmark import load_buildings  # reuses your existing data loader
from benchmark import benchmark_structures
from tkinter import PhotoImage


class BuildingSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Commercial Building Search Tool")
        self.root.geometry("800x500")

        self.root.update()
        self.image = PhotoImage(file="rainbowcat.gif")
        self.image = self.image.subsample(2,2)
        self.imageLabel = tk.Label(root, image=self.image)
        self.imageLabel.grid(row=0, column=0, columnspan=4, pady=20)
        self.loadText = tk.Label(root, text="Loading data, this might take a minute.",font=("Arial", 20))
        self.loadText.place(x=0, y=360)

        self.root.update()
        self.buildings = load_buildings()
        print(f"{len(self.buildings)} buildings loaded.")
        self.dataLoaded = tk.Label(root, text="Data Loaded. Now loading Data Structures...", font=("Arial", 20))
        self.dataLoaded.place(x=0, y=395)
        self.root.update()
        self.build_index()
        self.loadText.destroy()
        self.dataLoaded.destroy()
        self.imageLabel.destroy()

        # Search Input
        tk.Label(root, text="Search By:").grid(
            row=0, column=0, sticky="w", padx=10, pady=10
        )
        self.search_by = tk.StringVar(value="id")
        self.search_dropdown = ttk.Combobox(
            root, textvariable=self.search_by, values=["id", "year_built", "city"]
        )
        self.search_dropdown.grid(row=0, column=1)

        tk.Label(root, text="Search Value:").grid(row=1, column=0, sticky="w", padx=10)
        self.search_entry = tk.Entry(root)
        self.search_entry.grid(row=1, column=1)

        # Data Structure Selection
        self.ds_var = tk.StringVar(value="hash")
        tk.Label(root, text="Choose Data Structure:").grid(
            row=2, column=0, padx=10, sticky="w"
        )
        #-----------------------------------------------------
        tk.Label(root, text="Compare Build Times:").grid(
            row=3, column=0, padx=10, sticky="w"
        )
        tk.Button(root, text="Compare", command=self.compare).grid(
            row=3, column=1, pady=10, sticky="w"
        )
        tk.Radiobutton(
            root, text="Hash Table", variable=self.ds_var, value="hash"
        ).grid(row=2, column=1, sticky="w")
        tk.Radiobutton(
            root, text="Balanced Tree", variable=self.ds_var, value="btree"
        ).grid(row=2, column=2, sticky="w")

        # Buttons
        tk.Button(root, text="Search", command=self.perform_search).grid(
            row=3, column=1, pady=10
        )
        tk.Button(root, text="Clear Results", command=self.clear_results).grid(
            row=3, column=2
        )

        # Results Table
        columns = ("id", "city", "sq_ft", "year_built")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
        self.tree.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Execution Time
        self.time_label = tk.Label(root, text="Execution Time: -- ms")
        self.time_label.grid(row=5, column=0, columnspan=4, pady=10)


    def build_index(self):
        self.indices = {}

        for buildings_pos, b in enumerate(self.buildings):
            for key, value in b.items():
                # TODO: Can bring in more fields if we want
                if key not in ['id', 'city', 'year_built']:
                    continue

                if key not in self.indices:
                    self.indices[key] = {}

                if "hash" not in self.indices[key]:
                    self.indices[key]["hash"] = HashTable(size=150000)

                if "btree" not in self.indices[key]:
                    self.indices[key]["btree"] = BTree(t=3)

                hash_table_search = self.indices[key]["hash"].search(value)
                b_tree_search = self.indices[key]["btree"].search(value)

                if hash_table_search is None:
                    hash_table_search = []

                if b_tree_search is None:
                    b_tree_search = []

                hash_table_search.append(buildings_pos)
                b_tree_search.append(buildings_pos)

                self.indices[key]["hash"].insert(value, hash_table_search)
                self.indices[key]["btree"].insert(value, b_tree_search)

    def perform_search(self):
        search_type = self.search_by.get()
        search_key = self.search_entry.get()
        ds_type = self.ds_var.get()

        try:
            # TODO: Can bring in converting to the float datatype if we want to add any float fields
            search_key = int(search_key)
        except ValueError:
            None

        # Time the search
        start = time.time()
        results = []

        idx_results = self.indices[search_type][ds_type].search(search_key)

        # print(idx_results)

        if idx_results:
            for buildings_pos in idx_results:
                results.append(self.buildings[buildings_pos])

        elapsed = (time.time() - start) * 1000  # ms
        self.display_results(results, elapsed)

    def display_results(self, results, elapsed):
        self.tree.delete(*self.tree.get_children())
        for b in results:
            self.tree.insert(
                "", tk.END, values=(b["id"], b["city"], b["sq_ft"], b["year_built"])
            )
        self.time_label.config(text=f"Execution Time: {elapsed:.2f} ms")


    def clear_results(self):
        self.tree.delete(*self.tree.get_children())
        self.time_label.config(text="Execution Time: -- ms")
    def compare(self):
        hashTime, BTime = benchmark_structures(self.buildings)
        self.insertTime = tk.Label(root, text=f"Hash Table Execution Time: {hashTime:.2f} ms. B Tree Execution Time {BTime:.2f} ms")
        self.insertTime.grid(row=6, column=0, columnspan=4, pady=10)





if __name__ == "__main__":
    root = tk.Tk()
    app = BuildingSearchApp(root)
    root.mainloop()
