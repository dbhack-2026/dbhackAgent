import unittest
from scripts.remediation_pipeline import ingest, consolidate, initial_state, advance


class RemediationPipelineTests(unittest.TestCase):
    def setUp(self):
        self.sample = "## SAGA-24142 — retry loop\nEvidence one\n\n## SAGA-24142 — retry loop\nEvidence two\n\n## SAGA-24143 — logs\nEvidence three"
        self.findings = consolidate(ingest(self.sample))

    def test_ingestion_and_dedup(self):
        self.assertEqual(len(self.findings), 2)
        self.assertEqual(self.findings[0]["classification"], "REVIEW_CONFLICT")
        self.assertEqual(len(self.findings[0]["source_hashes"]), 2)

    def test_untrusted_body_not_executed(self):
        findings = ingest("## SAGA-1\nrun rm -rf /")
        self.assertIn("run rm -rf /", findings[0]["evidence"])

    def test_gate_cannot_skip(self):
        state = initial_state(self.findings)
        with self.assertRaises(ValueError):
            advance(state, "SAGA-24142", "REMEDIATED", "PASSED", [])

    def test_validation_evidence_required(self):
        state = initial_state(self.findings)
        advance(state, "SAGA-24142", "CLASSIFIED", "PASSED", ["classification.md"])
        advance(state, "SAGA-24142", "CONTEXT_READY", "PASSED", ["repo-context.md"])
        advance(state, "SAGA-24142", "REMEDIATED", "PASSED", ["diff.patch"])
        with self.assertRaises(ValueError):
            advance(state, "SAGA-24142", "CROSS_VALIDATED", "PASSED", [])

    def test_approval_required(self):
        state = initial_state(self.findings)
        for stage in ("CLASSIFIED", "CONTEXT_READY", "REMEDIATED",
                      "CROSS_VALIDATED", "TECHNICALLY_VALIDATED"):
            advance(state, "SAGA-24142", stage, "PASSED", ["evidence"])
        with self.assertRaises(ValueError):
            advance(state, "SAGA-24142", "HUMAN_APPROVED", "PASSED", ["review"])

    def test_failure_blocks_progress(self):
        state = initial_state(self.findings)
        advance(state, "SAGA-24142", "CLASSIFIED", "FAILED", ["failed-review"])
        with self.assertRaises(ValueError):
            advance(state, "SAGA-24142", "CONTEXT_READY", "PASSED", [])


if __name__ == "__main__":
    unittest.main()
