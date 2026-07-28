"""Canonical JSON and JSONL contract tests for P01-04B2A (FD-B2A-2, FD-B2A-3, FD-B2A-8).

Golden vectors are committed as explicit byte and digest literals derived
independently of the implementation under test.  Recomputing them with the
production serializer would make the test agree with whatever the code does,
which is exactly the failure mode cross-platform evidence cannot detect.
"""

from __future__ import annotations

import builtins
import hashlib
import io
import os
import pathlib
import socket
from collections import OrderedDict
from collections.abc import Iterator, Mapping
from decimal import Decimal
from enum import Enum, IntEnum, StrEnum
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from medscale.mesc._canonical_json_v1 import (
    CanonicalContractError,
    CanonicalizationFailureError,
    FloatingPointValueProhibitedError,
    NonStringObjectKeyError,
    UnsupportedValueTypeError,
    canonical_json_bytes,
    canonical_jsonl_bytes,
    canonical_sha256,
    sha256_of_bytes,
)

# --------------------------------------------------------------------------
# Golden vectors (literal; independently derived)
# --------------------------------------------------------------------------

GOLDEN_DOCUMENT: dict[str, Any] = {
    "zulu": None,
    "alpha": {"nested": [1, 2, 3], "flag": True},
    "Beta": "café ☕",
    "delta": [],
    "echo": {},
    "big": 12345678901234567890123456789,
    "neg": -42,
}

GOLDEN_DOCUMENT_BYTES = (
    b'{"Beta":"caf\xc3\xa9 \xe2\x98\x95","alpha":{"flag":true,"nested":[1,2,3]},'
    b'"big":12345678901234567890123456789,"delta":[],"echo":{},"neg":-42,'
    b'"zulu":null}\n'
)
GOLDEN_DOCUMENT_SHA256 = "63a17a304622ecebe6950e8a0ece7286c6c0699cdde05ff3f4f2b1d240cf67a4"

GOLDEN_RECORDS: list[dict[str, Any]] = [
    {"b": 1, "a": "x"},
    {"z": [True, False, None]},
    {},
]
GOLDEN_JSONL_BYTES = b'{"a":"x","b":1}\n{"z":[true,false,null]}\n{}\n'
GOLDEN_JSONL_SHA256 = "d18b1feb10ffa58a50228907fd2f15e09466550d80660f90b560a0b6d8abf574"


class _Colour(Enum):
    RED = "red"


class _IntColour(IntEnum):
    RED = 1


class _StrColour(StrEnum):
    RED = "red"


class _MyInt(int):
    pass


class _MyStr(str):
    pass


class _PlainMapping(Mapping[str, object]):
    """A well-behaved custom Mapping that is not a dict."""

    def __init__(self, data: dict[str, object]) -> None:
        self._data = dict(data)

    def __getitem__(self, key: str) -> object:
        return self._data[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)


class _InjectingMapping(Mapping[object, object]):
    """A hostile Mapping that injects a non-string key on every iteration."""

    def __init__(self, data: dict[object, object]) -> None:
        self._data: dict[object, object] = dict(data)
        self.iterations = 0

    def __getitem__(self, key: object) -> object:
        return self._data[key]

    def __iter__(self) -> Iterator[object]:
        self.iterations += 1
        self._data[self.iterations] = "injected"
        return iter(list(self._data))

    def __len__(self) -> int:
        return len(self._data)


# --------------------------------------------------------------------------
# Golden vectors and byte contract
# --------------------------------------------------------------------------


def test_golden_document_bytes_are_exact() -> None:
    assert canonical_json_bytes(GOLDEN_DOCUMENT) == GOLDEN_DOCUMENT_BYTES


def test_golden_document_digest_is_exact() -> None:
    assert canonical_sha256(GOLDEN_DOCUMENT) == GOLDEN_DOCUMENT_SHA256


def test_golden_jsonl_bytes_are_exact() -> None:
    assert canonical_jsonl_bytes(GOLDEN_RECORDS) == GOLDEN_JSONL_BYTES


def test_golden_jsonl_digest_is_exact() -> None:
    assert sha256_of_bytes(canonical_jsonl_bytes(GOLDEN_RECORDS)) == GOLDEN_JSONL_SHA256


def test_output_is_bytes_not_text() -> None:
    assert isinstance(canonical_json_bytes({"a": 1}), bytes)
    assert isinstance(canonical_jsonl_bytes([{"a": 1}]), bytes)


def test_exactly_one_terminal_line_feed() -> None:
    data = canonical_json_bytes(GOLDEN_DOCUMENT)
    assert data.endswith(b"\n")
    assert data.count(b"\n") == 1
    assert not data[:-1].endswith(b"\n")


def test_terminal_line_feed_is_inside_the_hashed_bytes() -> None:
    data = canonical_json_bytes(GOLDEN_DOCUMENT)
    assert canonical_sha256(GOLDEN_DOCUMENT) == hashlib.sha256(data).hexdigest()
    # Hashing the payload without its terminal LF must give a different digest.
    assert hashlib.sha256(data[:-1]).hexdigest() != GOLDEN_DOCUMENT_SHA256


def test_no_byte_order_mark() -> None:
    assert not canonical_json_bytes({"a": 1}).startswith(b"\xef\xbb\xbf")
    assert b"\xef\xbb\xbf" not in canonical_json_bytes({"a": "café"})


def test_no_carriage_return_anywhere() -> None:
    assert b"\r" not in canonical_json_bytes({"a": "line", "b": ["c"]})
    assert b"\r" not in canonical_jsonl_bytes(GOLDEN_RECORDS)


def test_compact_separators_and_no_indentation() -> None:
    data = canonical_json_bytes({"a": 1, "b": [1, 2], "c": {"d": 2}})
    assert data == b'{"a":1,"b":[1,2],"c":{"d":2}}\n'
    assert b", " not in data
    assert b": " not in data
    assert b"  " not in data


def test_output_is_valid_utf8() -> None:
    canonical_json_bytes({"k": "café ☕ 日本語"}).decode("utf-8")


# --------------------------------------------------------------------------
# Supported value domain
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, b"null\n"),
        (True, b"true\n"),
        (False, b"false\n"),
        (0, b"0\n"),
        (-1, b"-1\n"),
        (10**30, b"1" + b"0" * 30 + b"\n"),
        ("", b'""\n'),
        ("x", b'"x"\n'),
        ([], b"[]\n"),
        ({}, b"{}\n"),
    ],
)
def test_supported_scalar_and_empty_containers(value: object, expected: bytes) -> None:
    assert canonical_json_bytes(value) == expected


def test_nested_values_round_through_every_supported_category() -> None:
    document: dict[str, Any] = {
        "a": [None, True, 1, "s", [], {}],
        "b": {"c": {"d": [1, {"e": False}]}},
    }
    assert canonical_json_bytes(document) == (
        b'{"a":[null,true,1,"s",[],{}],"b":{"c":{"d":[1,{"e":false}]}}}\n'
    )


def test_unbounded_integers_are_not_truncated() -> None:
    big = 2**200 + 1
    assert canonical_json_bytes({"n": big}) == f'{{"n":{big}}}\n'.encode()


def test_tuple_and_list_both_serialize_as_arrays() -> None:
    assert canonical_json_bytes((1, 2, 3)) == canonical_json_bytes([1, 2, 3]) == b"[1,2,3]\n"
    assert canonical_json_bytes({"a": (1, "x")}) == b'{"a":[1,"x"]}\n'


def test_array_order_is_preserved_not_sorted() -> None:
    assert canonical_json_bytes([3, 1, 2]) == b"[3,1,2]\n"
    assert canonical_json_bytes(("z", "a")) == b'["z","a"]\n'


def test_nested_tuple_inside_mapping_inside_tuple() -> None:
    assert canonical_json_bytes(({"b": (1,)}, [2])) == b'[{"b":[1]},[2]]\n'


# --------------------------------------------------------------------------
# Key ordering, insertion-order independence, Unicode
# --------------------------------------------------------------------------


def test_object_keys_sorted_by_ascending_code_point() -> None:
    # Uppercase sorts before lowercase: this is direct code-point order, not
    # case-folded, not locale-aware.
    assert canonical_json_bytes({"b": 1, "A": 2, "a": 3, "B": 4}) == (
        b'{"A":2,"B":4,"a":3,"b":1}\n'
    )


def test_key_ordering_is_recursive() -> None:
    assert canonical_json_bytes({"z": {"y": 1, "x": 2}, "a": {"c": 3, "b": 4}}) == (
        b'{"a":{"b":4,"c":3},"z":{"x":2,"y":1}}\n'
    )


def test_key_ordering_is_not_case_folded() -> None:
    data = canonical_json_bytes({"apple": 1, "Apple": 2})
    assert data == b'{"Apple":2,"apple":1}\n'


def test_non_ascii_keys_sort_by_code_point() -> None:
    assert canonical_json_bytes({"é": 1, "z": 2, "a": 3}) == b'{"a":3,"z":2,"\xc3\xa9":1}\n'


def test_insertion_order_does_not_change_bytes() -> None:
    first = {"a": 1, "b": 2, "c": 3}
    second = {"c": 3, "b": 2, "a": 1}
    third = OrderedDict([("b", 2), ("a", 1), ("c", 3)])
    assert canonical_json_bytes(first) == canonical_json_bytes(second)
    assert canonical_json_bytes(first) == canonical_json_bytes(third)


def test_nested_insertion_order_does_not_change_bytes() -> None:
    first = {"outer": {"x": 1, "y": 2}}
    second = {"outer": OrderedDict([("y", 2), ("x", 1)])}
    assert canonical_json_bytes(first) == canonical_json_bytes(second)


def test_unicode_is_preserved_not_ascii_escaped() -> None:
    data = canonical_json_bytes({"k": "café ☕"})
    assert "café ☕".encode() in data
    assert b"\\u" not in data


def test_unicode_is_not_normalized() -> None:
    # U+00E9 and "e" + U+0301 are canonically equivalent under NFC but are
    # different code-point sequences; canonicalization must not merge them.
    precomposed = {"k": "é"}
    decomposed = {"k": "é"}
    assert canonical_json_bytes(precomposed) != canonical_json_bytes(decomposed)
    assert canonical_json_bytes(precomposed) == b'{"k":"\xc3\xa9"}\n'
    assert canonical_json_bytes(decomposed) == b'{"k":"e\xcc\x81"}\n'


def test_unicode_keys_are_not_normalized() -> None:
    assert canonical_json_bytes({"é": 1}) != canonical_json_bytes({"é": 1})


def test_control_characters_are_escaped_deterministically() -> None:
    assert canonical_json_bytes({"k": "a\nb\tc"}) == b'{"k":"a\\nb\\tc"}\n'


# --------------------------------------------------------------------------
# Determinism
# --------------------------------------------------------------------------


def test_repeated_runs_are_byte_identical() -> None:
    results = {canonical_json_bytes(GOLDEN_DOCUMENT) for _ in range(64)}
    assert len(results) == 1


def test_repeated_jsonl_runs_are_byte_identical() -> None:
    results = {canonical_jsonl_bytes(GOLDEN_RECORDS) for _ in range(64)}
    assert len(results) == 1


def test_equal_documents_built_differently_agree() -> None:
    built = dict.fromkeys(("zulu",))
    built["alpha"] = {"flag": True, "nested": [1, 2, 3]}
    built["Beta"] = "café ☕"
    built["delta"] = []
    built["echo"] = {}
    built["big"] = 12345678901234567890123456789
    built["neg"] = -42
    assert canonical_json_bytes(built) == GOLDEN_DOCUMENT_BYTES


def test_locale_environment_does_not_change_bytes(monkeypatch: pytest.MonkeyPatch) -> None:
    baseline = canonical_json_bytes(GOLDEN_DOCUMENT)
    for value in ("C", "tr_TR.UTF-8", "de_DE.UTF-8", "ja_JP.UTF-8"):
        monkeypatch.setenv("LC_ALL", value)
        monkeypatch.setenv("LANG", value)
        monkeypatch.setenv("LC_COLLATE", value)
        assert canonical_json_bytes(GOLDEN_DOCUMENT) == baseline


def test_timezone_environment_does_not_change_bytes(monkeypatch: pytest.MonkeyPatch) -> None:
    baseline = canonical_json_bytes(GOLDEN_DOCUMENT)
    for value in ("UTC", "Asia/Riyadh", "America/Los_Angeles", "Pacific/Kiritimati"):
        monkeypatch.setenv("TZ", value)
        assert canonical_json_bytes(GOLDEN_DOCUMENT) == baseline


def test_output_carries_no_runtime_or_environment_metadata() -> None:
    # The serializer must never inject provenance of its own. A legitimate
    # value may contain a slash — schema identifiers do — so assert on the
    # absence of metadata *keys*, not on incidental characters.
    document = dict(GOLDEN_DOCUMENT)
    document["schema"] = "mesc-pilot-01-example-registry/1"
    data = canonical_json_bytes(document) + canonical_jsonl_bytes(GOLDEN_RECORDS)
    lowered = data.lower()
    for key in (
        b"python_version",
        b"runtime",
        b"platform",
        b"hostname",
        b"host",
        b"username",
        b"user",
        b"cwd",
        b"path",
        b"date",
        b"timestamp",
        b"created_at",
        b"locale",
        b"timezone",
        b"environment",
        b"command",
        b"machine",
    ):
        assert key not in lowered
    # The legitimate slash-bearing value survives untouched.
    assert b"mesc-pilot-01-example-registry/1" in data
    # Output is exactly what the caller supplied, plus canonical structure.
    assert len(data) == len(canonical_json_bytes(document)) + len(
        canonical_jsonl_bytes(GOLDEN_RECORDS)
    )


# --------------------------------------------------------------------------
# Fail-closed rejection
# --------------------------------------------------------------------------


@pytest.mark.parametrize("value", [1.0, 0.0, -2.5, 1e300, float(1)])
def test_finite_floats_are_rejected(value: float) -> None:
    with pytest.raises(FloatingPointValueProhibitedError) as excinfo:
        canonical_json_bytes({"k": value})
    assert excinfo.value.code == "floating_point_value_prohibited"


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_nan_and_infinities_are_rejected(value: float) -> None:
    with pytest.raises(FloatingPointValueProhibitedError):
        canonical_json_bytes([value])


def test_float_nested_deeply_is_rejected() -> None:
    with pytest.raises(FloatingPointValueProhibitedError):
        canonical_json_bytes({"a": {"b": [{"c": [1.5]}]}})


@pytest.mark.parametrize("key", [1, 2.5, None, True, (1, 2)])
def test_non_string_object_keys_are_rejected(key: object) -> None:
    with pytest.raises(NonStringObjectKeyError) as excinfo:
        canonical_json_bytes({key: "v"})
    assert excinfo.value.code == "non_string_object_key"


def test_non_string_key_rejected_even_when_other_keys_are_strings() -> None:
    with pytest.raises(NonStringObjectKeyError):
        canonical_json_bytes({"good": 1, 2: "bad"})


@pytest.mark.parametrize(
    "value",
    [
        {1, 2},
        frozenset({1}),
        b"bytes",
        bytearray(b"bytes"),
        Path("/tmp/x"),
        pathlib.PurePosixPath("a/b"),
        Decimal("1.5"),
        Fraction(1, 2),
        _Colour.RED,
        object(),
        complex(1, 2),
        range(3),
        iter([1]),
    ],
)
def test_unsupported_types_are_rejected(value: object) -> None:
    with pytest.raises(UnsupportedValueTypeError) as excinfo:
        canonical_json_bytes({"k": value})
    assert excinfo.value.code == "unsupported_value_type"


def test_enum_is_rejected_but_its_extracted_primitive_is_accepted() -> None:
    with pytest.raises(UnsupportedValueTypeError):
        canonical_json_bytes({"k": _Colour.RED})
    assert canonical_json_bytes({"k": _Colour.RED.value}) == b'{"k":"red"}\n'


# --------------------------------------------------------------------------
# Exact primitive types: enums and subclasses are outside the closed domain
# --------------------------------------------------------------------------


@pytest.mark.parametrize("value", [_Colour.RED, _IntColour.RED, _StrColour.RED])
def test_every_enum_flavour_is_rejected_as_a_value(value: object) -> None:
    # IntEnum and StrEnum pass isinstance(int) / isinstance(str); only an exact
    # type check keeps them out of the closed canonical domain.
    with pytest.raises(UnsupportedValueTypeError) as excinfo:
        canonical_json_bytes({"k": value})
    assert excinfo.value.code == "unsupported_value_type"


@pytest.mark.parametrize("key", [_StrColour.RED, _MyStr("k"), _IntColour.RED])
def test_enum_and_str_subclass_keys_are_rejected(key: object) -> None:
    with pytest.raises(NonStringObjectKeyError) as excinfo:
        canonical_json_bytes({key: 1})
    assert excinfo.value.code == "non_string_object_key"


@pytest.mark.parametrize("value", [_MyInt(5), _MyStr("v")])
def test_primitive_subclasses_are_rejected_as_values(value: object) -> None:
    with pytest.raises(UnsupportedValueTypeError):
        canonical_json_bytes({"k": value})


def test_enums_are_never_silently_unwrapped() -> None:
    # A silent .value extraction would have produced these bytes; it must not.
    with pytest.raises(UnsupportedValueTypeError):
        canonical_json_bytes({"k": _IntColour.RED})
    with pytest.raises(UnsupportedValueTypeError):
        canonical_json_bytes({"k": _StrColour.RED})


def test_explicitly_extracted_exact_primitives_are_accepted() -> None:
    assert canonical_json_bytes({"k": int(_IntColour.RED)}) == b'{"k":1}\n'
    assert canonical_json_bytes({"k": str(_StrColour.RED)}) == b'{"k":"red"}\n'
    assert canonical_json_bytes({"k": _Colour.RED.value}) == b'{"k":"red"}\n'
    assert canonical_json_bytes({str(_StrColour.RED): 1}) == b'{"red":1}\n'
    assert canonical_json_bytes({"k": int(_MyInt(5))}) == b'{"k":5}\n'


def test_exact_bool_and_int_classification_is_preserved() -> None:
    assert canonical_json_bytes({"k": True}) == b'{"k":true}\n'
    assert canonical_json_bytes({"k": 1}) == b'{"k":1}\n'
    with pytest.raises(UnsupportedValueTypeError):
        canonical_json_bytes({"k": _MyInt(1)})


# --------------------------------------------------------------------------
# Single validated mapping snapshot
# --------------------------------------------------------------------------


def test_well_behaved_custom_mapping_is_supported() -> None:
    mapping = _PlainMapping({"b": 1, "a": {"d": 2, "c": 3}})
    assert canonical_json_bytes(mapping) == b'{"a":{"c":3,"d":2},"b":1}\n'


def test_custom_mapping_matches_the_equivalent_dict() -> None:
    data: dict[str, object] = {"z": 1, "a": [1, 2], "m": {"k": "v"}}
    assert canonical_json_bytes(_PlainMapping(data)) == canonical_json_bytes(data)


def test_mutating_mapping_cannot_inject_an_unvalidated_key() -> None:
    hostile = _InjectingMapping({"a": 1})
    with pytest.raises(NonStringObjectKeyError):
        canonical_json_bytes(hostile)
    # Exactly one iteration: the snapshot is taken once and validated once.
    assert hostile.iterations == 1


def test_injected_key_is_never_stringified() -> None:
    hostile = _InjectingMapping({"a": 1})
    try:
        data = canonical_json_bytes(hostile)
    except NonStringObjectKeyError:
        return
    raise AssertionError(f"non-string key was admitted: {data!r}")


def test_non_string_key_is_never_coerced_to_its_string_form() -> None:
    for key in (1, 2.5, None, True):
        with pytest.raises(NonStringObjectKeyError):
            canonical_json_bytes({key: "v"})
    # The coerced form would have been valid output; it must never appear.
    assert canonical_json_bytes({"1": "v"}) == b'{"1":"v"}\n'


def test_invalid_key_precedence_is_independent_of_insertion_order() -> None:
    forward: dict[object, object] = {"a": 1, 2: "x", 3: "y"}
    reverse: dict[object, object] = {3: "y", 2: "x", "a": 1}
    messages = set()
    for document in (forward, reverse):
        with pytest.raises(NonStringObjectKeyError) as excinfo:
            canonical_json_bytes(document)
        messages.add(str(excinfo.value))
    assert len(messages) == 1


def test_lone_surrogate_string_fails_closed() -> None:
    with pytest.raises(CanonicalizationFailureError) as excinfo:
        canonical_json_bytes({"k": "\ud800"})
    assert excinfo.value.code == "canonicalization_failure"


def test_lone_surrogate_key_fails_closed() -> None:
    with pytest.raises(CanonicalizationFailureError):
        canonical_json_bytes({"\udfff": 1})


def test_prohibited_values_are_not_silently_coerced() -> None:
    for value in (1.0, Decimal("1"), b"1"):
        with pytest.raises(CanonicalContractError):
            canonical_json_bytes({"k": value})


# --------------------------------------------------------------------------
# Boolean / integer distinction
# --------------------------------------------------------------------------


def test_booleans_and_integers_serialize_distinctly() -> None:
    assert canonical_json_bytes({"k": True}) == b'{"k":true}\n'
    assert canonical_json_bytes({"k": 1}) == b'{"k":1}\n'
    assert canonical_json_bytes({"k": False}) == b'{"k":false}\n'
    assert canonical_json_bytes({"k": 0}) == b'{"k":0}\n'


def test_boolean_and_integer_documents_do_not_collide() -> None:
    assert canonical_json_bytes({"k": True}) != canonical_json_bytes({"k": 1})
    assert canonical_sha256({"k": False}) != canonical_sha256({"k": 0})


# --------------------------------------------------------------------------
# Deterministic error precedence
# --------------------------------------------------------------------------


def test_non_string_key_precedes_float_in_the_same_object() -> None:
    with pytest.raises(NonStringObjectKeyError):
        canonical_json_bytes({"a": 1.5, 2: "x"})


def test_key_check_precedes_value_visit_regardless_of_insertion_order() -> None:
    forward = {"a": 1.5, 3: "x"}
    reverse = {3: "x", "a": 1.5}
    with pytest.raises(NonStringObjectKeyError):
        canonical_json_bytes(forward)
    with pytest.raises(NonStringObjectKeyError):
        canonical_json_bytes(reverse)


def test_values_are_visited_in_ascending_key_order_not_insertion_order() -> None:
    # "a" holds an unsupported type and "z" a float; ascending key order means
    # the unsupported type is always reported, whichever way the dict is built.
    forward = {"z": 1.5, "a": object()}
    reverse = {"a": object(), "z": 1.5}
    with pytest.raises(UnsupportedValueTypeError):
        canonical_json_bytes(forward)
    with pytest.raises(UnsupportedValueTypeError):
        canonical_json_bytes(reverse)


def test_multi_violation_precedence_is_stable_across_repeated_runs() -> None:
    document = {"z": 1.5, "m": {1: "bad"}, "a": object()}
    for _ in range(16):
        with pytest.raises(UnsupportedValueTypeError):
            canonical_json_bytes(dict(document))


def test_every_error_is_a_canonical_contract_error() -> None:
    for error in (
        UnsupportedValueTypeError,
        FloatingPointValueProhibitedError,
        NonStringObjectKeyError,
        CanonicalizationFailureError,
    ):
        assert issubclass(error, CanonicalContractError)
        assert not issubclass(error, SystemExit)


# --------------------------------------------------------------------------
# JSONL contract
# --------------------------------------------------------------------------


def test_zero_records_produce_zero_bytes() -> None:
    assert canonical_jsonl_bytes([]) == b""
    assert canonical_jsonl_bytes(iter([])) == b""
    assert len(canonical_jsonl_bytes(())) == 0


def test_one_object_per_line_with_final_line_feed() -> None:
    data = canonical_jsonl_bytes([{"a": 1}, {"b": 2}])
    assert data == b'{"a":1}\n{"b":2}\n'
    assert data.endswith(b"\n")
    assert data.count(b"\n") == 2


def test_jsonl_has_no_blank_lines() -> None:
    data = canonical_jsonl_bytes([{"a": 1}, {}, {"b": 2}])
    assert b"\n\n" not in data
    lines = data.split(b"\n")[:-1]
    assert all(line for line in lines)
    assert len(lines) == 3


def test_jsonl_preserves_caller_record_order() -> None:
    records = [{"n": 3}, {"n": 1}, {"n": 2}]
    assert canonical_jsonl_bytes(records) == b'{"n":3}\n{"n":1}\n{"n":2}\n'


def test_jsonl_canonicalizes_each_record_independently() -> None:
    assert canonical_jsonl_bytes([{"b": 1, "a": 2}]) == b'{"a":2,"b":1}\n'


def test_jsonl_accepts_a_generator_once() -> None:
    assert canonical_jsonl_bytes(record for record in ({"a": 1}, {"a": 2})) == (
        b'{"a":1}\n{"a":2}\n'
    )


@pytest.mark.parametrize("record", [1, "x", None, [1, 2], (1,), True, 1.5])
def test_jsonl_rejects_non_object_records(record: object) -> None:
    with pytest.raises(UnsupportedValueTypeError):
        canonical_jsonl_bytes([record])


def test_jsonl_prohibited_values_fail_closed() -> None:
    with pytest.raises(FloatingPointValueProhibitedError):
        canonical_jsonl_bytes([{"a": 1}, {"b": 2.5}])
    with pytest.raises(NonStringObjectKeyError):
        canonical_jsonl_bytes([{1: "x"}])


# --------------------------------------------------------------------------
# No side effects
# --------------------------------------------------------------------------


def test_no_filesystem_access(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("canonical serialization must not touch the filesystem")

    monkeypatch.setattr(builtins, "open", forbidden)
    monkeypatch.setattr(io, "open", forbidden)
    monkeypatch.setattr(os, "open", forbidden)
    monkeypatch.setattr(pathlib.Path, "open", forbidden)
    monkeypatch.setattr(pathlib.Path, "write_bytes", forbidden)
    monkeypatch.setattr(pathlib.Path, "write_text", forbidden)
    canonical_json_bytes(GOLDEN_DOCUMENT)
    canonical_jsonl_bytes(GOLDEN_RECORDS)
    canonical_sha256(GOLDEN_DOCUMENT)


def test_no_network_access(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("canonical serialization must not touch the network")

    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)
    canonical_json_bytes(GOLDEN_DOCUMENT)
    canonical_jsonl_bytes(GOLDEN_RECORDS)


def test_input_is_not_mutated() -> None:
    document = {"b": {"inner": [1, 2]}, "a": 1}
    snapshot = {"b": {"inner": [1, 2]}, "a": 1}
    canonical_json_bytes(document)
    assert document == snapshot
    assert list(document) == ["b", "a"]


def test_no_temporary_files_are_created(tmp_path: Path) -> None:
    before = set(tmp_path.iterdir())
    canonical_json_bytes(GOLDEN_DOCUMENT)
    canonical_jsonl_bytes(GOLDEN_RECORDS)
    assert set(tmp_path.iterdir()) == before


# --------------------------------------------------------------------------
# Boundary: nothing new is public
# --------------------------------------------------------------------------


def test_new_symbols_are_absent_from_the_public_facade() -> None:
    import medscale.mesc as mesc

    for name in (
        "canonical_json_bytes",
        "canonical_jsonl_bytes",
        "canonical_sha256",
        "sha256_of_bytes",
        "CanonicalJsonValue",
        "CanonicalContractError",
        "UnsupportedValueTypeError",
        "FloatingPointValueProhibitedError",
        "NonStringObjectKeyError",
        "CanonicalizationFailureError",
    ):
        assert name not in mesc.__all__
        assert not hasattr(mesc, name)


def test_facade_all_is_unchanged_by_this_increment() -> None:
    import medscale.mesc as mesc

    assert "SourceDocumentGroupedSplitter" in mesc.__all__
    assert not any(name.startswith("Canonical") for name in mesc.__all__)
    assert not any("canonical" in name for name in mesc.__all__)
    assert not any(name.startswith("_") for name in mesc.__all__)


def test_b1_serializer_is_not_used_and_is_unchanged() -> None:
    from medscale.mesc import _split_v1

    # B1 remains the compatibility contract: no terminal LF.
    assert _split_v1.canonical_json_bytes({"a": 1}) == b'{"a":1}'
    # B2A adds exactly one, and therefore cannot be B1's output.
    assert canonical_json_bytes({"a": 1}) == b'{"a":1}\n'
    assert canonical_json_bytes({"a": 1}) != _split_v1.canonical_json_bytes({"a": 1})
    # B1 admits a finite float; B2A must not.
    assert _split_v1.canonical_json_bytes({"a": 1.5}) == b'{"a":1.5}'
    with pytest.raises(FloatingPointValueProhibitedError):
        canonical_json_bytes({"a": 1.5})


def test_module_imports_only_the_standard_library_allowlist() -> None:
    import ast

    from medscale.mesc import _canonical_json_v1

    source = Path(_canonical_json_v1.__file__).read_text(encoding="utf-8")
    imported: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            imported.add(node.module.split(".")[0])
    assert imported <= {"__future__", "hashlib", "json", "collections", "typing", "types"}
    # No dataset, model, inference, retrieval, training, metrics or benchmark
    # dependency, and no B1 import at all.
    assert "medscale" not in imported
