from django.test import TestCase

from api import genome


class TestContainsLocation(TestCase):
    @classmethod
    def setUpTestData(cls):
        feature_table = genome.fetch_genome_data("NC_007346")[0]["GBSeq_feature-table"]

        # from: 378, end: 386
        cls.feature1 = feature_table[3]
        # from: 1022, end: 276
        cls.feature2 = feature_table[2]

    def test_returns_true_when_query_fully_contained(self):
        self._assert_in(self.feature1, 379, 3)

    def test_returns_true_when_query_touches_start(self):
        self._assert_in(self.feature1, 375, 4)

    def test_returns_true_when_query_touches_end(self):
        self._assert_in(self.feature1, 386, 3)

    def test_returns_true_when_query_contains_feature(self):
        self._assert_in(self.feature1, 375, 30)

    def test_returns_false_when_query_before_feature(self):
        self._assert_not_in(self.feature1, 375, 3)

    def test_returns_false_when_query_after_feature(self):
        self._assert_not_in(self.feature1, 387, 3)

    def test_returns_true_when_query_fully_contained_complement(self):
        self._assert_in(self.feature2, 280, 3)

    def test_returns_true_when_query_touches_start_complement(self):
        self._assert_in(self.feature2, 273, 4)

    def test_returns_true_when_query_touches_end_complement(self):
        self._assert_in(self.feature2, 1022, 3)

    def test_returns_true_when_query_contains_feature_complement(self):
        self._assert_in(self.feature2, 270, 1000)

    def test_returns_false_when_query_before_feature_complement(self):
        self._assert_not_in(self.feature2, 273, 3)

    def test_returns_false_when_query_after_feature_complement(self):
        self._assert_not_in(self.feature2, 1023, 3)

    def _assert_in(self, feature, location, length):
        self.assertTrue(genome.contains_location(feature, location, length))

    def _assert_not_in(self, feature, location, length):
        self.assertFalse(genome.contains_location(feature, location, length))


class TestGetProteinId(TestCase):
    @classmethod
    def setUpTestData(cls):
        feature_table = genome.fetch_genome_data("NC_007346")[0]["GBSeq_feature-table"]

        cls.quals1 = feature_table[2]["GBFeature_quals"]
        cls.quals2 = feature_table[3]["GBFeature_quals"]

    def test_finds_protein_when_present(self):
        self.assertEqual(genome.get_protein_id(self.quals1), "YP_293755.1")

    def test_returns_none_when_no_id(self):
        self.assertIsNone(genome.get_protein_id(self.quals2))


class TestSearchGenome(TestCase):
    def test_finds_query_in_early_feature(self):
        self.assertEqual(
            genome.search_genome("NC_007346", "catttctatc"),
            genome.GenomeMatch(
                location=281,
                feature_location="complement(276..1022)",
                protein_id="YP_293755.1",
            ),
        )

    def test_finds_query_in_later_feature(self):
        self.assertEqual(
            genome.search_genome("NC_007346", "tgttgaaaca"),
            genome.GenomeMatch(
                location=1921,
                feature_location="1920..2537",
                protein_id="YP_293758.1",
            ),
        )

    def test_doesnt_find_nonexistent_query(self):
        self.assertIsNone(genome.search_genome("NC_007346", "catttctatcatccattac"))
