# M4 — ModelKit Backends

Implemented under `src/medscale/backends/`, remaining fully optional.

## Components

- `src/medscale/backends/common.py`: shared backend contracts and errors.
- `src/medscale/backends/transformers/`: optional transformers backend.
- `src/medscale/backends/llamacpp/`: optional llama.cpp backend.

## Optional dependencies

```bash
pip install medscale[backends-transformers]
pip install medscale[backends-llamacpp]
```

Core install keeps no transitive ML dependencies.

## Known limitations

- Core install does not install transformer model dependencies.
- llama.cpp runtime requires platform-appropriate binary wheels.
- Deterministic configuration verified in tests; full remote-model generation is out of scope for M4.

## Verification

```bash
uv run ruff check .
uv run mypy src tests
uv run pytest tests/test_modelkit_backends.py
```
