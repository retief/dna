import json
from unittest.mock import patch

from django.test import TestCase

from api import protein


class TestWithData(TestCase):
    def load_data(self):
        with open("api/test_data.json", "r") as data_file:
            self.data = json.load(data_file)


class TestContainsLocation(TestWithData):
    def setUp(self):
        self.load_data()

        feature_table = self.data[0]["GBSeq_feature-table"]

        # from: 378, end: 386
        self.feature1 = feature_table[3]
        # from: 1022, end: 276
        self.feature2 = feature_table[2]

    def test_returns_true_when_query_fully_contained(self):
        self.assertTrue(protein.contains_location(self.feature1, 379, 3))

    def test_returns_true_when_query_touches_start(self):
        self.assertTrue(protein.contains_location(self.feature1, 375, 4))

    def test_returns_true_when_query_touches_end(self):
        self.assertTrue(protein.contains_location(self.feature1, 386, 3))

    def test_returns_true_when_query_contains_feature(self):
        self.assertTrue(protein.contains_location(self.feature1, 375, 30))

    def test_returns_false_when_query_before_feature(self):
        self.assertFalse(protein.contains_location(self.feature1, 375, 3))

    def test_returns_false_when_query_after_feature(self):
        self.assertFalse(protein.contains_location(self.feature1, 387, 3))

    def test_returns_true_when_query_fully_contained_complement(self):
        self.assertTrue(protein.contains_location(self.feature2, 280, 3))

    def test_returns_true_when_query_touches_start_complement(self):
        self.assertTrue(protein.contains_location(self.feature2, 273, 4))

    def test_returns_true_when_query_touches_end_complement(self):
        self.assertTrue(protein.contains_location(self.feature2, 1022, 3))

    def test_returns_true_when_query_contains_feature_complement(self):
        self.assertTrue(protein.contains_location(self.feature2, 270, 1000))

    def test_returns_false_when_query_before_feature_complement(self):
        self.assertFalse(protein.contains_location(self.feature2, 273, 3))

    def test_returns_false_when_query_after_feature_complement(self):
        self.assertFalse(protein.contains_location(self.feature2, 1023, 3))


class TestGetProteinId(TestWithData):
    def setUp(self):
        self.load_data()

        feature_table = self.data[0]["GBSeq_feature-table"]

        self.quals1 = feature_table[2]["GBFeature_quals"]
        self.quals2 = feature_table[3]["GBFeature_quals"]

    def test_finds_protein_when_present(self):
        self.assertEqual(protein.get_protein_id(self.quals1), "YP_293755.1")

    def test_returns_none_when_no_id(self):
        self.assertIsNone(protein.get_protein_id(self.quals2))


class TestSearchProtein(TestWithData):
    def setUp(self):
        self.load_data()

    @patch("api.protein.fetch_protein_data")
    def test_finds_query_in_early_feature(self, fetch_protein_data):
        fetch_protein_data.return_value = self.data
        self.assertEqual(
            protein.search_protein("test", "catttctatc"),
            protein.ProteinMatch(
                location=281,
                feature_location="complement(276..1022)",
                protein_id="YP_293755.1",
            ),
        )
        fetch_protein_data.assert_called_once_with("test")

    @patch("api.protein.fetch_protein_data")
    def test_finds_query_in_later_feature(self, fetch_protein_data):
        fetch_protein_data.return_value = self.data
        self.assertEqual(
            protein.search_protein("test", "tgttgaaaca"),
            protein.ProteinMatch(
                location=1921,
                feature_location="1920..2537",
                protein_id="YP_293758.1",
            ),
        )
        fetch_protein_data.assert_called_once_with("test")

    @patch("api.protein.fetch_protein_data")
    def test_doesnt_find_nonexistent_query(self, fetch_protein_data):
        fetch_protein_data.return_value = self.data
        self.assertIsNone(protein.search_protein("test", "catttctatcatccattac"))
        fetch_protein_data.assert_called_once_with("test")
