"""Dataset package init.

Stability: public. Re-exports the versioned dataset API.
"""

from __future__ import annotations

from medscale.dataset.compat import deterministic_hash_split
from medscale.dataset.manifest import (
    DatasetManifest,
    compute_dataset_manifest,
    write_manifest,
)
from medscale.dataset.split import (
    DeterministicSplitter,
    SplitStrategy,
    split_literature_records,
)
from medscale.dataset.validate import (
    DatasetValidationReport,
    validate_dataset,
)
from medscale.dataset.schema import (
    BENCHMARK_ITEM_SCHEMA,
    EVIDENCE_OBJECT_SCHEMA,
    LITERATURE_RECORD_SCHEMA,
    DatasetSchema,
)

__all__ = [
    "BENCHMARK_ITEM_SCHEMA",
    "DatasetManifest",
    "DatasetSchema",
    "DatasetValidationReport",
    "EVIDENCE_OBJECT_SCHEMA",
    "LITERATURE_RECORD_SCHEMA",
    "SplitStrategy",
    "compute_dataset_manifest",
    "deterministic_hash_split",
    "split_literature_records",
    "validate_dataset",
    "write_manifest",
]
