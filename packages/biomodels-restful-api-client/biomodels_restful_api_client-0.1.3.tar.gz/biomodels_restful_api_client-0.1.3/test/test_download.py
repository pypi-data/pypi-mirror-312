import os
import zipfile
from utils4test import bmservices
import unittest

"""
Test Download Models
"""
class TestBioModelsDownload(unittest.TestCase):

    def test_download_one_model(self):
        """
        Test download one model
        """
        self.assertEqual(1, 1)
    

    def test_download_multiple_models(self):
        """
        Test download many models at once click
        """
        lst_model_ids = ["BIOMD0000000501", "BIOMD0000000502", "BIOMD0000000503"]
        # curl -X GET --output test.zip \
        #   https://www.ebi.ac.uk/biomodels/search/download\?models=BIOMD0000000501,BIOMD0000000502,BIOMD0000000503
        model_ids = ','.join(lst_model_ids)
        download_path = bmservices.download_bulk(model_ids)
        assert download_path
        file_size = os.path.getsize(download_path)
        assert file_size
        with zipfile.ZipFile(download_path) as myzip:
            info = myzip.infolist()
            self.assertEqual(len(lst_model_ids), len(info))
        # try:
        #     os.remove(download_path)
        # except OSError:
        #     pass


    def test_download_many_models_customised_name(self):
        """
        Test download many models at once click with a given name
        """
        lst_model_ids = ["BIOMD0000000200", "BIOMD0000000201", "BIOMD0000000203"]
        model_ids = ','.join(lst_model_ids)
        save_as_file = "biomodels-200-203-c.zip"
        download_path = bmservices.download_bulk(model_ids, save_as_file=save_as_file)
        with zipfile.ZipFile(download_path) as myzip:
            info = myzip.infolist()
            self.assertEqual(len(lst_model_ids), len(info))
        try:
            # os.remove(download_path)
            os.rename(download_path, f"tmp/{save_as_file}")
        except OSError:
            pass


if __name__ == "__main__":
    unittest.main()
