# MESC Pilot-01 -- P01-03A Acquisition Authorization Request

Freeze date: 2026-07-17

## What this requests

This document requests a future founder decision on whether `P01-03B IMMUTABLE ARTIFACT ACQUISITION ONLY` may be authorized.

It does not record approval. It does not itself grant authority.

## Exact acquisition scope

Repository: `qiaojin/PubMedQA`
Configuration: `pqa_labeled`
Immutable revision: `9001f2853fb87cab8d220904e0de81ac6973b318`
Representation: `Parquet`
Target storage root: `C:\Users\Shehr\MedScaleData\mesc-pilot-01\raw\pubmedqa\`
Target revision-specific directory: `C:\Users\Shehr\MedScaleData\mesc-pilot-01\raw\pubmedqa\9001f2853fb87cab8d220904e0de81ac6973b318\pqa_labeled\`
Boundary: external to every Git worktree and repository
Cloud-sync exclusion: not under OneDrive or synchronized tree

## Explicitly excluded from this request

* dataset opening or Parquet schema inspection
* transformation or normalization
* annotation or label generation
* inference, retrieval, or baseline execution
* model or embedding-model download
* release, publication, production, or clinical use
* Afia integration
* arbitrary Python loading scripts
* `trust_remote_code`
* arbitrary code execution from remote sources
* full article text or PDF

## Proposed conditions

### One-run versus continuing authorization

Recommended boundary: `P01-03B` is a one-run acquisition event that produces immutable local artifacts and a manifest. Continuation into `P01-03C` or later stages requires a separate governance decision.

### Stop conditions

Founder authorization, if later granted, remains subject to these stop conditions:

* revision mismatch against `9001f2853fb87cab8d220904e0de81ac6973b318`
* unexpected file outside the verified artifact allowlist
* rights-metadata change detected before or during acquisition
* raw content would enter Git tracking or a synchronized directory
* `trust_remote_code` would be required
* loading mechanism would execute remote Python code
* storage path resolves inside a Git worktree, OneDrive-synchronized directory, or cloud-synced tree
* hash verification fails for any acquired file
* download produces partial or duplicate artifacts

Any stop condition aborts acquisition and returns control without authorizing later stages.

### Environment

Acquisition, if later authorized, must occur in a controlled local environment with:

* explicit path guard rejecting any path under a Git worktree
* explicit path guard rejecting any path under a synchronized cloud directory
* fail-closed behavior on ambiguity

## Governance note

This request is documentation only. It does not create, modify, or execute any acquisition procedure.
