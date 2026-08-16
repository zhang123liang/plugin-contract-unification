---
name: plugin-contract-unification
description: Use when designing or refactoring a plugin-based agent runtime, integrating heterogeneous functions/classes/APIs into one registry, or adding hot-swappable capability loading with lifecycle and schema enforcement.
---

# Plugin Contract Unification

## Purpose

Wrap heterogeneous capabilities as standard plugins, then load, invoke, replace, and unload them through one registry.

## When To Use

- The system must combine functions, classes, APIs, tools, or agents behind one interface.
- Components need hot replacement without stopping the host.
- The agent must reject malformed capabilities before they enter the runtime.

## Run

```bash
python skill.py
```

## Interfaces

```python
from skill import Plugin, Registry, detect, verify

registry = Registry()
registry.register(Plugin("double", {"input": "int", "output": "int"}, lambda x: x * 2))
registry.invoke("double", 4)
```

Use `detect(project_desc)` for skill matching.

Use `verify(claim, evidence)` to confirm whether a claim belongs to this plugin-contract domain.

## Boundaries

Do not use this skill as a complete agent runtime. It is the minimal atomic contract for plugin lifecycle, registry, and error propagation.

## Source And License

This project is not affiliated with DeepSeek; it is only inspired by DeepSeek Harness's public MIT design.
This skill implementation is distributed under GPLv3.
See `NOTICE` and `LICENSE`.
