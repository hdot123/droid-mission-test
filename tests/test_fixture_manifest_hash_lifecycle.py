"""Anti-regression guard: manifest sha256 keys must stay resolvable INSIDE
the repository.

Round-55 root cause: a test followed an attested sha256 record out of the
repo (a machine-local evidence tree) and turned the whole suite red in any
clean environment. This guard pins the manifest lifecycle so that pattern
cannot quietly return: for every ``sha256`` key in the ``validator-r*``
and ``worker-r*`` fixture manifests,

- entity vendored in-repo -> bytes must still match the attested digest
  (any single-byte drift fails here);
- entity absent from repo -> historical debt (the r53c pattern: digest
  attested, bytes never vendored) -> the key is skipped, never chased to a
  path outside the repo, and never fails a clean environment.

The glob is recursive because the r54A/C manifests live one level below
their fixture roots (``validator-r54ac/{a,c}/manifest.json``), unlike the
flat r52b/r53c layouts; the worker-r58d manifest follows the flat root
layout and its control-ok-missing sibling is nested two levels down.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).resolve().parent / "fixtures"
MANIFESTS = sorted(
    FIXTURES.glob("*-r*/**/manifest*.json"), key=lambda p: p.as_posix()
)


def _lifecycle_entries():
    """Yield (manifest, key, digest, entity) per sha256 key; entity is None
    when the key would resolve outside the fixture root."""
    for manifest_path in MANIFESTS:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for key, digest in sorted(manifest.get("sha256", {}).items()):
            entity = manifest_path.parent / key
            # containment before any stat/read: a key pointing outside the
            # fixture root must never turn into an out-of-repo read here.
            inside = entity.resolve().is_relative_to(FIXTURES.resolve())
            yield manifest_path, key, digest, entity if inside else None


def test_manifest_sha256_keys_stay_inside_the_repo():
    vendored = []
    debt = 0
    for manifest_path, key, digest, entity in _lifecycle_entries():
        if entity is None or not entity.is_file():
            debt += 1
            continue
        vendored.append((manifest_path, key, digest, entity))
    assert MANIFESTS, "no validator-r*/worker-r* manifests found under tests/fixtures/"
    if not vendored:
        pytest.skip(
            "r53c-style historical debt: manifests record sha256 digests but "
            f"no entity is vendored in-repo ({debt} keys); hash verification "
            "skipped, nothing read outside the repo, clean environment "
            "stays green"
        )
    vendored_worker_fixtures = 0
    for manifest_path, key, digest, entity in vendored:
        actual = hashlib.sha256(entity.read_bytes()).hexdigest()
        assert actual == digest, (
            f"{entity.relative_to(FIXTURES).as_posix()}: vendored bytes "
            f"diverge from {manifest_path.relative_to(FIXTURES).as_posix()} "
            f"sha256[{key!r}] attestation (expected {digest}, got {actual})"
        )
        if "worker-r" in manifest_path.as_posix():
            vendored_worker_fixtures += 1
    # the worker-r58d manifests must actually exercise the vendored path,
    # not silently join the debt bucket
    assert vendored_worker_fixtures >= 2, (
        "expected the worker-r58d manifest pair (verbatim + control) to "
        f"contribute vendored entities, found {vendored_worker_fixtures}"
    )
