# UI.py

import tkinter as tk
from tkinter import ttk
import time

from hashTable import HashTable
from btree import BTree
from benchmark import load_buildings  # reuses your existing data loader


class BuildingSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Commercial Building Search Tool")
        self.root.geometry("800x500")

        self.buildings = load_buildings()
        self.build_index()

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
        self.hash_table = HashTable(size=100_000)
        self.b_tree = BTree(t=3)
        for b in self.buildings:
            self.hash_table.insert(b["id"], b)
            self.b_tree.insert(b["id"], b)

    def perform_search(self):
        search_type = self.search_by.get()
        value = self.search_entry.get()
        ds_type = self.ds_var.get()

        # Time the search
        start = time.time()
        results = []

        if ds_type == "hash":
            for b in self.buildings:
                if str(b[search_type]) == value:
                    results.append(b)
        else:
            # Only id is indexed in BTree
            if search_type == "id":
                b = self.b_tree.search(value)
                if b:
                    results.append(b)

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


if __name__ == "__main__":
    root = tk.Tk()
    app = BuildingSearchApp(root)
    root.mainloop()
