import unittest
from unittest.mock import patch, Mock, mock_open
import pdf_downloader_snake
import pandas as pd

class TestPDFloading(unittest.TestCase):

    # --- Test 1: Excel loading (your first test) ---
    @patch("pdf_downloader_snake.pd.read_excel")
    def test_main_runs_with_valid_excel_data(self, mock_read_excel):

        df = pd.DataFrame({
            "BRnum": ["BR1"],
            "Pdf_URL": ["http://example.com/file.pdf"]
        })

        mock_read_excel.return_value = df
  
        pdf_downloader_snake.main()

    # --- Test 2: Simulate downloading a valid PDF ---
    @patch("pdf_downloader_snake.requests.get")
    @patch("pdf_downloader_snake.pd.read_excel")

    def test_download(self, mock_read_excel, mock_requests_get):

        df = pd.DataFrame({
            "BRnum": ["BR1"],
            "Pdf_URL": ["http://example.com/file.pdf"]
        })

        mock_read_excel.return_value = df
        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.headers = {"Content-Type": "application/pdf"}
        fake_response.content = b"%PDF fake content"
        mock_requests_get.return_value = fake_response

        pdf_downloader_snake.main()

     # --- Test 3: Checks if a PDF file is already on disk ---
    @patch("pdf_downloader_snake.requests.get")
    @patch("pdf_downloader_snake.os.path.exists")
    @patch("pdf_downloader_snake.pd.read_excel")
    def test_existing_file_is_not_overwritten(self, mock_read_excel, mock_exists, mock_requests_get):

        df = pd.DataFrame({
            "BRnum": ["BR_EXISTS"],
            "Pdf_URL": ["http://example.com/file.pdf"]
        })
        mock_read_excel.return_value = df
        mock_exists.return_value = True
        pdf_downloader_snake.main()
        mock_requests_get.assert_not_called()
    # --- Test 4: Checks whether a file downloaded is a pdf ---

    @patch("pdf_downloader_snake.requests.get")
    @patch("pdf_downloader_snake.pd.read_excel")
    def test_downloaded_content_is_valid_pdf(self, mock_read_excel, mock_requests_get):

        df = pd.DataFrame({
            "BRnum": ["BR_VALID"],
            "Pdf_URL": ["http://example.com/valid.pdf"]
        })
        mock_read_excel.return_value = df

        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.headers = {"Content-Type": "application/pdf"}
        fake_response.content = b"%PDF-1.4 fake but valid signature"
        mock_requests_get.return_value = fake_response

        with patch("builtins.open", mock_open()) as mock_file:
            pdf_downloader_snake.main()

            # Check that the content written to disk starts with %PDF
            written_content = mock_file().write.call_args[0][0]
            self.assertTrue(written_content.startswith(b"%PDF"),
                f"Expected content to start with %PDF but got: {written_content[:10]}")
    
    # --- Test 5: Checks whether the program will continue running after 403 --
    @patch("pdf_downloader_snake.requests.get")
    @patch("pdf_downloader_snake.pd.read_excel")
    def test_403_response(self, mock_read_excel, mock_requests_get):
        df = pd.DataFrame({
            "BRnum": ["BR_403"],
            "Pdf_URL": ["http://example.com/forbidden.pdf"]
        })
        mock_read_excel.return_value = df

        fake_response = Mock()
        fake_response.status_code = 403
        fake_response.headers = {"Content-Type": "text/html"}
        mock_requests_get.return_value = fake_response

        with patch("builtins.open", mock_open()) as mock_file:
            pdf_downloader_snake.main()

            mock_file.assert_not_called()


if __name__ == "__main__":
    unittest.main()
