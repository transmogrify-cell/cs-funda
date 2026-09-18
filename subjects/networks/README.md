# MOD-04 · Computer Networks

> How two machines that have never met agree on anything.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/divider-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="../../assets/divider-light.svg">
  <img alt="" src="../../assets/divider-light.svg" width="100%">
</picture>

## Topics

| Done | Topic | What to actually understand |
|:--:|---|---|
| `[ ]` | Layering | OSI vs TCP/IP, encapsulation, where each header goes |
| `[ ]` | Link layer | Ethernet frames, MAC, ARP, switching |
| `[ ]` | Network layer | IPv4/IPv6, subnetting, NAT, routing tables, BGP sketch |
| `[ ]` | Transport | TCP handshake & teardown, sliding window, UDP's use cases |
| `[ ]` | Congestion control | AIMD, slow start, Reno vs CUBIC vs BBR |
| `[ ]` | DNS | Recursive vs iterative, TTL, records, anycast |
| `[ ]` | HTTP & TLS | 1.1 vs 2 vs 3, keep-alive, handshake, certificates |
| `[ ]` | Sockets | The actual syscall sequence, blocking vs non-blocking, `epoll` |

Tick a box here when the note exists **and** you could explain it without it.

## Folder shape

```
networks/
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
