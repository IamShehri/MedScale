"""Private fixture-only atomic publication and write-path protection (FD-BPUB-1..18).

This module publishes the six accepted byte surfaces of one exact
``FixtureSplitResult``, plus one non-circular publication manifest, into one
directory that becomes visible through exactly one same-parent atomic
no-replace directory rename.

Boundary, restated so it cannot be misread:

* private, unexported, library-only, fixture-only, synthetic-only, non-evidence;
* no CLI, no public API, no environment switch, no network, no subprocess, no
  clock and no randomness;
* it does not make ``SourceDocumentGroupedSplitter.assign`` executable;
* it creates no real split, no canonical dataset partition, no research
  artifact, no clinical artifact and no admissible evidence.

Publishing these bytes is a filesystem operation on synthetic material. It is
not promotion and it is not a scientific result.

Durability boundary (FD-BPUB-12): the only guarantee stated here is **atomic
namespace visibility** of the final directory. Universal power-loss durability,
storage-controller durability, filesystem-journal durability and directory-entry
durability across every supported platform are explicitly *not* claimed.

Atomic publication and write-path protection are one cohesive capability
(FD-BPUB-1). There is deliberately no writer-without-protection mode, no
protection-only mode, no manifest-only mode, no rename-only mode, no partial
publication mode, and no resume, repair or cleanup mode.
"""

from __future__ import annotations

import ctypes
import errno
import json
import os
import stat
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Final

from medscale.mesc._canonical_json_v1 import canonical_json_bytes, sha256_of_bytes
from medscale.mesc._fixture_split_v1 import FixtureSplitRequest, FixtureSplitResult
from medscale.mesc._split_artifacts_v1 import (
    verify_descriptor_against_bytes,
    verify_split_fingerprint_record,
)

# ---------------------------------------------------------------------------
# Frozen literals (FD-BPUB-5, FD-BPUB-6, FD-BPUB-7)
# ---------------------------------------------------------------------------

#: The publication manifest schema. This manifest is its own schema domain and is
#: deliberately unrelated to the accepted artifact schema-version table (FD-BPUB-7).
MANIFEST_SCHEMA_VERSION: Final = "mesc-pilot-01-fixture-publication-manifest/1"

#: The seventh file, always written last (FD-BPUB-11).
_MANIFEST_FILENAME: Final = "publication-manifest.json"

#: The mandatory ``-split-`` component is part of both literals (FD-BPUB-5).
_FINAL_DIRECTORY_PREFIX: Final = "mesc-p01-04b-split-"
_STAGING_DIRECTORY_PREFIX: Final = ".mesc-p01-04b-split-"
_STAGING_DIRECTORY_SUFFIX: Final = ".staging"

#: ``(filename, surface, result attribute)`` in ascending filename order.
#: This tuple is the single source of the six payload bindings (FD-BPUB-6) and of
#: the six ``surface`` identifiers (FD-BPUB-7).
_PAYLOAD_BINDINGS: Final[tuple[tuple[str, str, str], ...]] = (
    ("example-registry.jsonl", "example_registry", "example_registry_bytes"),
    ("excluded-ledger.json", "excluded_ledger", "excluded_ledger_bytes"),
    ("group-registry.jsonl", "group_registry", "group_registry_bytes"),
    ("leakage-audit.json", "leakage_audit", "audit_report_bytes"),
    (
        "split-summary-identity-core.json",
        "split_summary_identity_core",
        "split_summary_identity_core_bytes",
    ),
    ("split-summary.json", "split_summary_document", "split_summary_document_bytes"),
)

#: The exact seven-name inventory, ascending. Used for the receipt tuple and for
#: filesystem-derived inventory comparison (FD-BPUB-13, FD-BPUB-17).
_PUBLISHED_FILENAMES: Final[tuple[str, ...]] = tuple(
    sorted([binding[0] for binding in _PAYLOAD_BINDINGS] + [_MANIFEST_FILENAME])
)

#: The accepted fingerprint record describes exactly these four roles. The two
#: remaining surfaces carry no descriptor, and that absence is not a defect
#: (FD-BPUB-8). No descriptor is ever invented for them.
_DESCRIBED_ROLE_ATTRIBUTES: Final[Mapping[str, str]] = MappingProxyType(
    {
        "example_registry": "example_registry_bytes",
        "excluded_ledger": "excluded_ledger_bytes",
        "group_registry": "group_registry_bytes",
        "split_summary": "split_summary_identity_core_bytes",
    }
)

_HEX_DIGITS: Final = frozenset("0123456789abcdef")
_SHA256_LENGTH: Final = 64

#: ``pathlib.Path`` is abstract at construction: it yields the concrete flavour for
#: this platform. Comparing against that exact flavour rejects ``str``, ``bytes``,
#: ``PurePath`` and every caller subclass, which a bare ``isinstance`` would admit.
_CONCRETE_PATH_TYPE: Final = type(Path())

_O_BINARY: Final = getattr(os, "O_BINARY", 0)
_O_NOFOLLOW: Final = getattr(os, "O_NOFOLLOW", 0)
_FILE_ATTRIBUTE_REPARSE_POINT: Final = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)

# Atomic no-replace rename primitives (FD-BPUB-14).
_PRIMITIVE_WINDOWS_RENAME: Final = "windows-rename-no-replace"
_PRIMITIVE_LINUX_RENAMEAT2: Final = "linux-renameat2-noreplace"
_PRIMITIVE_MACOS_RENAMEX_NP: Final = "macos-renamex-np-excl"

_LINUX_RENAME_NOREPLACE: Final = 1
_MACOS_RENAME_EXCL: Final = 0x00000004
_AT_FDCWD: Final = -100

_UNSUPPORTED_ERRNOS: Final = frozenset(
    {
        errno.ENOSYS,
        errno.EINVAL,
        errno.ENOTSUP,
        getattr(errno, "EOPNOTSUPP", errno.ENOTSUP),
    }
)
_CONFLICT_ERRNOS: Final = frozenset({errno.EEXIST, errno.ENOTEMPTY})


# ---------------------------------------------------------------------------
# Typed error taxonomy (FD-BPUB-18) — class-based dispatch only, never messages
# ---------------------------------------------------------------------------


class _PublicationError(Exception):
    """Private base for every publication-boundary failure."""


class _InvalidPublicationInputError(_PublicationError):
    """Invalid input type, or a broken request/result identity binding."""


class _UnsafePublicationPathError(_PublicationError):
    """A publication parent or protected root that fails the write-path contract."""


class _PublicationTargetConflictError(_PublicationError):
    """The staging directory or the final directory already exists."""


class _UnsupportedAtomicRenameError(_PublicationError):
    """No atomic no-replace directory rename primitive is available here."""


class _StagingAcquisitionError(_PublicationError):
    """Exclusive creation of the staging directory failed."""


class _ExclusiveWriteError(_PublicationError):
    """Exclusive creation of, or writing to, one published file failed."""


class _ContentVerificationError(_PublicationError):
    """A written file did not read back as the exact planned bytes."""


class _InventoryVerificationError(_PublicationError):
    """The filesystem-derived staging inventory did not match the exact contract."""


class _FinalRenameError(_PublicationError):
    """The single atomic no-replace rename failed for a non-conflict reason."""


class _PostRenameVerificationError(_PublicationError):
    """Verification of the visible final directory failed after the rename."""


# ---------------------------------------------------------------------------
# Immutable value objects (FD-BPUB-8, FD-BPUB-17)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class _PlannedFile:
    """One planned file: its exact bytes, digest and size, fixed before mutation."""

    filename: str
    payload: bytes
    sha256: str
    byte_size: int


@dataclass(frozen=True, slots=True)
class _PublicationPlan:
    """The complete immutable plan. Nothing is computed after staging acquisition.

    ``final_directory`` and ``final_directory_name`` are FD-BPUB-5 vocabulary and
    belong to this internal plan only.  They are deliberately *not* receipt
    fields: FD-BPUB-17 fixes the receipt at exactly five names, where the visible
    directory is ``publication_directory``.
    """

    request_id: str
    split_fingerprint: str
    publication_parent: Path
    staging_directory: Path
    final_directory: Path
    final_directory_name: str
    payload_files: tuple[_PlannedFile, ...]
    manifest_file: _PlannedFile
    rename_primitive: str


@dataclass(frozen=True, slots=True)
class _PublicationReceipt:
    """The private runtime receipt (FD-BPUB-17).

    Never written to disk, never exported, never canonical evidence, never a
    research or clinical claim. Returning it does not promote the fixture result.
    """

    publication_directory: Path
    request_id: str
    split_fingerprint: str
    publication_manifest_sha256: str
    published_filenames: tuple[str, ...]


# ---------------------------------------------------------------------------
# Atomic no-replace rename primitive resolution (FD-BPUB-14)
# ---------------------------------------------------------------------------


def _load_posix_symbol(name: str) -> Any:
    """Return a libc symbol, or ``None`` when this runtime does not expose it."""
    try:
        library = ctypes.CDLL(None, use_errno=True)
    except (OSError, TypeError):  # pragma: no cover - platform dependent
        return None
    return getattr(library, name, None)


def _resolve_rename_primitive() -> str:
    """Select the atomic no-replace primitive, or fail closed.

    Resolution happens during planning, before staging is ever created, so an
    unsupported platform can never leave a half-published attempt behind.

    * Windows: ``os.rename`` is itself no-replace. The underlying rename is
      issued with ``ReplaceIfExists = FALSE``, so the existence test and the
      directory-entry creation are one kernel operation and cannot race.
    * Linux: ``renameat2`` with ``RENAME_NOREPLACE``.
    * macOS: ``renamex_np`` with ``RENAME_EXCL``.

    Every other platform raises, because a plain POSIX ``rename`` silently
    replaces an existing empty destination directory and therefore does not
    provide the required semantics.
    """
    if os.name == "nt":
        return _PRIMITIVE_WINDOWS_RENAME
    if sys.platform.startswith("linux"):
        if _load_posix_symbol("renameat2") is not None:
            return _PRIMITIVE_LINUX_RENAMEAT2
    elif sys.platform == "darwin":
        if _load_posix_symbol("renamex_np") is not None:
            return _PRIMITIVE_MACOS_RENAMEX_NP
    raise _UnsupportedAtomicRenameError(
        f"no atomic no-replace directory rename primitive is available on {sys.platform!r}"
    )


def _raise_for_rename_errno(code: int) -> None:
    """Map a failed primitive call to its exact typed category."""
    if code in _CONFLICT_ERRNOS:
        raise _PublicationTargetConflictError(f"the final directory already exists (errno {code})")
    if code in _UNSUPPORTED_ERRNOS:
        raise _UnsupportedAtomicRenameError(
            f"the atomic no-replace rename primitive is unsupported here (errno {code})"
        )
    raise _FinalRenameError(f"the atomic no-replace rename failed (errno {code})")


def _atomic_no_replace_rename(source: Path, destination: Path, primitive: str) -> None:
    """Perform exactly one same-parent atomic no-replace directory rename.

    The replace-existing rename variant is never called, no destination precheck
    stands in for the no-replace guarantee, and there is no copy, cross-device or
    recursive-move fallback.
    """
    if primitive == _PRIMITIVE_WINDOWS_RENAME:
        try:
            source.rename(destination)
        except FileExistsError as error:
            raise _PublicationTargetConflictError("the final directory already exists") from error
        except OSError as error:
            raise _FinalRenameError("the atomic no-replace rename failed") from error
        return

    if primitive == _PRIMITIVE_LINUX_RENAMEAT2:
        function = _load_posix_symbol("renameat2")
        if function is None:  # pragma: no cover - resolved during planning
            raise _UnsupportedAtomicRenameError("renameat2 is unavailable")
        function.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        ]
        function.restype = ctypes.c_int
        ctypes.set_errno(0)
        status = function(
            _AT_FDCWD,
            os.fsencode(source),
            _AT_FDCWD,
            os.fsencode(destination),
            _LINUX_RENAME_NOREPLACE,
        )
        if status != 0:
            _raise_for_rename_errno(ctypes.get_errno())
        return

    if primitive == _PRIMITIVE_MACOS_RENAMEX_NP:
        function = _load_posix_symbol("renamex_np")
        if function is None:  # pragma: no cover - resolved during planning
            raise _UnsupportedAtomicRenameError("renamex_np is unavailable")
        function.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
        function.restype = ctypes.c_int
        ctypes.set_errno(0)
        status = function(os.fsencode(source), os.fsencode(destination), _MACOS_RENAME_EXCL)
        if status != 0:
            _raise_for_rename_errno(ctypes.get_errno())
        return

    raise _UnsupportedAtomicRenameError(f"unknown rename primitive {primitive!r}")


# ---------------------------------------------------------------------------
# Path identity helpers (FD-BPUB-4)
# ---------------------------------------------------------------------------


def _resolve_directory(path: Path, role: str) -> tuple[Path, tuple[int, int]]:
    """Return the canonical path and filesystem identity of an existing directory.

    Fails closed whenever identity cannot be safely established, rather than
    falling back to unresolved string comparison.
    """
    if type(path) is not _CONCRETE_PATH_TYPE:
        raise _InvalidPublicationInputError(f"{role} must be an exact pathlib.Path")
    if not path.is_absolute():
        raise _UnsafePublicationPathError(f"{role} must be an absolute path")
    try:
        link_status = path.lstat()
    except OSError as error:
        raise _UnsafePublicationPathError(f"{role} does not exist") from error
    if stat.S_ISLNK(link_status.st_mode):
        raise _UnsafePublicationPathError(f"{role} must not be a symbolic link")
    if getattr(link_status, "st_file_attributes", 0) & _FILE_ATTRIBUTE_REPARSE_POINT:
        raise _UnsafePublicationPathError(f"{role} must not be a junction or reparse indirection")
    try:
        resolved = path.resolve(strict=True)
        status = resolved.stat()
    except OSError as error:
        raise _UnsafePublicationPathError(
            f"{role} canonical identity could not be established"
        ) from error
    if not stat.S_ISDIR(status.st_mode):
        raise _UnsafePublicationPathError(f"{role} must be an existing directory")
    if resolved != path:
        raise _UnsafePublicationPathError(f"{role} must already be a canonical path")
    return resolved, (status.st_dev, status.st_ino)


def _assert_disjoint(publication_parent: Path, protected_root: Path) -> None:
    """Reject equality and containment in both directions."""
    if publication_parent.is_relative_to(protected_root):
        raise _UnsafePublicationPathError(
            "the publication parent must not be inside a protected root"
        )
    if protected_root.is_relative_to(publication_parent):
        raise _UnsafePublicationPathError(
            "a protected root must not be inside the publication parent"
        )


def _validate_write_path_boundary(
    publication_parent: Path, protected_roots: tuple[Path, ...]
) -> tuple[Path, tuple[Path, ...]]:
    """Validate the publication parent and the immutable protected-root tuple."""
    if type(protected_roots) is not tuple:
        raise _InvalidPublicationInputError(
            "protected_roots must be an exact tuple of pathlib.Path values"
        )
    if not protected_roots:
        raise _InvalidPublicationInputError("protected_roots must not be empty")

    parent_path, parent_identity = _resolve_directory(publication_parent, "publication_parent")

    resolved_roots: list[Path] = []
    seen_identities: set[tuple[int, int]] = set()
    for index, root in enumerate(protected_roots):
        root_path, root_identity = _resolve_directory(root, f"protected_roots[{index}]")
        if root_identity in seen_identities:
            raise _UnsafePublicationPathError(
                "protected_roots contains a duplicate after canonical identity resolution"
            )
        seen_identities.add(root_identity)
        if root_identity == parent_identity:
            raise _UnsafePublicationPathError(
                "the publication parent must not equal a protected root"
            )
        _assert_disjoint(parent_path, root_path)
        resolved_roots.append(root_path)

    return parent_path, tuple(resolved_roots)


def _assert_direct_child_name(name: str) -> None:
    """Reject traversal, separator injection, dot components and stream suffixes."""
    if not name or name in {".", ".."}:
        raise _UnsafePublicationPathError("a publication child name must be a real name")
    if "/" in name or "\\" in name or os.sep in name or (os.altsep or "") in name:
        raise _UnsafePublicationPathError("a publication child name must not inject a separator")
    if ":" in name:
        raise _UnsafePublicationPathError(
            "a publication child name must not carry an alternate data stream"
        )
    if len(Path(name).parts) != 1:
        raise _UnsafePublicationPathError("a publication child name must be one component")


# ---------------------------------------------------------------------------
# Request and result binding (FD-BPUB-3, FD-BPUB-8)
# ---------------------------------------------------------------------------


def _verify_request_result_binding(request: FixtureSplitRequest, result: FixtureSplitResult) -> str:
    """Prove the result came from this exact request; return the authoritative fingerprint.

    Every check reuses an accepted primitive without weakening it. Accepted
    upstream typed errors propagate unchanged, because they attribute a failure
    more precisely than this module could.
    """
    if type(request) is not FixtureSplitRequest:
        raise _InvalidPublicationInputError("request must be an exact FixtureSplitRequest")
    if type(result) is not FixtureSplitResult:
        raise _InvalidPublicationInputError("result must be an exact FixtureSplitResult")
    if result.request_id != request.request_id:
        raise _InvalidPublicationInputError("result request_id does not match the request")
    if result.execution_evidence_ref != request.execution_evidence_ref:
        raise _InvalidPublicationInputError(
            "result execution_evidence_ref does not match the request"
        )

    record = result.split_fingerprint_record
    fingerprint = record.split_fingerprint
    if type(fingerprint) is not str or len(fingerprint) != _SHA256_LENGTH:
        raise _InvalidPublicationInputError("the split fingerprint must be 64 hex characters")
    if not set(fingerprint) <= _HEX_DIGITS:
        raise _InvalidPublicationInputError("the split fingerprint must be lowercase hex")

    # The accepted record verification proves the fingerprint binds its identity.
    verify_split_fingerprint_record(record)

    # Descriptors exist for four roles only. Verify each one that is present, and
    # never manufacture a requirement for a surface the record does not describe.
    for descriptor in record.identity.artifact_descriptors:
        attribute = _DESCRIBED_ROLE_ATTRIBUTES.get(descriptor.role)
        if attribute is None:
            raise _InvalidPublicationInputError(
                f"unexpected artifact descriptor role {descriptor.role!r}"
            )
        verify_descriptor_against_bytes(descriptor, getattr(result, attribute))

    # The two undescribed surfaces are bound through their accepted carriers.
    identity_core_bytes = result.split_summary_identity_core.canonical_bytes()
    if result.split_summary_identity_core_bytes != identity_core_bytes:
        raise _InvalidPublicationInputError(
            "summary identity core bytes do not match the carried core"
        )
    if result.audit_report_bytes != result.audit_report.to_canonical_bytes():
        raise _InvalidPublicationInputError("audit report bytes do not match the carried report")
    if fingerprint.encode("utf-8") not in result.split_summary_document_bytes:
        raise _InvalidPublicationInputError(
            "the final summary does not carry the authoritative fingerprint"
        )
    return fingerprint


# ---------------------------------------------------------------------------
# Planning (FD-BPUB-8) — complete, verified and frozen before any mutation
# ---------------------------------------------------------------------------


def _build_manifest_document(
    request_id: str,
    split_fingerprint: str,
    final_directory_name: str,
    payload_files: Sequence[_PlannedFile],
) -> dict[str, object]:
    """Build the exact five-member, non-circular publication manifest.

    The manifest describes only the six payload files. It carries no digest or
    size of itself, no absolute path, no protected root, no timestamp, no runtime
    or host metadata, and no evidence-promotion claim. The per-file descriptor
    field is ``surface``, and the accepted artifact schema-version table is never
    consulted, projected or mapped here: it governs the four-role descriptor layer
    of the fingerprint record, not this manifest.
    """
    surface_by_filename = {binding[0]: binding[1] for binding in _PAYLOAD_BINDINGS}
    records: list[dict[str, object]] = [
        {
            "filename": planned.filename,
            "surface": surface_by_filename[planned.filename],
            "sha256": planned.sha256,
            "byte_size": planned.byte_size,
        }
        for planned in payload_files
    ]
    return {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "request_id": request_id,
        "split_fingerprint": split_fingerprint,
        "publication_directory_name": final_directory_name,
        "files": records,
    }


def _plan_file(filename: str, payload: bytes) -> _PlannedFile:
    """Freeze one planned file with a recomputed digest and a recomputed size."""
    if type(payload) is not bytes:
        raise _InvalidPublicationInputError(f"{filename} payload must be exact bytes")
    return _PlannedFile(
        filename=filename,
        payload=payload,
        sha256=sha256_of_bytes(payload),
        byte_size=len(payload),
    )


def _build_plan(
    request: FixtureSplitRequest,
    result: FixtureSplitResult,
    publication_parent: Path,
    protected_roots: tuple[Path, ...],
) -> _PublicationPlan:
    """Validate everything, build the complete plan and freeze it. No mutation here."""
    # 1-5. exact types, identity binding, authoritative fingerprint, record, descriptors
    split_fingerprint = _verify_request_result_binding(request, result)

    # 6-8. six exact byte surfaces, with recomputed digests and sizes
    payload_files = tuple(
        _plan_file(filename, getattr(result, attribute))
        for filename, _surface, attribute in _PAYLOAD_BINDINGS
    )

    # 9-10. directory names, then the exact canonical manifest bytes
    final_directory_name = f"{_FINAL_DIRECTORY_PREFIX}{split_fingerprint}"
    staging_directory_name = (
        f"{_STAGING_DIRECTORY_PREFIX}{split_fingerprint}{_STAGING_DIRECTORY_SUFFIX}"
    )
    manifest_document = _build_manifest_document(
        result.request_id, split_fingerprint, final_directory_name, payload_files
    )
    manifest_file = _plan_file(_MANIFEST_FILENAME, canonical_json_bytes(manifest_document))

    # 11-12. filename uniqueness and the exact seven-name inventory
    payload_names = [planned.filename for planned in payload_files]
    if len(set(payload_names)) != len(payload_names):
        raise _InvalidPublicationInputError("payload filenames must be unique")
    if tuple(sorted([*payload_names, manifest_file.filename])) != _PUBLISHED_FILENAMES:
        raise _InvalidPublicationInputError("the planned inventory is not the exact seven names")

    # 13-14. child-name safety, then the write-path boundary
    _assert_direct_child_name(final_directory_name)
    _assert_direct_child_name(staging_directory_name)
    parent_path, _resolved_roots = _validate_write_path_boundary(
        publication_parent, protected_roots
    )
    staging_directory = parent_path / staging_directory_name
    final_directory = parent_path / final_directory_name

    # 15-16. staging and final must both be absent
    if staging_directory.exists() or staging_directory.is_symlink():
        raise _PublicationTargetConflictError("the staging directory already exists")
    if final_directory.exists() or final_directory.is_symlink():
        raise _PublicationTargetConflictError("the final directory already exists")

    # 17. the atomic no-replace primitive, resolved before any attempt is acquired
    rename_primitive = _resolve_rename_primitive()

    # 18. freeze
    return _PublicationPlan(
        request_id=result.request_id,
        split_fingerprint=split_fingerprint,
        publication_parent=parent_path,
        staging_directory=staging_directory,
        final_directory=final_directory,
        final_directory_name=final_directory_name,
        payload_files=payload_files,
        manifest_file=manifest_file,
        rename_primitive=rename_primitive,
    )


# ---------------------------------------------------------------------------
# Mutation phase (FD-BPUB-9 .. FD-BPUB-13)
# ---------------------------------------------------------------------------


def _sync_file(file_descriptor: int) -> None:
    """Apply the supported file synchronization primitive for this platform."""
    os.fsync(file_descriptor)


def _write_exact_once(directory: Path, planned: _PlannedFile) -> None:
    """Create one file exclusively, write it once, flush, synchronize and close."""
    target = directory / planned.filename
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | _O_BINARY | _O_NOFOLLOW
    try:
        descriptor = os.open(target, flags, 0o600)
    except OSError as error:
        raise _ExclusiveWriteError(f"exclusive creation of {planned.filename} failed") from error
    try:
        with os.fdopen(descriptor, "wb", closefd=True) as handle:
            handle.write(planned.payload)
            handle.flush()
            _sync_file(handle.fileno())
    except OSError as error:
        raise _ExclusiveWriteError(f"writing {planned.filename} failed") from error


def _read_back(target: Path, expected: _PlannedFile) -> bytes:
    """Reopen read-only without following an indirection and verify the exact bytes."""
    flags = os.O_RDONLY | _O_BINARY | _O_NOFOLLOW
    try:
        descriptor = os.open(target, flags)
    except OSError as error:
        raise _ContentVerificationError(
            f"{expected.filename} could not be reopened for verification"
        ) from error
    try:
        status = os.fstat(descriptor)
        if not stat.S_ISREG(status.st_mode):
            raise _ContentVerificationError(f"{expected.filename} is not a regular file")
        if status.st_nlink > 1:
            raise _ContentVerificationError(f"{expected.filename} has more than one hard link")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
    finally:
        os.close(descriptor)
    observed = b"".join(chunks)
    if observed != expected.payload:
        raise _ContentVerificationError(f"{expected.filename} bytes do not match the plan")
    if sha256_of_bytes(observed) != expected.sha256:
        raise _ContentVerificationError(f"{expected.filename} digest does not match the plan")
    if len(observed) != expected.byte_size:
        raise _ContentVerificationError(f"{expected.filename} size does not match the plan")
    return observed


def _verify_directory_inventory(
    directory: Path, plan: _PublicationPlan, failure: type[_PublicationError]
) -> None:
    """Derive the inventory from the filesystem and verify it exactly.

    Hard-link substitution is rejected wherever the platform reports a usable
    link count. Where a platform cannot report one, no detection is claimed.
    """
    observed_names: list[str] = []
    for entry in directory.iterdir():
        entry_status = entry.lstat()
        if stat.S_ISLNK(entry_status.st_mode):
            raise failure(f"{entry.name} is a symbolic link")
        if getattr(entry_status, "st_file_attributes", 0) & _FILE_ATTRIBUTE_REPARSE_POINT:
            raise failure(f"{entry.name} is a junction or reparse indirection")
        if not stat.S_ISREG(entry_status.st_mode):
            raise failure(f"{entry.name} is not a regular file")
        observed_names.append(entry.name)

    if tuple(sorted(observed_names)) != _PUBLISHED_FILENAMES:
        raise failure("the directory inventory is not the exact seven names")

    for planned in (*plan.payload_files, plan.manifest_file):
        try:
            _read_back(directory / planned.filename, planned)
        except _ContentVerificationError as error:
            # Re-typed by category, never by inspecting the original message.
            raise failure(f"{planned.filename} failed content reverification") from error

    document = json.loads(plan.manifest_file.payload.decode("utf-8"))
    if set(document) != {
        "schema_version",
        "request_id",
        "split_fingerprint",
        "publication_directory_name",
        "files",
    }:
        raise failure("the manifest does not carry exactly the five members")
    if document["request_id"] != plan.request_id:
        raise failure("the manifest request_id does not match the request")
    if document["split_fingerprint"] != plan.split_fingerprint:
        raise failure("the manifest split_fingerprint does not match the result")
    if document["publication_directory_name"] != plan.final_directory_name:
        raise failure("the manifest publication_directory_name does not match")
    described = [record["filename"] for record in document["files"]]
    if tuple(described) != tuple(planned.filename for planned in plan.payload_files):
        raise failure("the manifest does not describe exactly the six payload files")


def _publish_fixture_split_v1(
    request: FixtureSplitRequest,
    result: FixtureSplitResult,
    *,
    publication_parent: Path,
    protected_roots: tuple[Path, ...],
) -> _PublicationReceipt:
    """Publish one exact fixture result atomically, or fail closed.

    After the staging directory exists, any failure leaves it exactly as it was
    left: nothing is deleted, cleaned, retried, resumed, repaired, renamed to an
    alternate name or completed. No receipt is returned on any failure.
    """
    plan = _build_plan(request, result, publication_parent, protected_roots)

    # FD-BPUB-9: the one attempt is acquired by exclusive directory creation.
    try:
        plan.staging_directory.mkdir()
    except FileExistsError as error:
        raise _PublicationTargetConflictError("the staging directory already exists") from error
    except OSError as error:
        raise _StagingAcquisitionError("exclusive staging creation failed") from error

    # FD-BPUB-10 and FD-BPUB-11: six payloads ascending, then the manifest last.
    for planned in plan.payload_files:
        _write_exact_once(plan.staging_directory, planned)
        _read_back(plan.staging_directory / planned.filename, planned)
    _write_exact_once(plan.staging_directory, plan.manifest_file)
    _read_back(plan.staging_directory / plan.manifest_file.filename, plan.manifest_file)

    # FD-BPUB-13: the pre-rename inventory comes from the filesystem, not the plan.
    _verify_directory_inventory(plan.staging_directory, plan, _InventoryVerificationError)

    # FD-BPUB-14: exactly one same-parent atomic no-replace directory rename.
    _atomic_no_replace_rename(plan.staging_directory, plan.final_directory, plan.rename_primitive)

    # FD-BPUB-16: verify the visible final directory; never roll back or repair.
    if plan.staging_directory.exists():
        raise _PostRenameVerificationError("the staging directory still exists")
    final_status = plan.final_directory.lstat()
    if stat.S_ISLNK(final_status.st_mode):
        raise _PostRenameVerificationError("the final directory is a symbolic link")
    if getattr(final_status, "st_file_attributes", 0) & _FILE_ATTRIBUTE_REPARSE_POINT:
        raise _PostRenameVerificationError("the final directory is a reparse indirection")
    if not stat.S_ISDIR(final_status.st_mode):
        raise _PostRenameVerificationError("the final directory is not a directory")
    parent_status = plan.publication_parent.stat()
    observed_parent = plan.final_directory.parent.stat()
    if (observed_parent.st_dev, observed_parent.st_ino) != (
        parent_status.st_dev,
        parent_status.st_ino,
    ):
        raise _PostRenameVerificationError("the final directory parent identity does not match")
    _verify_directory_inventory(plan.final_directory, plan, _PostRenameVerificationError)

    return _PublicationReceipt(
        publication_directory=plan.final_directory,
        request_id=plan.request_id,
        split_fingerprint=plan.split_fingerprint,
        publication_manifest_sha256=plan.manifest_file.sha256,
        published_filenames=_PUBLISHED_FILENAMES,
    )
