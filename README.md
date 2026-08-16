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

## Potential Applications

This atomic skill can be reused as a lightweight control plane for:

- Claude Code / Codex skill and tool loaders
- DeepSeek Harness compatible plugin registries
- MCP server and API adapter routing
- hot-swappable model providers
- sandbox and permission lifecycle management
- multi-agent capability orchestration
- enterprise tool buses that unify internal APIs
- private vertical skill packages that implement the same contract

## Recommended First Applications

| Priority | Application | Reason |
|---|---|---|
| 1 | Claude Code / Codex skill runtime | Validate the contract in real agent hosts |
| 2 | Public plugin registry reference | Establish a neutral integration standard |
| 3 | Tool/API adapter bus | Reuse the same lifecycle for MCP and internal APIs |
| 4 | Private vertical eggs | Keep proprietary skills compatible without exposing them |

## Validation Status

- Local `python -B skill.py` self-tests pass.
- Claude Code and Codex loading is being validated separately.
- The public release is intended as a reference contract, not as a complete agent runtime.

## License

This public egg is distributed under GPLv3. It is inspired by the public MIT
design of DeepSeek Harness and is not affiliated with DeepSeek.

See `LICENSE`, `COPYING`, and `NOTICE`.

Chinese version: [README.zh-CN.md](README.zh-CN.md)
