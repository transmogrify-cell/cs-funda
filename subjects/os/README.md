# MOD-02 · Operating Systems

> What actually happens between your code and the hardware.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/divider-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="../../assets/divider-light.svg">
  <img alt="" src="../../assets/divider-light.svg" width="100%">
</picture>

## Topics

| Done | Topic | What to actually understand |
|:--:|---|---|
| `[ ]` | Processes & threads | Address space, context switch cost, `fork` vs `clone` |
| `[ ]` | CPU scheduling | FCFS, SJF, round robin, CFS; turnaround vs response |
| `[ ]` | Synchronisation | Mutex, semaphore, condition variable, the mutual-exclusion proof |
| `[ ]` | Deadlock | Coffman conditions, banker's algorithm, why prevention usually wins |
| `[ ]` | Memory management | Contiguous allocation, fragmentation, buddy allocator |
| `[ ]` | Virtual memory | Paging, TLB, page-replacement policies, thrashing |
| `[ ]` | File systems | inodes, journalling, `fsync` and what "durable" really means |
| `[ ]` | I/O & disk | Interrupts vs polling, DMA, elevator scheduling, SSD reality |
| `[ ]` | Virtualisation | Hypervisors, containers, namespaces & cgroups |

Tick a box here when the note exists **and** you could explain it without it.

## Folder shape

```
os/
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
