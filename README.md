# Plugin Contract Unification

> A self-contained atomic skill egg that solves the heterogeneous-component coupling problem.

## What This Is

An atomic skill inspired by the public DeepSeek Harness design. It forces every
component to follow one lifecycle contract, input/output schema, and error
propagation model. Functions, classes, and APIs can be loaded, replaced, and
invoked through a single registry.

- Breakthrough pattern: `form-shift`
- Core principle: `interpose`

## Run

Zero dependencies:

```bash
python skill.py
```

The script runs 10 self-tests and exits successfully when all pass.

Claude Code and Codex can load this skill through `SKILL.md`.

## Input To Output

```text
raw capability definition (function / class / API)
  -> standardized plugin descriptor and runtime handle
```

## Use Cases

Suitable for:

- hot-swappable plugin frameworks
- unified orchestration of heterogeneous capabilities
- plugin-based agent runtimes

Not suitable for:

- fixed single-capability systems
- extreme performance paths that cannot tolerate an intermediary layer

## License

This public egg is distributed under GPLv3. It is inspired by the public MIT
design of DeepSeek Harness and is not affiliated with DeepSeek.

See `LICENSE`, `COPYING`, and `NOTICE`.

Chinese version: [README.zh-CN.md](README.zh-CN.md)
