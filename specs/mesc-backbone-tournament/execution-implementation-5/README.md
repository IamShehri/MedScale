# Backbone Tournament execution implementation 5 — fixture activation identity verifier

Status: **DRAFT / FIXTURE-ONLY / NO EXECUTION AUTHORITY**

This slice is based directly on canonical `main`:

```text
BASE_MAIN_SHA = ab4d64f8708f649d33e494a4bed0272a2a526d9c
BASE_MAIN_TREE = 8fb0ccb9377a97b024e674b99f4d5ff89e34099e
FD-MESC-BT-EXEC-1 = CONDITIONAL_AUTHORIZATION_CANONICAL
EXECUTION_ACTIVATION = REQUIRED
```

## Scope

This implementation covers only pure, deterministic validation of the Section I/J
`RUNTIME_BINDING` and `identity_preimage` serialization contracts using synthetic
in-memory bytes and injected independently-recomputed fixture values.

The verifier:

- rejects duplicate JSON members before mapping construction;
- requires canonical ASCII JSON bytes with lexically sorted keys, exact compact
  separators, no BOM, and no trailing newline;
- requires the exact closed `RUNTIME_BINDING` key set and scalar/array types;
- enforces exact `RunPod Secure Cloud`, one-GPU, sequential execution, and
  `NVIDIA H100 80GB HBM3` identity values without contacting a provider;
- validates non-empty runtime identity strings using the authorization's printable
  ASCII restrictions;
- requires unique, byte-sorted acceleration runtime identities;
- validates exact OCI digest, dependency-lock digest, checkout SHA/tree, numeric
  descriptor identities, and canonical checkout-root path grammar;
- recomputes `runtime_binding_sha256` over the accepted exact bytes;
- requires the exact closed `identity_preimage` scalar schema;
- validates the fixed activation decision and receipt-version identifiers;
- compares every externally bound activation value against an injected
  `IndependentActivationBindings` fixture object;
- requires the runtime checkout SHA/tree to equal independently supplied fixture
  values;
- derives `ACTIVATION_ID` as lowercase SHA-256 over the exact canonical
  `identity_preimage` bytes;
- derives the external and repository result-root strings deterministically from
  that activation ID.

## Deliberate non-claims

This is not the activation executor and does not authenticate or retrieve any
GitHub commit, tree, Founder comment, gated-access attestation, telemetry
qualification, Phi manifest, sandbox qualification, or executor allowlist.

`IndependentActivationBindings` represents values that a future activation
verifier must independently recompute through separately reviewed mechanisms.
This fixture primitive only proves that canonical activation bytes bind exactly
to those injected values.

This slice does not:

- perform the Section I.1 descriptor-relative filesystem bootstrap;
- call `openat2`, `mkdirat`, NVML, RunPod, Docker, or subprocesses;
- allocate an H100 or prove a live GPU/provider instance;
- create activation directories or artifacts;
- access/download/load model weights;
- request or accept gated model access;
- read frozen Repair-2 prompt/corpus/scoring-key contents;
- serialize prompts to a model;
- run inference, generation, ranking, winner selection, or training.

The race-safe filesystem bootstrap, exact-instance telemetry qualification,
Git/comment authentication, remote-code controls, gated-access authority, final
activation receipt, and production executor integration remain separate,
independently reviewed work.

## Local fixture qualification before push

```text
py_compile = PASS
fixture tests = 49 passed
```

Only standard-library code and synthetic in-memory fixture values were used.

## Hard boundary

```text
EXECUTION_ACTIVATION = REQUIRED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
GATED_ACCESS_REQUEST_OR_ACCEPTANCE = NOT_AUTHORIZED
MODEL_RETRIEVAL = NOT_AUTHORIZED
PROMPT_SERIALIZATION_TO_MODEL = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
GENERATION = NOT_AUTHORIZED
RANKING = NOT_AUTHORIZED
WINNER_SELECTION = NOT_AUTHORIZED
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
```

Keep this work Draft until exact-head CI, CodeQL, scope reconciliation, and an
independently permitted review are all proven. Any head mutation burns prior
head-specific evidence.
