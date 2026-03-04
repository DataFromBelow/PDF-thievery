import unittest
# Imports Python's built-in testing framework.

from unittest.mock import patch, Mock
# Imports tools used for mocking:
# patch → temporarily replaces functions during tests
# Mock → creates fake objects (like fake HTTP responses)

import pdf_downloader_snake
# Imports the file we are testing so we can run functions inside it.

import pandas as pd
# Imports pandas so we can create fake DataFrames that simulate Excel data.



class TestPDFloading(unittest.TestCase):
# Defines a test class. unittest will automatically run any method
# that starts with "test_" inside this class.



    # --- Test 1: Excel loading (your first test) ---
    @patch("pdf_downloader_snake.pd.read_excel")
    # Temporarily replaces pd.read_excel inside pdf_downloader_snake
    # with a mock object while this test runs.

    def test_main_runs_with_valid_excel_data(self, mock_read_excel):
    # Defines the first test function.
    # mock_read_excel is the fake version of pd.read_excel created by patch.

        df = pd.DataFrame({
            "BRnum": ["BR1"],
            "Pdf_URL": ["http://example.com/file.pdf"]
        })
        # Creates a fake dataframe that looks like the Excel file.
        # This simulates one row from the Excel sheet.

        mock_read_excel.return_value = df
        # Tells the mock: whenever pd.read_excel() is called,
        # return this dataframe instead of reading a real Excel file.

        pdf_downloader_snake.main()
        # Runs the main program we are testing.
        # When the program calls pd.read_excel(), it will receive the fake dataframe.



    # --- Test 2: Simulate downloading a valid PDF ---
    @patch("pdf_downloader_snake.requests.get")
    # Temporarily replaces requests.get with a mock function
    # so the test does not perform real internet downloads.

    @patch("pdf_downloader_snake.pd.read_excel")
    # Again replaces pd.read_excel with a mock so we control the Excel data.

    def test_download(self, mock_read_excel, mock_requests_get):
    # Defines the second test.
    # mock_read_excel = fake pd.read_excel
    # mock_requests_get = fake requests.get

        df = pd.DataFrame({
            "BRnum": ["BR1"],
            "Pdf_URL": ["http://example.com/file.pdf"]
        })
        # Creates the same fake Excel data used in the first test.

        mock_read_excel.return_value = df
        # Makes pd.read_excel() return this fake dataframe.

        # Create fake HTTP response
        fake_response = Mock()
        # Creates a fake object that will behave like a requests response.

        fake_response.status_code = 200
        # Pretends the server responded successfully (HTTP 200).

        fake_response.headers = {"Content-Type": "application/pdf"}
        # Pretends the downloaded file is a PDF by setting the MIME type.

        fake_response.content = b"%PDF fake content"
        # Fake binary content representing a PDF file.

        mock_requests_get.return_value = fake_response
        # Tells requests.get() to return our fake response instead of
        # making a real network request.

        pdf_downloader_snake.main()
        # Runs the program again.
        # This time it believes:
        # - Excel returned one row
        # - the URL returned a valid PDF
        # So the program should execute the PDF download branch.

if __name__ == "__main__":
    unittest.main()
