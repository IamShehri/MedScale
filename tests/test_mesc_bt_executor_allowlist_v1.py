"""Fixture-only qualification for the Backbone Tournament executor allowlist primitive.

These tests perform no model access, retrieval, inference, generation, network access, subprocess
execution, or filesystem mutation. Git object resolution is injected with deterministic fakes.
"""

from __future__ import annotations

import hashlib

import pytest

from medscale.mesc._bt_executor_allowlist_v1 import (
    ExecutorAllowlistCanonicalizationError,
    ExecutorAllowlistDuplicateMemberError,
    ExecutorAllowlistJsonError,
    ExecutorAllowlistResolutionError,
    ExecutorAllowlistSchemaError,
    ResolvedExecutorObject,
    canonical_executor_allowlist_bytes,
    parse_executor_allowlist,
    verify_executor_allowlist_objects,
)

_SHA_A = "a" * 40
_SHA_B = "b" * 40
_VALID = (
    f'[{{"git_blob_sha":"{_SHA_A}","path":"scripts/runner.py"}},'
    f'{{"git_blob_sha":"{_SHA_B}","path":"src/medscale/mesc/harness.py"}}]'
).encode("ascii")


def test_valid_canonical_allowlist_binds_exact_bytes_and_digest() -> None:
    allowlist = parse_executor_allowlist(_VALID)

    assert [entry.path for entry in allowlist.entries] == [
        "scripts/runner.py",
        "src/medscale/mesc/harness.py",
    ]
    assert allowlist.sha256 == hashlib.sha256(_VALID).hexdigest()
    assert allowlist.byte_length == len(_VALID)
    assert canonical_executor_allowlist_bytes(allowlist.entries) == _VALID
    assert not _VALID.endswith(b"\n")


def test_utf8_bom_is_rejected() -> None:
    with pytest.raises(ExecutorAllowlistJsonError, match="BOM"):
        parse_executor_allowlist(b"\xef\xbb\xbf" + _VALID)


def test_invalid_utf8_is_rejected() -> None:
    with pytest.raises(ExecutorAllowlistJsonError, match="UTF-8"):
        parse_executor_allowlist(b"[\xff]")


def test_top_level_must_be_array() -> None:
    with pytest.raises(ExecutorAllowlistSchemaError, match="top level"):
        parse_executor_allowlist(b"{}")


def test_duplicate_path_member_is_rejected_before_mapping_creation() -> None:
    payload = f'[{{"git_blob_sha":"{_SHA_A}","path":"a.py","path":"b.py"}}]'.encode("ascii")
    with pytest.raises(ExecutorAllowlistDuplicateMemberError, match="path"):
        parse_executor_allowlist(payload)


def test_duplicate_git_blob_member_is_rejected_before_mapping_creation() -> None:
    payload = (
        f'[{{"git_blob_sha":"{_SHA_A}","git_blob_sha":"{_SHA_B}","path":"a.py"}}]'
    ).encode("ascii")
    with pytest.raises(ExecutorAllowlistDuplicateMemberError, match="git_blob_sha"):
        parse_executor_allowlist(payload)


@pytest.mark.parametrize(
    "payload",
    [
        b"[[]]",
        f'[{{"git_blob_sha":"{_SHA_A}"}}]'.encode("ascii"),
        f'[{{"git_blob_sha":"{_SHA_A}","path":"a.py","extra":"x"}}]'.encode("ascii"),
        f'[{{"git_blob_sha":"{_SHA_A}","path":1}}]'.encode("ascii"),
        b'[{"git_blob_sha":1,"path":"a.py"}]',
    ],
)
def test_closed_entry_schema_is_enforced(payload: bytes) -> None:
    with pytest.raises(ExecutorAllowlistSchemaError):
        parse_executor_allowlist(payload)


@pytest.mark.parametrize(
    "path",
    [
        "",
        "/absolute.py",
        "a//b.py",
        ".",
        "..",
        "a/./b.py",
        "a/../b.py",
        "a\\b.py",
        "ümlaut.py",
    ],
)
def test_path_grammar_is_fail_closed(path: str) -> None:
    payload = (
        '[{"git_blob_sha":"'
        + _SHA_A
        + '","path":"'
        + path.replace("\\", "\\\\")
        + '"}]'
    ).encode("utf-8")
    with pytest.raises(ExecutorAllowlistSchemaError):
        parse_executor_allowlist(payload)


@pytest.mark.parametrize("blob_sha", ["A" * 40, "a" * 39, "g" * 40, ""])
def test_git_blob_sha_must_be_exact_lowercase_40_hex(blob_sha: str) -> None:
    payload = f'[{{"git_blob_sha":"{blob_sha}","path":"a.py"}}]'.encode("ascii")
    with pytest.raises(ExecutorAllowlistSchemaError, match="Git blob SHA"):
        parse_executor_allowlist(payload)


def test_duplicate_decoded_paths_are_rejected() -> None:
    payload = (
        f'[{{"git_blob_sha":"{_SHA_A}","path":"a.py"}},'
        f'{{"git_blob_sha":"{_SHA_B}","path":"a.py"}}]'
    ).encode("ascii")
    with pytest.raises(ExecutorAllowlistSchemaError, match="duplicate executor path"):
        parse_executor_allowlist(payload)


def test_entries_must_be_sorted_by_decoded_ascii_path() -> None:
    payload = (
        f'[{{"git_blob_sha":"{_SHA_B}","path":"b.py"}},'
        f'{{"git_blob_sha":"{_SHA_A}","path":"a.py"}}]'
    ).encode("ascii")
    with pytest.raises(ExecutorAllowlistCanonicalizationError, match="sorted"):
        parse_executor_allowlist(payload)


@pytest.mark.parametrize(
    "payload",
    [
        f'[ {{"git_blob_sha":"{_SHA_A}","path":"a.py"}}]'.encode("ascii"),
        f'[{{"path":"a.py","git_blob_sha":"{_SHA_A}"}}]'.encode("ascii"),
        f'[{{"git_blob_sha":"{_SHA_A}","path":"a.py"}}]\n'.encode("ascii"),
        f'[{{"git_blob_sha":"{_SHA_A}","path":"a\\u002epy"}}]'.encode("ascii"),
    ],
)
def test_noncanonical_serialization_is_rejected(payload: bytes) -> None:
    with pytest.raises(ExecutorAllowlistCanonicalizationError):
        parse_executor_allowlist(payload)


def test_nonstandard_json_constant_is_rejected() -> None:
    with pytest.raises(ExecutorAllowlistJsonError, match="constant"):
        parse_executor_allowlist(b"[NaN]")


def test_regular_file_blob_resolution_passes_for_100644_and_100755() -> None:
    allowlist = parse_executor_allowlist(_VALID)
    resolved = {
        "scripts/runner.py": ResolvedExecutorObject("blob", "100755", _SHA_A),
        "src/medscale/mesc/harness.py": ResolvedExecutorObject("blob", "100644", _SHA_B),
    }

    verify_executor_allowlist_objects(allowlist, resolved.__getitem__)


@pytest.mark.parametrize("mode", ["120000", "160000", "040000", "100600"])
def test_non_regular_or_unapproved_modes_are_blocked(mode: str) -> None:
    allowlist = parse_executor_allowlist(
        f'[{{"git_blob_sha":"{_SHA_A}","path":"a.py"}}]'.encode("ascii")
    )

    def resolve(_: str) -> ResolvedExecutorObject:
        return ResolvedExecutorObject("blob", mode, _SHA_A)

    with pytest.raises(ExecutorAllowlistResolutionError, match="prohibited mode"):
        verify_executor_allowlist_objects(allowlist, resolve)


def test_non_blob_object_is_blocked() -> None:
    allowlist = parse_executor_allowlist(
        f'[{{"git_blob_sha":"{_SHA_A}","path":"a.py"}}]'.encode("ascii")
    )

    def resolve(_: str) -> ResolvedExecutorObject:
        return ResolvedExecutorObject("tree", "040000", _SHA_A)

    with pytest.raises(ExecutorAllowlistResolutionError, match="must resolve to a blob"):
        verify_executor_allowlist_objects(allowlist, resolve)


def test_blob_identity_mismatch_is_blocked() -> None:
    allowlist = parse_executor_allowlist(
        f'[{{"git_blob_sha":"{_SHA_A}","path":"a.py"}}]'.encode("ascii")
    )

    def resolve(_: str) -> ResolvedExecutorObject:
        return ResolvedExecutorObject("blob", "100644", _SHA_B)

    with pytest.raises(ExecutorAllowlistResolutionError, match="Git blob mismatch"):
        verify_executor_allowlist_objects(allowlist, resolve)


def test_resolver_failure_is_fail_closed() -> None:
    allowlist = parse_executor_allowlist(
        f'[{{"git_blob_sha":"{_SHA_A}","path":"a.py"}}]'.encode("ascii")
    )

    def resolve(_: str) -> ResolvedExecutorObject:
        raise KeyError("missing")

    with pytest.raises(ExecutorAllowlistResolutionError, match="failed to resolve"):
        verify_executor_allowlist_objects(allowlist, resolve)