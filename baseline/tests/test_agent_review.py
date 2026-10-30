import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent_review import parse_verdict


class ParseVerdictTest(unittest.TestCase):
    def test_valid_verdict(self) -> None:
        self.assertEqual(parse_verdict('{"verdict": "APPROVE", "summary": "ok", "findings": []}'), {"verdict": "APPROVE", "summary": "ok", "findings": []})

    def test_malformed_json(self) -> None:
        self.assertIsNone(parse_verdict('{"verdict": "APPROVE" "summary": "x"}'))

    def test_unknown_verdict(self) -> None:
        self.assertIsNone(parse_verdict('{"verdict": "MAYBE"}'))

    def test_non_object(self) -> None:
        self.assertIsNone(parse_verdict('["APPROVE"]'))


if __name__ == "__main__":
    unittest.main()
