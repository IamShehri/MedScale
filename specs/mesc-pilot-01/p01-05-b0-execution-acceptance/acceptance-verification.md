# P01-05 B0 Real-Execution Acceptance Verification

Status: **PASS**

This record verifies the bounded B0 validation execution against the controlling
P01-05 deterministic discipline and the separately issued founder authorization.

## Bound identities

```text
code commit:
5e073db72149266a4e14993cc2501ea2e0e163f5

code tree:
07443a6b9cc0845c5e83de6a80012e6fcfacba47

validation input:
size   262968
sha256 0cb55ad4de0eb831e2475030e889ad9a6f0701ea59adbdd6a30cc0d0115be8d3

model:
meta-llama/Llama-3.2-3B-Instruct

revision:
0cb88a4f764b7a12671c53f0838cd831a0843b95

run digest:
66797ef270714a482bc1346513e9c61b98a7ffa5880b12bfb79834b1baeb6ae9

report:
size   78921
sha256 eaeb58c077f8666c3999855bd74e09303d538f1d37353df62cf236abcf483053

external evidence bundle:
size   22957
sha256 3502ba1b2ddaf006d2465db01ef9722b0da171a6eeb667837110d93c44a40aa1
```

## Gate sequence

```text
remote GPU attestation:                         PASS
validation-input remote attestation:            PASS
gated model access:                             PASS
immutable revision attestation:                 PASS
exact model acquisition:                        PASS
model-byte provenance:                          PASS
canonical code/blob attestation:                PASS
runtime dependency attestation:                 PASS
canonical Python import attestation:            PASS
model device/dtype attestation:                  PASS
single-example execution probe:                 PASS
full 150-example execution returned:             PASS
full-result structural attestation:             PASS
deterministic probe reconciliation:              PASS
canonical report write:                          PASS
external evidence preservation:                  PASS
post-runtime artifact-integrity verification:    PASS
```

## Hash-domain reconciliation event

The full 150-example inference completed before the first report-publication
attempt. A post-run guard then stopped because the probe anchor had been recorded
as SHA-256 over raw UTF-8 bytes while canonical `run_b0` stores
`sha256_hexdigest(value)`, which hashes canonical JSON bytes.

Disposition:

```text
scientific inference rerun:       NO
configuration change:             NO
prompt change:                    NO
model/revision change:            NO
additional inference in repair:   NO
```

The existing in-memory completed report was retained. Raw-byte and canonical-JSON
hash domains were then verified independently:

```text
probe raw prompt:
47243bf47a9a68ac0e6da81b09613c1c0786821165940d21c1caf14a69bc6410

probe canonical prompt:
9e9a6948e4eb7cdc60a4a2a85cc396cd70daf9cf7e9d536179b4d3367861471b

probe raw output:
c42b4f18b1de03ed609d436e8a62d31ec9e5618e7f56666b41c8e90054f0f080

probe canonical output:
e15bc325568233f15273344d4b5f6a13412a3c3d0ce157f042bf32a76bc3b1a9
```

All four reconciled. The report was then published without rerunning the 150
examples.

## Scientific result

```text
TOTAL=150
PARSED_COUNT=150
UNPARSEABLE_COUNT=0
AMBIGUOUS_COUNT=0
GENERATION_FAILED_COUNT=0
CORRECT_COUNT=104
ACCURACY=0.6933333333333334
COVERAGE=1.0
PREDICTED_DISTRIBUTION={"maybe":1,"no":47,"yes":102}
GOLD_DISTRIBUTION={"maybe":17,"no":50,"yes":83}
```

## Boundary verification

```text
test scientific content accessed: NO
training:                         NOT PERFORMED
retrieval:                        NOT PERFORMED
fallback model:                   NOT USED
quantization:                     NONE
Google Drive mount:               NOT PERFORMED
repository mutation during run:   NONE
```

## Acceptance disposition

```text
P01-05 B0 REAL ZERO-SHOT VALIDATION EXECUTION:
COMPLETE / ACCEPTED

artifact integrity:
VERIFIED

independent model replication:
NOT PERFORMED

B1 execution:
NOT AUTHORIZED

test execution:
NOT AUTHORIZED

P01-06:
NOT AUTHORIZED
```
