# tests.py
import unittest
import os
import sqlite3

class TestSQLiteData(unittest.TestCase):
    def setUp(self):
        """
        Set up before tests. Ensure the SQLite file is accessible.
        """
        self.sqlite_file = os.path.abspath("data/final_dataset.sqlite")
        self.table_name = "final_combined_quarterly_data"

        if not os.path.exists(self.sqlite_file):
            self.fail(f"File does not exist: {self.sqlite_file}")
        elif not os.access(self.sqlite_file, os.R_OK):
            self.fail(f"File is not accessible for reading: {self.sqlite_file}")

    def test_columns_exist(self):
        """
        Test if all required columns exist in the table.
        """
        conn = sqlite3.connect(self.sqlite_file)
        cursor = conn.cursor()

        cursor.execute(f"PRAGMA table_info({self.table_name});")
        columns = cursor.fetchall()

        # Expected columns
        expected_columns = [
            'Quarter', 'CPIAUCSL', 'UNRATE', 'GDP', 'index', 'GDP_MIL', 'DEBT_MIL'
        ]
        column_names = [col[1] for col in columns]
        
        for column in expected_columns:
            self.assertIn(column, column_names, f"Column {column} is missing from the table.")

        conn.close()

    def test_valid_data_in_columns(self):
        """
        Test if data in columns are valid (e.g., numerical values where appropriate).
        """
        conn = sqlite3.connect(self.sqlite_file)
        cursor = conn.cursor()

        # get some rows from the table
        cursor.execute(f"SELECT * FROM {self.table_name} LIMIT 5;")
        rows = cursor.fetchall()

        for row in rows:
            # Check for numerical validity in relevant columns
            self.assertIsInstance(row[1], (int, float), "CPIAUCSL column contains invalid data.")
            self.assertIsInstance(row[2], (int, float), "UNRATE column contains invalid data.")
            self.assertIsInstance(row[3], (int, float), "GDP column contains invalid data.")
            self.assertIsInstance(row[5], (int, float), "GDP_MIL column contains invalid data.")
            self.assertIsInstance(row[6], (int, float), "DEBT_MIL column contains invalid data.")

        conn.close()

    def test_no_duplicate_entries(self):

        conn = sqlite3.connect(self.sqlite_file)
        cursor = conn.cursor()

        # Query to find any duplicate entries based on 'Quarter'
        cursor.execute(f"""
            SELECT Quarter, COUNT(*) 
            FROM {self.table_name}
            GROUP BY Quarter 
            HAVING COUNT(*) > 1;
        """)
        duplicates = cursor.fetchall()

        self.assertEqual(len(duplicates), 0, "There are duplicate entries in the table.")

        conn.close()

    def test_no_null_values(self):

        conn = sqlite3.connect(self.sqlite_file)
        cursor = conn.cursor()

        # Query to check for NULL values in critical columns
        cursor.execute(f"""
            SELECT COUNT(*) 
            FROM {self.table_name} 
            WHERE Quarter IS NULL OR CPIAUCSL IS NULL OR UNRATE IS NULL OR GDP IS NULL OR GDP_MIL IS NULL OR DEBT_MIL IS NULL;
        """)
        null_count = cursor.fetchone()[0]

        self.assertEqual(null_count, 0, "There are NULL values in the critical columns.")

        conn.close()

if __name__ == "__main__":
    unittest.main()
