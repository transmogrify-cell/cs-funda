# MOD-03 · Database Systems

> Where the data actually lives, and what it costs to keep it correct.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/divider-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="../../assets/divider-light.svg">
  <img alt="" src="../../assets/divider-light.svg" width="100%">
</picture>

## Topics

| Done | Topic | What to actually understand |
|:--:|---|---|
| `[ ]` | Relational model | Relations, keys, relational algebra |
| `[ ]` | SQL | Joins, window functions, `EXPLAIN` output |
| `[ ]` | Normalisation | 1NF → BCNF, and when denormalising is correct |
| `[ ]` | Indexing | B+ tree layout, covering indexes, hash vs ordered |
| `[ ]` | Transactions | ACID, isolation levels, the anomaly each one permits |
| `[ ]` | Concurrency control | 2PL, MVCC, snapshot isolation, write skew |
| `[ ]` | Recovery | WAL, ARIES, checkpointing |
| `[ ]` | Query optimisation | Cost models, join ordering, cardinality estimation |
| `[ ]` | NoSQL | KV / document / column / graph, and what they trade away |

Tick a box here when the note exists **and** you could explain it without it.

## Folder shape

```
dbms/
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
