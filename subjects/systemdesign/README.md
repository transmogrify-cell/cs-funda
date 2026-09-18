# MOD-06 · System Design

> Putting the previous five together, under load, with money on the line.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/divider-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="../../assets/divider-light.svg">
  <img alt="" src="../../assets/divider-light.svg" width="100%">
</picture>

## Topics

| Done | Topic | What to actually understand |
|:--:|---|---|
| `[ ]` | Estimation | Back-of-envelope: QPS, storage, bandwidth, latency budgets |
| `[ ]` | Load balancing | L4 vs L7, health checks, sticky sessions |
| `[ ]` | Caching | Cache-aside vs write-through, eviction, stampede, invalidation |
| `[ ]` | Sharding | Range vs hash, hot keys, resharding pain |
| `[ ]` | Replication | Sync vs async, read-your-writes, replica lag |
| `[ ]` | CAP & PACELC | What the theorem says, and what it does **not** say |
| `[ ]` | Async & queues | At-least-once, idempotency, dead-letter queues, backpressure |
| `[ ]` | Rate limiting | Token bucket, leaky bucket, distributed counters |
| `[ ]` | Consistent hashing | Virtual nodes, and why plain modulo breaks on resize |
| `[ ]` | Case studies | URL shortener, news feed, chat, rate limiter, object store |

Tick a box here when the note exists **and** you could explain it without it.

## Folder shape

```
systemdesign/
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
