# MOD-01 · Data Structures & Algorithms

> The base layer. Everything above assumes you can reason about cost.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/divider-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="../../assets/divider-light.svg">
  <img alt="" src="../../assets/divider-light.svg" width="100%">
</picture>

## Topics

| Done | Topic | What to actually understand |
|:--:|---|---|
| `[ ]` | Arrays & strings | Cache locality, why `vector` beats `list` far more often than Big-O suggests |
| `[ ]` | Linked lists | Pointer surgery, dummy heads, cycle detection (Floyd) |
| `[ ]` | Stacks & queues | Monotonic stack, deque, amortised analysis |
| `[ ]` | Hashing | Open addressing vs chaining, load factor, hash flooding |
| `[ ]` | Trees | BST invariants, traversals, AVL/red-black rotations |
| `[ ]` | Heaps | Sift up/down, heapify in O(n), k-th element problems |
| `[ ]` | Graphs | Adjacency representations, BFS/DFS, Dijkstra, topological sort |
| `[ ]` | Sorting | Quicksort pivots, merge stability, why `std::sort` is introsort |
| `[ ]` | Recursion & backtracking | Recursion tree, pruning, state restoration |
| `[ ]` | Greedy | Exchange argument — proving a greedy choice is safe |
| `[ ]` | Dynamic programming | State design, memo → tabulation, space compression |
| `[ ]` | Tries | Prefix search, memory cost, compressed tries |
| `[ ]` | Segment tree / Fenwick | Range queries, lazy propagation |
| `[ ]` | Disjoint set union | Path compression + union by rank, near-O(1) |

Tick a box here when the note exists **and** you could explain it without it.

## Folder shape

```
dsa/
├── README.md     # this file — the checklist
├── notes/        # one file per topic, one page each
├── code/         # from-scratch implementations
└── diagrams/     # SVG or mermaid sources
```

## Conventions

- One topic per file, named `NN-topic-name.md`
- Every note ends with a **Trade-off** line — what this approach gives up
- Code compiles clean: `g++ -std=c++20 -O2 -Wall -Wextra`

[← back to the roadmap](../../README.md)
