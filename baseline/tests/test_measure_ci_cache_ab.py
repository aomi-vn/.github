import json
import subprocess
import sys
import unittest
from pathlib import Path

BASELINE = Path(__file__).resolve().parents[1]


class MeasureCiCacheAbTest(unittest.TestCase):
    def test_decision_remove_without_bench(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(BASELINE / "measure_ci_cache_ab.py"), "--json"],
            check=True,
            capture_output=True,
            text=True,
        )
        report = json.loads(proc.stdout)
        self.assertEqual(report["task"], "AOMI-736")
        self.assertFalse(report["keep_cache"])
        self.assertEqual(report["decision"], "remove_cache")


if __name__ == "__main__":
    unittest.main()
