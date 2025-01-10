import unittest
import os
import sqlite3

class TestPipeline(unittest.TestCase):
    def setUp(self):
        """
        Set up before tests. Ensure the output directory exists.
        """
        self.output_dir = "./data"
        self.output_file = os.path.join(self.output_dir, "final_combined_quarterly_data.sqlite")
        self.pipeline_script = "./project/pipeline.sh"

    def test_pipeline_execution(self):
        """
        Test if the pipeline runs successfully.
        """
        # Run the pipeline
        result = os.system(self.pipeline_script)
        self.assertEqual(result, 0, "Pipeline did not execute successfully.")

    def test_output_file_exists(self):
        """
        Test if the output SQLite file is created.
        """
        self.assertTrue(os.path.exists(self.output_file), "Output file not found.")

    def test_output_file_validity(self):
        """
        Test if the SQLite output file can be opened and queried.
        """
        try:
            conn = sqlite3.connect(self.output_file)
            cursor = conn.cursor()
            # Test if a basic query works (e.g., checking for a table)
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            self.assertGreater(len(tables), 0, "No tables found in the SQLite file.")
            conn.close()
        except sqlite3.Error as e:
            self.fail(f"SQLite file is invalid: {e}")

if __name__ == "__main__":
    unittest.main()
