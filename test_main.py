import unittest
import pandas as pd
from main import clean_dataframe

class TestMain(unittest.TestCase):

    def test_clean_dataframe(self):
        raw_data = {
            "Âge": ["25", "30", ""],
            "Taille": ["185", "190", ""],
            "Poids": ["80", "85", ""],
            "Salaire": ["€10M", "€20K", "€100K"]
        }
        df = pd.DataFrame(raw_data)
        cleaned_df = clean_dataframe(df)

        expected_data = {
            "Âge": [25, 30],
            "Taille": [185, 190],
            "Poids": [80, 85],
            "Salaire": [10000000, 20000],
        }
        expected_df = pd.DataFrame(expected_data)

        try:
            pd.testing.assert_frame_equal(cleaned_df, expected_df)
            print("Test clean_dataframe : réussi")
            
        except AssertionError:
            print("Test clean_dataframe : échoué")
            raise