"""Fail-closed executor allowlist parsing for MESC Backbone Tournament activation.

This module implements only the immutable executor/harness allowlist primitive required by
``FD-MESC-BT-EXEC-1`` Section D. It performs no model access, model retrieval, prompt dispatch,
inference, generation, ranking, winner selection, network access, subprocess execution, or
filesystem mutation.

The accepted wire format is deliberately narrower than the repository's older canonical JSON
helpers: the allowlist is one UTF-8 JSON array with no BOM and **no trailing newline**. Every
entry has exactly ``git_blob_sha`` and ``path``. Duplicate JSON members are rejected before a
Python mapping exists, and accepted bytes must equal a canonical reserialization byte-for-byte.

Git-tree/runtime identity resolution is dependency-injected. The verifier therefore cannot fetch,
checkout, import, or execute an allowlisted path itself; callers must provide already-resolved Git
object metadata from the exact commit/tree under independent review.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Final

_PATH_RE: Final = re.compile(r"^[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*$")
_GIT_BLOB_RE: Final = re.compile(r"^[0-9a-f]{40}$")
_ALLOWED_REGULAR_FILE_MODES: Final = frozenset({"100644", "100755"})
_REQUIRED_ENTRY_KEYS: Final = frozenset({"git_blob_sha", "path"})
_UTF8_BOM: Final = b"\xef\xbb\xbf"


class ExecutorAllowlistError(ValueError):
    """Base class for every fail-closed executor allowlist violation."""


class ExecutorAllowlistJsonError(ExecutorAllowlistError):
    """The supplied bytes are not valid duplicate-member-safe UTF-8 JSON."""


class ExecutorAllowlistDuplicateMemberError(ExecutorAllowlistJsonError):
    """A JSON object contains the same member name more than once."""


class ExecutorAllowlistSchemaError(ExecutorAllowlistError):
    """The parsed value violates the closed allowlist schema."""


class ExecutorAllowlistCanonicalizationError(ExecutorAllowlistError):
    """The supplied bytes are valid JSON but are not the exact canonical bytes."""


class ExecutorAllowlistResolutionError(ExecutorAllowlistError):
    """An allowlisted path does not resolve to the exact required regular-file blob."""


@dataclass(frozen=True, slots=True)
class ExecutorAllowlistEntry:
    """One exact executable/imported path and its expected Git blob identity."""

    git_blob_sha: str
    path: str


@dataclass(frozen=True, slots=True)
class ExecutorAllowlist:
    """One validated canonical allowlist and the digest of its exact supplied bytes."""

    entries: tuple[ExecutorAllowlistEntry, ...]
    sha256: str
    byte_length: int


@dataclass(frozen=True, slots=True)
class ResolvedExecutorObject:
    """Git metadata returned by a trusted, separately reviewed resolver."""

    object_type: str
    mode: str
    git_blob_sha: str


ExecutorObjectResolver = Callable[[str], ResolvedExecutorObject]


def parse_executor_allowlist(payload: bytes) -> ExecutorAllowlist:
    """Parse and validate the exact canonical ``EXECUTOR_PATHS_AND_BLOB_SHAS`` bytes.

    Validation is fail-closed and includes duplicate-member rejection, exact top-level and entry
    schemas, scalar types, ASCII/path/blob grammar, path uniqueness/order, canonical serialization,
    and SHA-256 over the exact accepted bytes.
    """
    if type(payload) is not bytes:
        raise ExecutorAllowlistJsonError("executor allowlist payload must be exact bytes")
    if payload.startswith(_UTF8_BOM):
        raise ExecutorAllowlistJsonError("UTF-8 BOM is prohibited")

    parsed = _load_duplicate_safe_json(payload)
    if type(parsed) is not list:
        raise ExecutorAllowlistSchemaError("executor allowlist top level must be a JSON array")

    entries: list[ExecutorAllowlistEntry] = []
    seen_paths: set[str] = set()
    for index, raw_entry in enumerate(parsed):
        entry = _validate_entry(raw_entry, index=index)
        if entry.path in seen_paths:
            raise ExecutorAllowlistSchemaError(f"duplicate executor path: {entry.path!r}")
        seen_paths.add(entry.path)
        entries.append(entry)

    paths = [entry.path for entry in entries]
    if paths != sorted(paths, key=lambda value: value.encode("ascii")):
        raise ExecutorAllowlistCanonicalizationError(
            "executor allowlist entries must be sorted by decoded path ASCII bytes"
        )

    canonical = canonical_executor_allowlist_bytes(tuple(entries))
    if payload != canonical:
        raise ExecutorAllowlistCanonicalizationError(
            "supplied executor allowlist bytes are not the exact canonical serialization"
        )

    return ExecutorAllowlist(
        entries=tuple(entries),
        sha256=hashlib.sha256(payload).hexdigest(),
        byte_length=len(payload),
    )


def canonical_executor_allowlist_bytes(entries: tuple[ExecutorAllowlistEntry, ...]) -> bytes:
    """Serialize already-validated entries using the Section D canonical byte rules.

    This helper intentionally emits no terminal newline. It is not a substitute for
    :func:`parse_executor_allowlist`: callers must parse and byte-compare externally supplied
    bytes before treating an allowlist digest as authoritative.
    """
    document = [
        {"git_blob_sha": entry.git_blob_sha, "path": entry.path}
        for entry in entries
    ]
    try:
        return json.dumps(
            document,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("ascii")
    except (TypeError, UnicodeEncodeError, ValueError) as error:
        raise ExecutorAllowlistCanonicalizationError(
            "executor allowlist cannot be serialized as canonical ASCII JSON"
        ) from error


def verify_executor_allowlist_objects(
    allowlist: ExecutorAllowlist,
    resolve: ExecutorObjectResolver,
) -> None:
    """Verify every allowlist entry against injected exact-commit Git object metadata.

    The resolver must be bound by its caller to the independently reviewed execution commit/tree.
    Only regular-file blob modes ``100644`` and ``100755`` are accepted. Symlinks, trees,
    gitlinks/submodules, missing objects, non-blobs, mode mismatches, and blob mismatches fail.
    """
    if type(allowlist) is not ExecutorAllowlist:
        raise ExecutorAllowlistResolutionError("allowlist must be a validated ExecutorAllowlist")

    for entry in allowlist.entries:
        try:
            resolved = resolve(entry.path)
        except Exception as error:
            raise ExecutorAllowlistResolutionError(
                f"failed to resolve allowlisted executor path {entry.path!r}"
            ) from error

        if type(resolved) is not ResolvedExecutorObject:
            raise ExecutorAllowlistResolutionError(
                f"resolver returned an invalid object for {entry.path!r}"
            )
        if resolved.object_type != "blob":
            raise ExecutorAllowlistResolutionError(
                f"allowlisted executor path {entry.path!r} must resolve to a blob"
            )
        if resolved.mode not in _ALLOWED_REGULAR_FILE_MODES:
            raise ExecutorAllowlistResolutionError(
                f"allowlisted executor path {entry.path!r} has prohibited mode {resolved.mode!r}"
            )
        if _GIT_BLOB_RE.fullmatch(resolved.git_blob_sha) is None:
            raise ExecutorAllowlistResolutionError(
                f"resolver returned an invalid Git blob SHA for {entry.path!r}"
            )
        if resolved.git_blob_sha != entry.git_blob_sha:
            raise ExecutorAllowlistResolutionError(
                f"Git blob mismatch for allowlisted executor path {entry.path!r}"
            )


def _load_duplicate_safe_json(payload: bytes) -> object:
    try:
        text = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise ExecutorAllowlistJsonError("executor allowlist must be valid UTF-8") from error

    try:
        return json.loads(
            text,
            object_pairs_hook=_object_from_unique_pairs,
            parse_constant=_reject_json_constant,
        )
    except ExecutorAllowlistDuplicateMemberError:
        raise
    except (json.JSONDecodeError, ExecutorAllowlistJsonError) as error:
        if isinstance(error, ExecutorAllowlistJsonError):
            raise
        raise ExecutorAllowlistJsonError("executor allowlist is not valid JSON") from error


def _object_from_unique_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    document: dict[str, object] = {}
    for key, value in pairs:
        if key in document:
            raise ExecutorAllowlistDuplicateMemberError(f"duplicate JSON member: {key!r}")
        document[key] = value
    return document


def _reject_json_constant(value: str) -> object:
    raise ExecutorAllowlistJsonError(f"non-standard JSON constant is prohibited: {value}")


def _validate_entry(raw_entry: object, *, index: int) -> ExecutorAllowlistEntry:
    if type(raw_entry) is not dict:
        raise ExecutorAllowlistSchemaError(f"allowlist entry {index} must be a JSON object")

    entry_keys = frozenset(raw_entry)
    if entry_keys != _REQUIRED_ENTRY_KEYS:
        raise ExecutorAllowlistSchemaError(
            f"allowlist entry {index} must contain exactly git_blob_sha and path"
        )

    raw_path = raw_entry["path"]
    raw_blob = raw_entry["git_blob_sha"]
    if type(raw_path) is not str or type(raw_blob) is not str:
        raise ExecutorAllowlistSchemaError(
            f"allowlist entry {index} path and git_blob_sha must be JSON strings"
        )

    try:
        raw_path.encode("ascii")
        raw_blob.encode("ascii")
    except UnicodeEncodeError as error:
        raise ExecutorAllowlistSchemaError(
            f"allowlist entry {index} values must contain ASCII bytes only"
        ) from error

    if _PATH_RE.fullmatch(raw_path) is None:
        raise ExecutorAllowlistSchemaError(
            f"allowlist entry {index} has invalid path grammar: {raw_path!r}"
        )
    if any(component in {".", ".."} for component in raw_path.split("/")):
        raise ExecutorAllowlistSchemaError(
            f"allowlist entry {index} path contains a prohibited dot component"
        )
    if _GIT_BLOB_RE.fullmatch(raw_blob) is None:
        raise ExecutorAllowlistSchemaError(
            f"allowlist entry {index} has invalid Git blob SHA"
        )

    return ExecutorAllowlistEntry(git_blob_sha=raw_blob, path=raw_path)
