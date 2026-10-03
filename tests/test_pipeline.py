import unittest

from synthetic_rag_data.corpus import Passage
from synthetic_rag_data.generator import GeneratedQuery
from synthetic_rag_data.pipeline import generate_rows
from synthetic_rag_data.splits import assign


class FakeGenerator:
    model = "local-test"

    def generate(self, source_id, passage, mode, count):
        return [
            GeneratedQuery(
                query=f"How does retrieval work for {source_id} item {i}?",
                source_id=source_id,
                model=self.model,
                mode=mode,
                source_chars=len(passage),
            )
            for i in range(count)
        ]


class Tests(unittest.TestCase):
    def test_split_is_stable(self):
        self.assertEqual(assign("abc"), assign("abc"))

    def test_pipeline(self):
        rows = generate_rows(
            [Passage("d1", "Hybrid retrieval combines lexical and dense ranking.", {})],
            FakeGenerator(),
            ["direct", "paraphrase"],
            2,
        )
        self.assertEqual(len(rows), 4)
        self.assertTrue(all("difficulty" in row for row in rows))
        self.assertTrue(all(row["generator_model"] == "local-test" for row in rows))


if __name__ == "__main__":
    unittest.main()
