# P01-05 B0 Execution Evidence Manifest

Status: **EXTERNAL EVIDENCE PRESERVED / IDENTITIES CANONICALIZED**

The repository records identity and verification metadata only. The external
bundle remains the byte-preserved execution evidence.

## External bundle

| artifact | byte size | SHA-256 |
|---|---:|---|
| `mesc-p01-05-b0-real-zero-shot-validation-1-evidence.zip` | 22957 | `3502ba1b2ddaf006d2465db01ef9722b0da171a6eeb667837110d93c44a40aa1` |
| `mesc-p01-05-b0-real-zero-shot-validation-1.json` | 78921 | `eaeb58c077f8666c3999855bd74e09303d538f1d37353df62cf236abcf483053` |
| `mesc-b0-remote-model-acquisition.provenance.json` | 3038 | `5fce67db08e829bceefda389552055366f9d996085e55b171304279be54c5d42` |
| `mesc-p01-05-b0-real-zero-shot-validation-1.closeout.json` | 2091 | `30822b9aa21f6a2106788c5c3f109f6f44a51cc3c958992d066364da31eefae7` |

The ZIP contains exactly the three listed inner artifacts and no model weights.

## Scientific execution identity

```text
canonical code commit:
5e073db72149266a4e14993cc2501ea2e0e163f5

canonical code tree:
07443a6b9cc0845c5e83de6a80012e6fcfacba47

model:
meta-llama/Llama-3.2-3B-Instruct

model revision:
0cb88a4f764b7a12671c53f0838cd831a0843b95

tokenizer revision:
0cb88a4f764b7a12671c53f0838cd831a0843b95

input size:
262968

input SHA-256:
0cb55ad4de0eb831e2475030e889ad9a6f0701ea59adbdd6a30cc0d0115be8d3

run id:
mesc-b0-run-66797ef270714a482bc1346513e9c61b98a7ffa5880b12bfb79834b1baeb6ae9

run digest:
66797ef270714a482bc1346513e9c61b98a7ffa5880b12bfb79834b1baeb6ae9
```

## Runtime manifest observed in the preserved report

```text
environment:          GOOGLE_COLAB_HOSTED_RUNTIME
GPU:                  Tesla T4
Python:               3.12.13
medscale:             0.2.0
transformers:         5.12.1
torch:                2.11.0+cu128
tokenizers:           0.22.2
huggingface-hub:      1.21.0
safetensors:          0.8.0
device:               cuda
dtype:                float16
quantization:         none
seed:                 0
prompt template:      mesc-b0-prompt/1
evidence condition:   none
```

## Determinism probe identities

```text
example id:
mesc-pilot-01:fc0fec260202f8a320dfec307968931fd499f62c530bf7939139d439b7990a57

row ordinal:
12

raw prompt SHA-256:
47243bf47a9a68ac0e6da81b09613c1c0786821165940d21c1caf14a69bc6410

canonical prompt SHA-256:
9e9a6948e4eb7cdc60a4a2a85cc396cd70daf9cf7e9d536179b4d3367861471b

raw output SHA-256:
c42b4f18b1de03ed609d436e8a62d31ec9e5618e7f56666b41c8e90054f0f080

canonical output SHA-256:
e15bc325568233f15273344d4b5f6a13412a3c3d0ce157f042bf32a76bc3b1a9

reexecution attestation:
PASS
```

## Artifact-integrity verification

The preserved report was checked after leaving the Colab execution environment:

- report SHA-256 matched the execution-recorded identity
- readiness-provenance SHA-256 matched
- closeout SHA-256 matched
- canonical run digest was recomputed from the report's canonical payload and
  exactly matched `66797ef270714a482bc1346513e9c61b98a7ffa5880b12bfb79834b1baeb6ae9`
- 150 prediction example IDs were unique
- 150 row ordinals were unique
- verbose predictions matched their canonical counterparts
- raw-output canonical hashes recomputed successfully
- aggregate counts and predicted distribution recomputed consistently

This verification establishes artifact integrity and internal consistency. It is
not an independent inference rerun and does not establish cross-hardware numerical
reproducibility.
