# OpenSandbox Adoption Review for MESC

Date: 2026-08-18
Status: STRATEGIC DONOR REVIEW — NO RUNTIME ADOPTION AUTHORIZED

## Source

Repository: `opensandbox-group/OpenSandbox`

Reviewed live upstream state:

- default branch: `main`
- recent reviewed head: `96175e2836ab8d44cc8bc6fb3c258b3d10ec3642`
- license: Apache-2.0
- scope: general-purpose sandbox platform for AI applications
- runtimes: Docker and Kubernetes
- secure-runtime options include gVisor, Kata Containers, and Firecracker-backed Kata
- release artifacts support signed provenance/attestation workflows

## Decision

Classification: `HIGH_VALUE_EXECUTION_AND_SECURITY_DONOR`

OpenSandbox is accepted as a **high-priority candidate provider/reference** for future MESC isolated execution, tool sandboxes, evaluation trials, training/evaluation jobs, and MCRL-controlled external execution.

It is not yet approved as a direct production dependency.

This review does not authorize:

- OpenSandbox installation in canonical MESC infrastructure;
- execution against real clinical systems;
- PHI processing;
- MCRL implementation;
- retrieval activation;
- model training;
- changes to Pilot-01;
- P01-06 or later stages.

Any runtime adoption requires a separate security, dependency, provenance, and operational admission gate.

## Why it matters

OpenSandbox provides several capabilities that MESC would otherwise need to design and operate independently:

- sandbox lifecycle API;
- command/file/code-execution APIs;
- Docker and Kubernetes backends;
- strong-isolation runtime support;
- resource limits and GPU-aware scheduling;
- network egress policy;
- credential injection without exposing real credentials to sandbox workloads;
- signed image/package provenance;
- MCP integration;
- one-sandbox-per-trial evaluation patterns;
- snapshots, pause/resume, and persistent/shared volume patterns.

## Recommended MESC position

MESC should define its own sandbox/provider interface and allow OpenSandbox to be one provider behind that seam.

```text
MCRL Clinical Tool Pipeline
        │
        ▼
MESC Sandbox Service Definition
        │
        ├── OpenSandbox provider
        ├── local restricted provider
        └── future provider(s)
```

MCRL must remain independent of OpenSandbox-specific APIs.

## High-value patterns to adopt

### 1. Strong isolation as a selectable provider capability

OpenSandbox supports standard containers and stronger isolation through gVisor/Kata/Firecracker configurations.

MESC should require a declared isolation level per workload class, rather than assuming all sandboxes are equivalent.

Example future MESC policy classes:

- `RESEARCH_FIXTURE` — bounded local/container execution;
- `UNTRUSTED_GENERATED_CODE` — gVisor or stronger;
- `HIGH_RISK_TOOL_EXECUTION` — VM/microVM isolation where required;
- `MODEL_EVALUATION_TRIAL` — isolated ephemeral environment with network default-deny;
- `CLINICAL_SYSTEM_ADAPTER_TEST` — synthetic-only, tightly scoped credentials and egress.

No production clinical deployment policy is authorized by this document.

### 2. Default-deny egress

OpenSandbox provides per-sandbox outbound network policy and recommends default-deny for credential-proxy use.

MESC should make `default deny` the normal security posture for tool/evaluation sandboxes, then explicitly allow required destinations.

Network policy should be bound to the MCRL objective/tool scope and included in execution provenance.

### 3. Credential vault / broker pattern

OpenSandbox's Credential Vault keeps real credentials outside the sandbox workload and injects them at the egress sidecar for narrowly matched outbound HTTPS requests.

MESC should adopt this architectural principle:

> untrusted model/tool workloads should receive no reusable real credential whenever a trusted broker can inject the credential at a narrower enforcement boundary.

Future MESC requirements should include:

- exact host/path/method scope;
- default-deny egress;
- no secret values in model-visible context;
- no secrets in sandbox filesystem or logs;
- redaction;
- short-lived/revocable credentials where possible;
- provenance event for credential-binding identity without secret content.

### 4. Signed release and image provenance

OpenSandbox publishes workflows for verifying source archives, container images, packages, and Helm charts with checksums, GitHub attestations, Sigstore/cosign, and workflow identities.

MESC should mirror this supply-chain discipline for:

- model-serving images;
- MCRL runtime images;
- AMGE/audio workers;
- evaluation images;
- public Python/CLI packages;
- Hugging Face artifacts where applicable.

Pin by immutable digest where the deployment platform supports it.

### 5. Runtime-neutral public contracts

OpenSandbox separates lifecycle/API contracts from Docker/Kubernetes implementations.

MESC should similarly separate:

- clinical/tool execution request contract;
- sandbox lifecycle provider;
- runtime backend;
- network policy provider;
- credential broker;
- evidence/result persistence.

### 6. One-sandbox-per-evaluation-trial

OpenSandbox explicitly supports agent evaluation and examples where trials run in separate sandboxes.

MESC-Eval should consider isolated trial execution for tasks involving tools, code, FHIR fixtures, browser/document workflows, or adversarial prompts so one trial cannot contaminate another.

### 7. Resource identity and limits

MESC provenance should capture sandbox image digest, runtime/provider identity, CPU/memory/GPU limits, network policy, and sandbox configuration for every scientific execution where those variables can affect reproducibility.

### 8. Pause/resume/snapshot as controlled research capability

Snapshots can be useful for reproducible long-running evaluation or agent workflows, but MESC must never assume secrets or credential-vault state survive snapshots safely. Trusted credential state remains outside the sandbox.

## Security observations requiring a later audit

### Upstream is evolving quickly

The repository is actively changing. Recent changes include PID-1/init handling, seccomp/capability hardening, Landlock confinement, and optional eBPF observation. MESC must pin an exact admitted release or commit rather than track mutable `main`.

### Secure runtime is not the same as complete policy

Choosing gVisor/Kata/Firecracker does not replace application-level controls for egress, credentials, filesystem scope, resource limits, or tool authorization.

### Some hardening layers can degrade/operate conditionally

Recent upstream implementation notes describe capability reporting for active/unsupported/degraded/disabled hardening layers and include cases where layers may degrade depending on platform/support. A future MESC admission gate must define which security layers are mandatory and fail closed if they are not active.

### Credential Vault has deployment constraints

Current upstream documentation requires `dns+nft` enforcement for Credential Vault and warns that DNS-only mode is insufficient because direct-IP connections can bypass DNS policy. It also documents incompatibility with an additional transparent service-mesh sidecar in the same namespace.

MESC must prove the actual deployment topology rather than merely enable a flag.

## Proposed MESC execution architecture

```text
MCRL Objective + Tool Policy
        │
        ▼
ClinicalToolPipeline
        │
        ├── identity/scope admission
        ├── monotonic safety guards
        ├── approval where required
        └── sandbox request
                 │
                 ▼
        MESC Sandbox Provider Seam
                 │
                 ├── OpenSandbox
                 │      ├── Docker/Kubernetes
                 │      ├── gVisor/Kata/Firecracker
                 │      ├── default-deny egress
                 │      └── credential broker
                 │
                 └── alternate provider
        │
        ▼
Immutable tool result + provenance event
        │
        ▼
MESC Verifier
```

## Relationship to DeepSeek Harness

The two donors solve complementary problems:

- DeepSeek Harness → event-sourced agent/tool orchestration and guarded tool pipeline architecture;
- OpenSandbox → execution isolation, runtime lifecycle, egress, credentials, and workload infrastructure.

A strong future MESC design can combine the **patterns** without coupling to either implementation:

```text
MCRL / Harness-style control plane
                +
OpenSandbox-style isolated execution plane
```

## Recommendation

Priority: `HIGH`

Potential direct provider use: `PROMISING, REQUIRES SEPARATE ADMISSION`

Architectural donor use: `RECOMMENDED`

Pilot-01 use: `NOT AUTHORIZED`

PHI/real clinical-system use: `NOT AUTHORIZED`

Next safe action after Pilot-01: create a MESC Sandbox Provider specification and a security-admission matrix comparing OpenSandbox with local/container, gVisor, Kata/Firecracker, and any other serious providers before implementation.