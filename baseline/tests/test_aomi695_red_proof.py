"""AOMI-695 proof: deliberately failing. Do not merge; PR will be closed."""
import unittest


class RedProof(unittest.TestCase):
    def test_deliberately_red(self) -> None:
        self.fail("AOMI-695 deliberate red check")
