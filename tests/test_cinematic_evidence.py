import json
from pathlib import Path


def test_track3_cinematic_evidence_manifest_and_docs():
    repo_root = Path(__file__).resolve().parent.parent
    manifest_path = repo_root / "docs" / "evidence" / "cinematic_evidence_manifest.json"
    evidence_md = repo_root / "docs" / "evidence" / "CINEMATIC_EVIDENCE.md"
    thumbnail = repo_root / "docs" / "assets" / "cinematic-evidence-thumbnail.jpg"

    assert manifest_path.exists(), "Manifest must exist in repo docs/evidence"
    assert evidence_md.exists(), "CINEMATIC_EVIDENCE.md must exist"
    assert thumbnail.exists(), "Thumbnail must exist in docs/assets"
    assert thumbnail.stat().st_size > 10000, "Thumbnail must be valid image"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["evidence_type"] == "supplemental_pregenerated_cinematic_evidence"
    assert manifest["track_number"] == 3
    assert manifest["model"] == "veo-3.1-fast-generate-001"
    assert manifest["total_shots"] == 7
    assert manifest["total_duration_seconds"] == 56.03
    assert manifest["master_sha256"] == "c97dff90b83c3b868f01684a179fd5a8027d965789e5329a6e3c711465e6f2c7"
    assert "Supplemental pre-generated cinematic evidence" in manifest["truthful_disclaimer"]

    content = evidence_md.read_text(encoding="utf-8")
    assert "veo-3.1-fast-generate-001" in content
    assert "c97dff90b83c3b868f01684a179fd5a8027d965789e5329a6e3c711465e6f2c7" in content
    assert "Supplemental pre-generated cinematic evidence" in content
    assert "No Direct Causal Lineage to Parallel" in content
