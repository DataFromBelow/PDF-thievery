import unittest
from unittest.mock import patch
import pdf_downloader_snake


class TestExcelLoading(unittest.TestCase):

    @patch("pdf_downloader_snake.pd.read_excel", side_effect=Exception())
    def test_excel_load_failure(self, mock_read_excel):
        with patch("builtins.print") as mock_print:
            pdf_downloader_snake.main()

            mock_print.assert_any_call("GODDAMNIT")
            mock_print.assert_any_call("test ended")


if __name__ == "__main__":
    unittest.main()