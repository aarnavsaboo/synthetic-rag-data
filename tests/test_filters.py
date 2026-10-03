import unittest
from synthetic_rag_data.filters import deduplicate, normalize


class Tests(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize("Hello, WORLD!"), "hello world")

    def test_dedupe(self):
        rows = [
            {"query":"What is reciprocal rank fusion?"},
            {"query":"What is reciprocal-rank fusion?"},
        ]
        self.assertEqual(len(deduplicate(rows)), 1)


if __name__ == "__main__":
    unittest.main()
