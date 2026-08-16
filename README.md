# Plugin Contract Unification

> One contract for every capability. Stop writing a new adapter for every tool.

## The Problem

Functions, classes, APIs, tools, and agents usually come in different shapes.
They have different call signatures, lifecycle rules, error styles, and
configuration formats.

As a project grows, this turns into custom glue code:

- one loader for a tool
- one wrapper for an API
- one adapter for a model
- one special case for a service

Every new capability becomes another integration problem.

## The Atomic Idea

Wrap every capability behind the same contract:

```text
name + schema + lifecycle + handler
```

`handler` is the executable logic behind a capability.

Then one registry can load, invoke, replace, and unload all of them the same
way. This turns heterogeneous capabilities into replaceable plugins without
rewriting the surrounding system.

## Why Developers Care

- Fewer custom adapters.
- Hot-swappable capabilities.
- Consistent schema and error codes.
- Clear lifecycle: register, load, run, replace, unload.
- A conformance suite that validates the contract.
- A small, zero-dependency reference implementation.

Before:

```text
one adapter for each tool, API, model, and service
```

After:

```text
registry.register(plugin)
```

## Quick Start

Run the reference implementation self-tests:

```bash
python -B skill.py
```

Run the conformance suite:

```bash
python -B conformance.py
```

## What Is In This Repository

```text
SPEC.md          language-neutral contract
skill.py         reference implementation
conformance.py   conformance tests
SKILL.md         entry for AI coding assistants
```

## Vision

The goal is to make plugin-contract unification a small, neutral integration
standard:

```text
capability + contract + registry = replaceable system
```

It should not require developers to adopt a whole agent framework. It should
be small enough to drop into an existing project and strict enough to make
different capabilities behave the same way.

## Roadmap

Current:

- language-neutral contract
- single-file reference implementation
- conformance suite

Next:

- more examples for common integration patterns
- CI badges and reproducible conformance results
- additional language bindings
- contribution and compatibility guidelines

Later:

- production runtime with timeout, isolation, and monitoring
- hosted registry and governance services
- private industry-specific plugin systems built on the same contract

## Production Directions

The same contract can be used to build:

- AI coding assistant skill systems
- enterprise tool and agent buses
- private industry-specific plugin systems
- plugin registry services with governance and auditing

Production versions may remain private or use separate licensing. This
repository only provides the contract, reference implementation, and
conformance suite.

## Non-Goals

- Not a full agent framework.
- Not a production or flagship product.
- Not a clone of any specific framework.
- Not an official product of any upstream project.

## License

This public implementation is distributed under GPLv3.

See `LICENSE`, `COPYING`, and `NOTICE`.

Chinese version: [README.zh-CN.md](README.zh-CN.md)
