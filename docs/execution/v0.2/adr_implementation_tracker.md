# ADR Implementation Tracker

## M4 Relevant ADRs
- ADR-0012: layered architecture model (`backends` placed at modelkit layer 2).
- ADR-0020: public API stability (`BackendMissingDependencyError` preserved).
- ADR-0021: extension architecture (`backends` implemented as optional extension, not core dependency).

## Implementation notes
- Added `backends` to architecture layer classification in `tests/test_architecture.py`.
- Kept dependency direction core: `backends` may depend on `modelkit`, but not `dataset`, `research`, or `cli`.
- Deterministic contract: `GenerationConfig` carries `backend_name`, `seed`, `do_sample`, `temperature`.
