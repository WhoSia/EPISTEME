"""W65 seven-edge manuscript-run provenance gate synthetic tests."""
import unittest
from p77_w65_provenance_gate import gate, EDGES


def claim(edge, **kwargs):
    c = {"edge": edge, "source_ref": "row-1", "target_ref": "row-2",
         "evidence_uri": "https://example.org/audit", "sha256": "a"*64,
         "join_key": "row-1:row-2", "evidence_kind": EDGES[edge], "reviewed": True}
    if edge != "source_to_input":
        c["run_id"] = "run-1"
    c.update(kwargs)
    return c


class ProvenanceGateTests(unittest.TestCase):
    def test_source_bytes_only_cannot_resolve_A08(self):
        r = gate([claim("source_to_input")])
        self.assertFalse(r["complete_single_run_attestation"])
        self.assertEqual(len(r["missing_edges"]), 6)

    def test_notebook_source_is_not_run_trace(self):
        with self.assertRaisesRegex(ValueError, "Evidence category"):
            gate([claim("input_to_invocation", evidence_kind="source_bytes")])

    def test_run_id_cannot_be_missing(self):
        with self.assertRaisesRegex(ValueError, "run_id"):
            gate([claim("output_to_query", run_id="")])

    def test_sha256_is_validated(self):
        with self.assertRaisesRegex(ValueError, "SHA256"):
            gate([claim("source_to_input", sha256="not-hash")])

    def test_all_same_run_edges_pass_schema_only(self):
        r = gate([claim(edge) for edge in EDGES])
        self.assertTrue(r["complete_single_run_attestation"])
        self.assertEqual(r["missing_edges"], [])

    def test_conflicting_runs_do_not_pass_single_run(self):
        records = [claim(edge) for edge in EDGES]
        records[-1]["run_id"] = "run-2"
        self.assertFalse(gate(records)["complete_single_run_attestation"])

    def test_review_and_join_required(self):
        with self.assertRaisesRegex(ValueError, "Unreviewed"):
            gate([claim("source_to_input", reviewed=False)])
        with self.assertRaisesRegex(ValueError, "join_key"):
            gate([claim("source_to_input", join_key="")])


if __name__ == "__main__":
    unittest.main()
