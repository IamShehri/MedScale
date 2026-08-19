# Apertus 1.5 Public AUP Binding Method

Status: **PRE-EXECUTION METHOD FREEZE / NO MODEL ACCESS**

Date: 2026-08-20

## Objective

Resolve `BT-RDY-BLK-APERTUS-AUP-001` without requesting or accepting gated model access and without touching model weights.

## Authoritative identity source

The legal artifact must be resolved from the public repository:

```text
repository = swiss-ai/apertus-legal
path = apertus_1.5/USAGE_POLICY.pdf
```

Before any interpretation, record from the authoritative repository:

- Git blob SHA;
- byte size;
- repository default branch or immutable commit used for retrieval.

## Binary retrieval

Retrieve the PDF only from an authoritative public GitHub repository/raw-content endpoint or an equivalent first-party public endpoint that does not require gated model access or agreement acceptance.

The retrieved file is a legal-document artifact, not a model-weight artifact.

## Mechanical binding

For retrieved bytes `B`:

1. record `len(B)`;
2. compute `SHA256(B)`;
3. compute Git blob SHA-1 as `SHA1("blob " + decimal(len(B)) + NUL + B)`;
4. require computed Git blob SHA-1 to equal the authoritative repository blob SHA exactly;
5. require retrieved byte length to equal the authoritative repository size exactly.

If either comparison fails, stop with `BLOCKED` and do not interpret the PDF.

## Readability verification

After successful byte binding:

1. inspect PDF metadata/structure;
2. render every page to images using a deterministic local PDF renderer;
3. inspect rendered pages for missing/clipped/garbled content;
4. extract text with a local PDF text extractor where available;
5. compare extracted text against rendered pages sufficiently to ensure material clauses were not silently omitted;
6. use OCR only if the PDF lacks usable text and only as a last resort;
7. do not substitute an older/newer policy, search snippet, third-party mirror, or model-generated reconstruction.

## Legal-evidence output

Record, with page/section references where possible:

- permitted use scope;
- prohibited use categories;
- downstream/user obligations;
- legal/compliance responsibilities;
- redistribution/derivative/commercial-use implications relevant to Program Rule R3;
- any healthcare/medical restrictions relevant to the bounded synthetic research tournament;
- privacy/data-controller obligations relevant to Program Rule R2;
- any ambiguity that prevents deterministic compatibility disposition.

## Disposition rule

```text
exact verified terms compatible + all other evidence proven
=> continue normal admission analysis

exact verified terms conclusively incompatible
=> NOT_ADMITTED

any unresolved, unreadable, contradictory, or unbindable material term
=> BLOCKED
```

## Prohibited shortcuts

Do not:

- accept the Hugging Face gate;
- request gated model access;
- access model repository weights/files behind the gate;
- infer exact 1.5 terms from Apertus 1.0 terms;
- use a third-party legal summary as authoritative evidence;
- weaken `BLOCKED` to `NOT_ADMITTED` merely to unblock the roster.
