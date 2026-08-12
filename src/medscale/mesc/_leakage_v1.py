"""Private fixture-only leakage primitives for P01-04B2B (FD-B2B-1 .. FD-B2B-10).

Everything here is pure, deterministic and in-memory.  No function reads the
filesystem, the network, the environment, the clock, the locale, process state,
a registry, a cache, a logger or any global mutable state, and nothing here
enumerates record pairs, scans a dataset or orchestrates an audit: a caller
constructs explicit synthetic findings and this module validates them.

Two boundaries are load-bearing and deliberately asymmetric.

*Canonical bytes come only from B2A.*  ``medscale.mesc._canonical_json_v1``
is the accepted identity serializer: exact primitive domain, sorted object
members, UTF-8, compact separators, float rejection and exactly one terminal LF
*inside* the returned bytes.  The B1 serializer in ``medscale.mesc._split_v1``
emits no terminal LF and admits floats, so it is never used for identity here.
Canonical JSON is not reimplemented and identity bytes are never concatenated
by hand.

*The runtime float is never authoritative.*  ``score_representation`` is the
frozen canonical string bound into both the canonical finding document and the
finding-ID payload.  ``LeakageFinding.score`` is a derived caller convenience
that is excluded from canonical documents, canonical bytes, fingerprints,
identity, ordering and every threshold decision, all of which use exact integer
comparison.
"""

from __future__ import annotations

import math
import unicodedata
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import pairwise
from types import MappingProxyType
from typing import ClassVar, Final

from medscale.mesc._canonical_json_v1 import canonical_json_bytes, sha256_of_bytes
from medscale.mesc._split_v1 import PARTITIONS

#: Authorized finding schema identifier (FD-B2B-6).
FINDING_SCHEMA_VERSION: Final = "mesc-pilot-01-leakage-finding/1"

#: Authorized finding-ID prefix; the remainder is a 64-lowercase-hex SHA-256.
FINDING_ID_PREFIX: Final = f"{FINDING_SCHEMA_VERSION}:sha256:"

#: The enumerated finding-type domain adopted in the senior B2 contracts.
FINDING_TYPES: Final[tuple[str, ...]] = (
    "context_overlap",
    "empty_normalized_question",
    "exact_example",
    "exact_question",
    "near_duplicate_question",
    "normalized_question",
    "source_document",
)

#: The exactly three allowed classifications (FD-B2-6, FD-B2B-7).
CLASSIFICATIONS: Final[tuple[str, ...]] = (
    "confirmed_leakage",
    "false_positive",
    "unresolved",
)

#: Classifications that force ``leaked`` true (FD-B2B-7).
_LEAKED_CLASSIFICATIONS: Final = frozenset({"confirmed_leakage", "unresolved"})

#: The canonical partition domain, reused rather than restated so it cannot drift.
_CANONICAL_PARTITIONS: Final = frozenset(PARTITIONS)

#: The exact ``shared_surface`` marker allowlist (FD-B2B-8).  Any other string is
#: treated as raw surface text and rejected.
SHARED_SURFACE_MARKERS: Final[tuple[str, ...]] = (
    "context_bytes",
    "context_token_set",
    "empty_normalized_question",
    "example_id",
    "normalized_question",
    "question_bytes",
    "question_token_set",
    "source_document_id",
)

#: The detection-method allowlist: exactly the primitives this module implements.
DETECTION_METHODS: Final[tuple[str, ...]] = (
    "exact_context_equality",
    "exact_example_identity",
    "exact_question_equality",
    "exact_source_document_identity",
    "normalize_question",
    "normalized_question_equality",
    "token_set_jaccard",
    "tokenize",
)

#: ``score_representation`` for an exact method with no approximate score.
SCORE_REPRESENTATION_NONE: Final = "none"

#: ``score_representation`` when the empty-input policy prohibits a Jaccard score.
SCORE_REPRESENTATION_NOT_EVALUABLE: Final = "not_evaluable"

_JACCARD_PREFIX: Final = "jaccard:"

#: Thresholds are compared as exact integers: 100 * i >= <percent> * u.
NEAR_DUPLICATE_THRESHOLD_PERCENT: Final = 90
CONTEXT_OVERLAP_THRESHOLD_PERCENT: Final = 95
_PERCENT_SCALE: Final = 100

#: The fixed normalization pipeline recorded in every audit report (FD-B2B-4).
NORMALIZATION_RECORD: Final[Mapping[str, str]] = MappingProxyType(
    {
        "case_folding": "unicode_case_folding",
        "unicode_normalization": "NFKC",
        "whitespace_collapse": "unicode_whitespace_runs_to_single_ascii_space",
        "whitespace_trim": "strip_leading_and_trailing_whitespace",
    }
)

# ASCII-only digit and hex sets.  ``str.isdigit`` and ``int`` both accept
# non-ASCII decimal digits, which the unsigned base-10 ASCII rule forbids.
_ASCII_DIGITS: Final = frozenset("0123456789")
_LOWERCASE_HEX: Final = frozenset("0123456789abcdef")
_SHA256_HEX_LENGTH: Final = 64

# Prefixes and characters that betray a local filesystem path.  Evidence
# references must be stable identifiers, never local paths (senior B2 contracts).
_PATH_PREFIXES: Final = ("/", "./", "../", "~")


class LeakageContractError(Exception):
    """Base class for every private B2B fail-closed contract failure.

    These are library-internal failures.  They are deliberately not exported
    from ``medscale.mesc`` and never carry raw question, context or answer text,
    a path, a username, a hostname, an environment value or a timestamp.
    """

    code: ClassVar[str] = "leakage_contract_error"


class InvalidPrimitiveInputError(LeakageContractError):
    """An input outside the exact primitive domain (FD-B2B-2)."""

    code: ClassVar[str] = "invalid_primitive_input"


class InvalidFindingTypeError(LeakageContractError):
    """A finding type outside the enumerated domain."""

    code: ClassVar[str] = "invalid_finding_type"


class InvalidClassificationError(LeakageContractError):
    """A classification outside ``unresolved``/``false_positive``/``confirmed_leakage``."""

    code: ClassVar[str] = "invalid_classification"


class InvalidScoreError(LeakageContractError):
    """A malformed score representation, or a runtime score inconsistent with it."""

    code: ClassVar[str] = "invalid_score"


class InvalidEvidenceReferenceError(LeakageContractError):
    """A missing, empty or local-path supporting-evidence reference."""

    code: ClassVar[str] = "invalid_evidence_reference"


class SuppressionAttemptError(LeakageContractError):
    """An attempt to suppress, drop or omit a detected finding (FD-B2B-7)."""

    code: ClassVar[str] = "suppression_attempt"


class RawTextBearingValueError(LeakageContractError):
    """A promotable value carrying raw surface text (FD-B2B-8)."""

    code: ClassVar[str] = "raw_text_bearing_promotable_value"


class InvalidFindingIdentifierError(LeakageContractError):
    """A malformed identity array, a duplicate identity value, or a mismatched ID."""

    code: ClassVar[str] = "invalid_finding_identifier"


class InvalidReportInvariantError(LeakageContractError):
    """A report whose ordering, count or aggregate ``leaked`` value is inconsistent."""

    code: ClassVar[str] = "invalid_report_invariant"


# ---------------------------------------------------------------------------
# Exact input-domain helpers
# ---------------------------------------------------------------------------


def _require_text(value: object, field: str) -> str:
    """Return ``value`` as an exact ``str`` that encodes as valid UTF-8.

    ``type(...) is str`` rather than ``isinstance``: ``str`` subclasses and
    ``StrEnum`` members are outside the exact primitive domain and must not be
    silently accepted.  No coercion is ever attempted.
    """
    if type(value) is not str:
        raise InvalidPrimitiveInputError(f"{field} must be an exact str")
    _utf8(value, field)
    return value


def _require_identifier(value: object, field: str) -> str:
    """Return ``value`` as an exact non-empty ``str`` identifier."""
    text = _require_text(value, field)
    if not text:
        raise InvalidPrimitiveInputError(f"{field} must be non-empty")
    return text


def _utf8(text: str, field: str) -> bytes:
    """Return the UTF-8 bytes of ``text``, failing closed on lone surrogates."""
    try:
        return text.encode("utf-8")
    except UnicodeEncodeError as error:
        raise InvalidPrimitiveInputError(f"{field} is not encodable as valid UTF-8") from error


def _require_token_set(value: object, field: str) -> frozenset[str]:
    """Return ``value`` as an exact ``frozenset`` of exact non-empty ``str`` tokens.

    An exact ``frozenset`` is required rather than any set-like object so that no
    caller-owned mutable collection is ever read twice or retained.
    """
    if type(value) is not frozenset:
        raise InvalidPrimitiveInputError(f"{field} must be an exact frozenset")
    for token in sorted(value, key=repr):
        _require_identifier(token, f"{field} token")
    return value


# ---------------------------------------------------------------------------
# Exact equality primitives (FD-B2B-3)
# ---------------------------------------------------------------------------


def _exact_bytes_equal(left: str, right: str, field: str) -> bool:
    return _utf8(left, field) == _utf8(right, field)


def exact_example_identity(left: object, right: object) -> bool:
    """Return byte equality of two canonical ``example_id`` values."""
    return _exact_bytes_equal(
        _require_identifier(left, "example_id"),
        _require_identifier(right, "example_id"),
        "example_id",
    )


def exact_source_document_identity(left: object, right: object) -> bool:
    """Return byte equality of two canonical ``source_document_id`` values."""
    return _exact_bytes_equal(
        _require_identifier(left, "source_document_id"),
        _require_identifier(right, "source_document_id"),
        "source_document_id",
    )


def exact_question_equality(left: object, right: object) -> bool:
    """Return byte equality of two question strings.

    No normalization occurs here: case, Unicode normalization form, whitespace
    and punctuation differences all remain significant (FD-B2B-3).
    """
    return _exact_bytes_equal(
        _require_text(left, "question"),
        _require_text(right, "question"),
        "question",
    )


def exact_context_equality(left: object, right: object) -> bool:
    """Return byte equality of two context strings, with no normalization."""
    return _exact_bytes_equal(
        _require_text(left, "context"),
        _require_text(right, "context"),
        "context",
    )


# ---------------------------------------------------------------------------
# Normalization and tokenization (FD-B2B-4)
# ---------------------------------------------------------------------------


def normalize_question(value: object) -> str:
    """Return the normalized question, applying exactly the ratified pipeline.

    1. Unicode NFKC;
    2. Unicode case folding;
    3. every run of Unicode whitespace collapsed to one ASCII space;
    4. leading and trailing whitespace removed.

    ``str.split()`` with no separator splits on Unicode whitespace runs and
    discards leading and trailing runs, so steps 3 and 4 are exactly one join.
    No locale is consulted and no stemming, lemmatization, stop-word removal,
    transliteration or embedding is performed.
    """
    text = _require_text(value, "question")
    folded = unicodedata.normalize("NFKC", text).casefold()
    return " ".join(folded.split())


def tokenize(value: object) -> frozenset[str]:
    """Return the token set of an already-normalized string.

    Tokens are maximal consecutive Unicode alphanumeric runs; punctuation and
    whitespace are boundaries; empty tokens cannot arise; the result is a set and
    never a multiset.  ``str.isalnum`` is Unicode-aware and excludes ``_``, so an
    underscore is a boundary like any other non-alphanumeric character.
    """
    text = _require_text(value, "normalized_question")
    tokens: list[str] = []
    run: list[str] = []
    for character in text:
        if character.isalnum():
            run.append(character)
        elif run:
            tokens.append("".join(run))
            run.clear()
    if run:
        tokens.append("".join(run))
    return frozenset(tokens)


def question_token_set(value: object) -> frozenset[str]:
    """Return the token set of a raw question: normalize, then tokenize."""
    return tokenize(normalize_question(value))


def normalized_question_equality(left: object, right: object) -> bool:
    """Return equality of the two normalized question forms."""
    return normalize_question(left) == normalize_question(right)


def is_empty_normalized_question_pair(left: object, right: object) -> bool:
    """Return whether both questions normalize to the empty string.

    This is step 1 of the controlling evaluation order and is a *separate*
    condition from the token-set empty-input rules.  A punctuation-only or
    symbol-only question normalizes to a non-empty string, so such a pair is not
    an ``empty_normalized_question`` condition even though it tokenizes to two
    empty token sets; it is scored by the token-set rules and yields
    ``not_evaluable``.
    """
    return normalize_question(left) == "" and normalize_question(right) == ""


# ---------------------------------------------------------------------------
# Jaccard, empty-input precedence and the authoritative score representation
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TokenSetJaccard:
    """The complete, immutable outcome of one token-set comparison.

    The integer counts and ``score_representation`` are authoritative; ``score``
    is a derived convenience and is ``None`` whenever no fraction was
    constructed.  Both threshold decisions are recorded here so no caller has to
    re-derive them from a float.
    """

    intersection_size: int
    union_size: int
    score_representation: str
    score: float | None
    near_duplicate_threshold_passed: bool
    context_overlap_threshold_passed: bool

    @property
    def evaluable(self) -> bool:
        """Whether a Jaccard fraction was constructed for this comparison."""
        return self.score_representation != SCORE_REPRESENTATION_NOT_EVALUABLE


def _reduced_jaccard(intersection_size: int, union_size: int) -> str:
    """Return ``jaccard:<i>/<u>`` reduced by the greatest common divisor.

    Only reached with a strictly positive union.  ``gcd(0, u) == u`` reduces
    every zero-intersection case to the canonical ``jaccard:0/1``.
    """
    divisor = math.gcd(intersection_size, union_size)
    return f"{_JACCARD_PREFIX}{intersection_size // divisor}/{union_size // divisor}"


def token_set_jaccard(left: object, right: object) -> TokenSetJaccard:
    """Return the total token-set Jaccard outcome for two token sets.

    The evaluation order is controlling and the earlier applicable rule wins:

    1. normalized-question empty routing is a caller-level step performed before
       this function (see :func:`is_empty_normalized_question_pair`);
    2. token-set empty-input rules are authoritative exceptions;
    3. a Jaccard fraction is constructed **only** when both token sets are
       non-empty;
    4. thresholds are compared on the integer counts.

    Both-empty yields union zero; exactly-one-empty yields a positive union and
    is policy-defined non-evaluable under senior FD-B2-6 rather than
    mathematically undefined.  Neither constructs a fraction, so ``jaccard:0/0``
    can never be built and ``jaccard:0/1`` can never be emitted when either
    token set is empty.  Two non-empty disjoint sets are a different case
    entirely and are always ``jaccard:0/1`` with a runtime score of ``0.0``.
    """
    left_tokens = _require_token_set(left, "left token set")
    right_tokens = _require_token_set(right, "right token set")
    intersection_size = len(left_tokens & right_tokens)
    union_size = len(left_tokens | right_tokens)

    if not left_tokens or not right_tokens:
        return TokenSetJaccard(
            intersection_size=intersection_size,
            union_size=union_size,
            score_representation=SCORE_REPRESENTATION_NOT_EVALUABLE,
            score=None,
            near_duplicate_threshold_passed=False,
            context_overlap_threshold_passed=False,
        )

    scaled = _PERCENT_SCALE * intersection_size
    return TokenSetJaccard(
        intersection_size=intersection_size,
        union_size=union_size,
        score_representation=_reduced_jaccard(intersection_size, union_size),
        score=intersection_size / union_size,
        near_duplicate_threshold_passed=scaled >= NEAR_DUPLICATE_THRESHOLD_PERCENT * union_size,
        context_overlap_threshold_passed=scaled >= CONTEXT_OVERLAP_THRESHOLD_PERCENT * union_size,
    )


def _parse_unsigned_ascii_integer(text: str) -> int:
    """Return the value of an unsigned base-10 ASCII integer with no leading zero.

    ``int()`` is only reached after the exact character domain has been checked,
    so non-ASCII decimal digits, signs, underscores and whitespace can never be
    accepted.
    """
    if not text or not _ASCII_DIGITS.issuperset(text):
        raise InvalidScoreError("score representation digits must be unsigned base-10 ASCII")
    if len(text) > 1 and text[0] == "0":
        raise InvalidScoreError("score representation must not use a leading zero")
    return int(text)


def validate_score_representation(value: object) -> str:
    """Return ``value`` if it is one of the exactly three allowed forms.

    ``none``, ``not_evaluable``, or ``jaccard:<i>/<u>`` reduced by the greatest
    common divisor, with unsigned base-10 ASCII operands, no leading zero except
    the single digit ``0``, a strictly positive denominator and ``0 <= i <= u``.
    """
    text = _require_text(value, "score_representation")
    if text in (SCORE_REPRESENTATION_NONE, SCORE_REPRESENTATION_NOT_EVALUABLE):
        return text
    if not text.startswith(_JACCARD_PREFIX):
        raise InvalidScoreError("score representation is outside the allowed domain")
    fraction = text[len(_JACCARD_PREFIX) :]
    if fraction.count("/") != 1:
        raise InvalidScoreError("jaccard score representation must contain exactly one solidus")
    numerator_text, denominator_text = fraction.split("/")
    numerator = _parse_unsigned_ascii_integer(numerator_text)
    denominator = _parse_unsigned_ascii_integer(denominator_text)
    if denominator <= 0:
        raise InvalidScoreError("jaccard denominator must be strictly positive")
    if numerator > denominator:
        raise InvalidScoreError("jaccard numerator must not exceed its denominator")
    if math.gcd(numerator, denominator) != 1:
        raise InvalidScoreError("jaccard score representation must be reduced")
    return text


def _validate_runtime_score(value: object, score_representation: str) -> float | None:
    """Return the derived runtime score, or ``None``.

    The float is non-authoritative, so it may always be omitted; when it is
    present it must be an exact finite ``float`` that agrees with the
    authoritative integer counts.  NaN, the infinities, ints and bools all fail
    closed, and a float is never permitted alongside a non-evaluable comparison.
    """
    if value is None:
        return None
    if type(value) is not float:
        raise InvalidScoreError("runtime score must be an exact float or None")
    if not math.isfinite(value):
        raise InvalidScoreError("runtime score must be finite")
    if not score_representation.startswith(_JACCARD_PREFIX):
        raise InvalidScoreError("only a jaccard score representation may carry a runtime score")
    numerator_text, denominator_text = score_representation[len(_JACCARD_PREFIX) :].split("/")
    if value != int(numerator_text) / int(denominator_text):
        raise InvalidScoreError("runtime score must equal its authoritative integer fraction")
    return value


# ---------------------------------------------------------------------------
# Finding identity (FD-B2B-6)
# ---------------------------------------------------------------------------


def _validate_identity_values(
    value: object, field: str, allowed: frozenset[str] | None = None
) -> tuple[str, ...]:
    """Return the validated, canonically sorted unique values of one identity array.

    Order of operations is fixed: container type, element type, element content,
    membership, duplicate rejection, then sorting.  Sets are rejected outright
    because a caller-side set would have already collapsed duplicates, which is
    exactly the silent deduplication the contract forbids.  Duplicates are never
    removed; they fail closed.
    """
    if type(value) is not tuple and type(value) is not list:
        raise InvalidFindingIdentifierError(f"{field} must be an exact tuple or list")
    values = tuple(value)
    if not values:
        raise InvalidFindingIdentifierError(f"{field} must contain at least one value")
    texts = tuple(_require_identifier(item, f"{field} value") for item in values)
    if allowed is not None:
        for text in texts:
            if text not in allowed:
                raise InvalidFindingIdentifierError(f"{field} value is outside the allowed domain")
    if len(set(texts)) != len(texts):
        raise InvalidFindingIdentifierError(f"{field} must not contain a duplicate value")
    return tuple(sorted(texts))


def _validate_finding_type(value: object) -> str:
    text = _require_text(value, "finding_type")
    if text not in FINDING_TYPES:
        raise InvalidFindingTypeError("finding_type is outside the enumerated domain")
    return text


@dataclass(frozen=True, slots=True)
class _IdentityFields:
    """The five validated, canonically ordered identity inputs."""

    finding_type: str
    example_ids: tuple[str, ...]
    source_document_ids: tuple[str, ...]
    partitions: tuple[str, ...]
    score_representation: str


def _validate_identity(
    finding_type: object,
    example_ids: object,
    source_document_ids: object,
    partitions: object,
    score_representation: object,
) -> _IdentityFields:
    return _IdentityFields(
        finding_type=_validate_finding_type(finding_type),
        example_ids=_validate_identity_values(example_ids, "example_ids"),
        source_document_ids=_validate_identity_values(source_document_ids, "source_document_ids"),
        partitions=_validate_identity_values(partitions, "partitions", _CANONICAL_PARTITIONS),
        score_representation=validate_score_representation(score_representation),
    )


def _identity_document(fields: _IdentityFields) -> dict[str, object]:
    """Return the exact six-member identity object and nothing else.

    The accepted B2A serializer orders object members deterministically, so the
    member order written here is documentation of the adopted semantics; the
    arrays, by contrast, are already in canonical lexicographic order before
    serialization because array order is not normalized by any serializer.
    """
    return {
        "schema": FINDING_SCHEMA_VERSION,
        "finding_type": fields.finding_type,
        "example_ids": list(fields.example_ids),
        "source_document_ids": list(fields.source_document_ids),
        "partitions": list(fields.partitions),
        "score_representation": fields.score_representation,
    }


def finding_identity_document(
    finding_type: object,
    example_ids: object,
    source_document_ids: object,
    partitions: object,
    score_representation: object,
) -> dict[str, object]:
    """Return the validated six-member identity document for a finding."""
    return _identity_document(
        _validate_identity(
            finding_type, example_ids, source_document_ids, partitions, score_representation
        )
    )


def finding_identity_bytes(
    finding_type: object,
    example_ids: object,
    source_document_ids: object,
    partitions: object,
    score_representation: object,
) -> bytes:
    """Return ``FINDING_IDENTITY_BYTES``: the accepted B2A canonical serialization.

    The terminal LF supplied by the B2A serializer is inside these bytes and is
    therefore inside the SHA-256 input.
    """
    return canonical_json_bytes(
        finding_identity_document(
            finding_type, example_ids, source_document_ids, partitions, score_representation
        )
    )


def derive_finding_id(
    finding_type: object,
    example_ids: object,
    source_document_ids: object,
    partitions: object,
    score_representation: object,
) -> str:
    """Return the deterministic finding ID for the validated semantic fields."""
    digest = sha256_of_bytes(
        finding_identity_bytes(
            finding_type, example_ids, source_document_ids, partitions, score_representation
        )
    )
    return FINDING_ID_PREFIX + digest


def _validate_finding_id(value: object, expected: str) -> str:
    """Return ``value`` only if it regenerates exactly from the semantic fields.

    A caller-supplied identifier is never trusted: it is re-derived and compared.
    """
    text = _require_text(value, "finding_id")
    if not text.startswith(FINDING_ID_PREFIX):
        raise InvalidFindingIdentifierError("finding_id must carry the authorized prefix")
    digest = text[len(FINDING_ID_PREFIX) :]
    if len(digest) != _SHA256_HEX_LENGTH or not _LOWERCASE_HEX.issuperset(digest):
        raise InvalidFindingIdentifierError("finding_id digest must be 64 lowercase hex characters")
    if text != expected:
        raise InvalidFindingIdentifierError("finding_id does not match its regenerated value")
    return text


# ---------------------------------------------------------------------------
# Immutable findings (FD-B2B-7, FD-B2B-8)
# ---------------------------------------------------------------------------


def _validate_shared_surface(value: object) -> tuple[str, ...]:
    """Return the sorted unique shared-surface markers.

    Only the eight allowlisted semantic markers are admissible.  Any other
    string is, by construction, a copied substring, token value, question,
    context or answer fragment and is rejected as raw surface text.
    """
    if type(value) is not tuple and type(value) is not list:
        raise RawTextBearingValueError("shared_surface must be an exact tuple or list")
    texts: list[str] = []
    for marker in tuple(value):
        if type(marker) is not str:
            raise RawTextBearingValueError("shared_surface entries must be exact str markers")
        if marker not in SHARED_SURFACE_MARKERS:
            raise RawTextBearingValueError("shared_surface entry is not an allowlisted marker")
        texts.append(marker)
    if len(set(texts)) != len(texts):
        raise RawTextBearingValueError("shared_surface must not repeat a marker")
    return tuple(sorted(texts))


def _validate_classification(value: object) -> str:
    text = _require_text(value, "classification")
    if text not in CLASSIFICATIONS:
        raise InvalidClassificationError("classification is outside the allowed domain")
    return text


def _validate_evidence_reference(value: object, classification: str) -> str | None:
    """Return the supporting-evidence reference, enforcing the false-positive rule.

    ``false_positive`` requires a non-empty stable reference.  A local path is
    never a stable reference, so path-shaped values fail closed.
    """
    if value is None:
        if classification == "false_positive":
            raise InvalidEvidenceReferenceError(
                "false_positive requires a supporting-evidence reference"
            )
        return None
    text = _require_text(value, "evidence_reference")
    if not text or text.strip() != text:
        raise InvalidEvidenceReferenceError("evidence_reference must be a non-empty stable value")
    if "\\" in text or text.startswith(_PATH_PREFIXES):
        raise InvalidEvidenceReferenceError("evidence_reference must not be a local path")
    if len(text) > 2 and text[1] == ":" and text[0].isalpha():
        raise InvalidEvidenceReferenceError("evidence_reference must not be a local path")
    return text


def _validate_suppressed(value: object) -> bool:
    """Return ``False``; any other value is a suppression attempt."""
    if type(value) is not bool:
        raise SuppressionAttemptError("suppressed must be an exact bool")
    if value:
        raise SuppressionAttemptError("suppression is prohibited; suppressed must be false")
    return value


@dataclass(frozen=True, slots=True)
class LeakageFinding:
    """One immutable, fully validated leakage finding.

    Validation order is fixed so a value violating several rules always fails the
    same way: identity fields, runtime score, shared surface, classification,
    evidence reference, suppression, then the regenerated identifier.  Every
    caller-owned sequence is replaced by a tuple before validation completes, so
    no instance can be mutated through a collection the caller still holds.

    No raw question, context or answer text is stored, and the derived runtime
    ``score`` is deliberately absent from the canonical document.
    """

    finding_id: str
    finding_type: str
    example_ids: tuple[str, ...]
    source_document_ids: tuple[str, ...]
    partitions: tuple[str, ...]
    score_representation: str
    score: float | None
    shared_surface: tuple[str, ...]
    classification: str
    evidence_reference: str | None
    suppressed: bool = False

    def __post_init__(self) -> None:
        identity = _validate_identity(
            self.finding_type,
            self.example_ids,
            self.source_document_ids,
            self.partitions,
            self.score_representation,
        )
        object.__setattr__(self, "example_ids", identity.example_ids)
        object.__setattr__(self, "source_document_ids", identity.source_document_ids)
        object.__setattr__(self, "partitions", identity.partitions)
        object.__setattr__(
            self, "score", _validate_runtime_score(self.score, identity.score_representation)
        )
        object.__setattr__(self, "shared_surface", _validate_shared_surface(self.shared_surface))
        classification = _validate_classification(self.classification)
        object.__setattr__(
            self,
            "evidence_reference",
            _validate_evidence_reference(self.evidence_reference, classification),
        )
        object.__setattr__(self, "suppressed", _validate_suppressed(self.suppressed))
        expected = FINDING_ID_PREFIX + sha256_of_bytes(
            canonical_json_bytes(_identity_document(identity))
        )
        _validate_finding_id(self.finding_id, expected)

    @classmethod
    def create(
        cls,
        *,
        finding_type: object,
        example_ids: object,
        source_document_ids: object,
        partitions: object,
        score_representation: object,
        classification: object,
        score: object = None,
        shared_surface: object = (),
        evidence_reference: object = None,
    ) -> LeakageFinding:
        """Return a finding whose identifier is derived from its semantic fields.

        Caller ordering of the identity arrays is non-semantic: any permutation
        of the same unique values produces identical canonical arrays, identical
        identity bytes and an identical identifier.
        """
        identity = _validate_identity(
            finding_type, example_ids, source_document_ids, partitions, score_representation
        )
        # Narrow every remaining field here so the constructor is called with
        # exact types; ``__post_init__`` revalidates the same values, and both
        # paths therefore enforce one identical contract.
        classification_value = _validate_classification(classification)
        finding_id = FINDING_ID_PREFIX + sha256_of_bytes(
            canonical_json_bytes(_identity_document(identity))
        )
        return cls(
            finding_id=finding_id,
            finding_type=identity.finding_type,
            example_ids=identity.example_ids,
            source_document_ids=identity.source_document_ids,
            partitions=identity.partitions,
            score_representation=identity.score_representation,
            score=_validate_runtime_score(score, identity.score_representation),
            shared_surface=_validate_shared_surface(shared_surface),
            classification=classification_value,
            evidence_reference=_validate_evidence_reference(
                evidence_reference, classification_value
            ),
        )

    def identity_document(self) -> dict[str, object]:
        """Return this finding's exact six-member identity document."""
        return finding_identity_document(
            self.finding_type,
            self.example_ids,
            self.source_document_ids,
            self.partitions,
            self.score_representation,
        )

    def identity_bytes(self) -> bytes:
        """Return this finding's ``FINDING_IDENTITY_BYTES``."""
        return canonical_json_bytes(self.identity_document())

    def to_canonical_document(self) -> dict[str, object]:
        """Return the promotable canonical document.

        ``score_representation`` is authoritative here and is identical to the
        representation bound into the identity payload; the derived binary float
        is structurally absent rather than merely omitted by convention.
        """
        return {
            "classification": self.classification,
            "evidence_reference": self.evidence_reference,
            "example_ids": list(self.example_ids),
            "finding_id": self.finding_id,
            "finding_type": self.finding_type,
            "partitions": list(self.partitions),
            "schema": FINDING_SCHEMA_VERSION,
            "score_representation": self.score_representation,
            "shared_surface": list(self.shared_surface),
            "source_document_ids": list(self.source_document_ids),
            "suppressed": self.suppressed,
        }

    def to_canonical_bytes(self) -> bytes:
        """Return the canonical bytes of this finding's promotable document."""
        return canonical_json_bytes(self.to_canonical_document())


# ---------------------------------------------------------------------------
# Immutable audit report (FD-B2B-7)
# ---------------------------------------------------------------------------


def _validate_findings(value: object) -> tuple[LeakageFinding, ...]:
    """Return the findings tuple, requiring strictly ascending identifiers.

    Strict ascent enforces the ordering rule and rejects a repeated finding in
    one check; neither insertion order, hash iteration order nor caller order can
    influence the result.
    """
    if type(value) is not tuple and type(value) is not list:
        raise InvalidReportInvariantError("findings must be an exact tuple or list")
    findings = tuple(value)
    for finding in findings:
        if type(finding) is not LeakageFinding:
            raise InvalidReportInvariantError("every finding must be a LeakageFinding")
    identifiers = [finding.finding_id for finding in findings]
    if any(later <= earlier for earlier, later in pairwise(identifiers)):
        raise InvalidReportInvariantError(
            "findings must be sorted by strictly ascending finding_id"
        )
    return findings


def _validate_detection_methods(value: object) -> tuple[str, ...]:
    """Return the ordered detection-method list, preserving caller order."""
    if type(value) is not tuple and type(value) is not list:
        raise InvalidReportInvariantError("detection_methods must be an exact tuple or list")
    texts: list[str] = []
    for method in tuple(value):
        if type(method) is not str or method not in DETECTION_METHODS:
            raise InvalidReportInvariantError("detection_methods entry is outside the allowlist")
        texts.append(method)
    if len(set(texts)) != len(texts):
        raise InvalidReportInvariantError("detection_methods must not repeat a method")
    return tuple(texts)


@dataclass(frozen=True, slots=True)
class LeakageAuditReport:
    """One immutable, fully validated leakage audit report.

    Suppression is impossible by construction: a finding can only exist with
    ``suppressed`` false, and ``finding_count`` must equal the exact number of
    findings, so dropping, filtering or omitting a detected finding cannot be
    represented as a valid report.
    """

    findings: tuple[LeakageFinding, ...]
    leaked: bool
    finding_count: int
    detection_methods: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        findings = _validate_findings(self.findings)
        object.__setattr__(self, "findings", findings)
        object.__setattr__(
            self, "detection_methods", _validate_detection_methods(self.detection_methods)
        )
        # ``type(...) is int`` also rejects ``bool``, which Python makes an ``int``
        # subclass; a boolean count must never satisfy the invariant.
        if type(self.finding_count) is not int:
            raise InvalidReportInvariantError("finding_count must be an exact int")
        if self.finding_count != len(findings):
            raise InvalidReportInvariantError("finding_count must equal the number of findings")
        if type(self.leaked) is not bool:
            raise InvalidReportInvariantError("leaked must be an exact bool")
        if self.leaked != _aggregate_leaked(findings):
            raise InvalidReportInvariantError("leaked must be derived from the findings")

    @classmethod
    def create(cls, findings: object, detection_methods: object = ()) -> LeakageAuditReport:
        """Return a report with findings sorted and aggregates derived."""
        if type(findings) is not tuple and type(findings) is not list:
            raise InvalidReportInvariantError("findings must be an exact tuple or list")
        for finding in findings:
            if type(finding) is not LeakageFinding:
                raise InvalidReportInvariantError("every finding must be a LeakageFinding")
        ordered = tuple(sorted(findings, key=lambda item: item.finding_id))
        return cls(
            findings=ordered,
            leaked=_aggregate_leaked(ordered),
            finding_count=len(ordered),
            detection_methods=_validate_detection_methods(detection_methods),
        )

    def to_canonical_document(self) -> dict[str, object]:
        """Return the promotable canonical report document."""
        return {
            "detection_methods": list(self.detection_methods),
            "finding_count": self.finding_count,
            "findings": [finding.to_canonical_document() for finding in self.findings],
            "leaked": self.leaked,
            "normalization_record": dict(NORMALIZATION_RECORD),
        }

    def to_canonical_bytes(self) -> bytes:
        """Return the canonical bytes of this report's promotable document."""
        return canonical_json_bytes(self.to_canonical_document())


def _aggregate_leaked(findings: Sequence[LeakageFinding]) -> bool:
    """Return the fail-closed aggregate ``leaked`` value.

    True when at least one finding is unresolved or confirmed leakage; false only
    when no findings exist or every finding is a supported false positive.
    """
    return any(finding.classification in _LEAKED_CLASSIFICATIONS for finding in findings)
