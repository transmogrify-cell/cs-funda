# MOD-05 · OOP & Design Patterns

> Structuring code so it survives the second person who reads it.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/divider-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="../../assets/divider-light.svg">
  <img alt="" src="../../assets/divider-light.svg" width="100%">
</picture>

## Topics

| Done | Topic | What to actually understand |
|:--:|---|---|
| `[ ]` | Encapsulation & abstraction | Invariants, why public fields leak them |
| `[ ]` | Inheritance & polymorphism | vtables, dynamic dispatch cost, composition first |
| `[ ]` | SOLID | Each principle with the bug it prevents |
| `[ ]` | Creational patterns | Factory, builder, singleton (and its costs) |
| `[ ]` | Structural patterns | Adapter, decorator, facade, proxy |
| `[ ]` | Behavioural patterns | Strategy, observer, state, command |
| `[ ]` | UML | Class & sequence diagrams that are worth drawing |

Tick a box here when the note exists **and** you could explain it without it.

## Folder shape

```
oop/
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
