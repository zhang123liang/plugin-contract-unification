# Plugin Contract Unification Specification

Version: 1.0

This document defines a minimal, language-neutral contract for wrapping
heterogeneous capabilities as plugins and managing them through a registry.

## 1. Purpose

The contract allows functions, classes, APIs, tools, and agents to be loaded,
invoked, replaced, and unloaded through one interface.

## 2. Definitions

- Capability: a function, class, API, tool, or agent that performs work.
- Plugin: a wrapper that gives a capability a uniform descriptor and lifecycle.
- Registry: a runtime collection that validates, stores, and invokes plugins.
- Descriptor: metadata describing a plugin, including name, schema, version,
  handler, and optional metadata.

## 3. Plugin Requirements

Every plugin must provide:

1. `name`: a non-empty string.
2. `schema`: a dictionary with at least `input` and `output`.
3. `handler`: a callable that executes the capability.
4. Optional `version`: a version string.
5. Optional `metadata`: a dictionary of additional machine-readable data.

## 4. Lifecycle

Minimal lifecycle states:

```text
unregistered
  -> registered
  -> loaded
  -> active
  -> unloaded
```

Rules:

- A plugin must be registered before it can be invoked.
- A plugin must be loaded before it can run.
- Replacing a registered plugin unloads the old version and loads the new
  version.
- Unregistering a plugin unloads it and removes it from the registry.

## 5. Registry Operations

The registry must support:

- register
- replace
- unregister
- invoke
- get
- list

## 6. Error Contract

Errors should include a stable code and, when applicable, the plugin name.

Required codes:

- `INVALID_NAME`
- `INVALID_SCHEMA`
- `INVALID_PLUGIN`
- `DUPLICATE_PLUGIN`
- `NOT_LOADED`
- `NOT_FOUND`
- `CONTRACT_ERROR`

## 7. Detection Interface

`detect(project_desc)` must return:

```json
{
  "score": 0,
  "matched": [],
  "evidence": ""
}
```

The score is the number of matched signature terms.

## 8. Verification Interface

`verify(claim, evidence)` must return:

```json
{
  "verdict": "confirmed",
  "matched": [],
  "reasoning": "",
  "evidence_strength": "moderate"
}
```

Allowed verdicts:

- `confirmed`
- `refuted`
- `unknown`
- `mismatched`

## 9. Conformance

An implementation is conformant when it passes the tests in `conformance.py`.

## 10. License

This specification is intentionally separate from the reference
implementation. It may be implemented under other licenses. The reference
implementation in this repository is GPLv3.
