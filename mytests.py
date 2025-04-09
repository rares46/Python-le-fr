import unittest
import sys
import os
import pandas as pd

#add parent directory for package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.data_ingestor import DataIngestor


class TestDataIngestor(unittest.TestCase):
    """test cases for the DataIngestor class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.csv_path = "./nutrition_activity_obesity_usa_subset.csv"
        self.data_ingestor = DataIngestor(self.csv_path)
        
    def test_california_vegetable_consumption_data(self):
        """test"""
        #parameters
        q = 'Percent of adults aged 18 years and older who have obesity'
        state = 'Ohio'
        year_start = 2019
        year_end = 2019
        
        #expected values from the dataset
        expected_values = [43.5, 40,1, 39.7, 36.5, 33.5, 21.8]
        
        # Manual filtering to get the results
        data = pd.DataFrame(self.data_ingestor.data_list)
        filtered_df = data[
            (data['Question'] == q) & 
            (data['LocationDesc'] == state) & 
            (data['YearStart'] == year_start) & 
            (data['YearEnd'] == year_end)
        ]
        actual_values = filtered_df['Data_Value'].tolist()
        
        # Verify the results match expected values
        self.assertEqual(actual_values, expected_values)


if __name__ == '__main__':
    unittest.main()
