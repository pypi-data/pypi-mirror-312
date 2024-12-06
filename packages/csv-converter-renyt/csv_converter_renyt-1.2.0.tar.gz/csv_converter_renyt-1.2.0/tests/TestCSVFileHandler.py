import unittest
import os
import pandas as pd
from csv_convert.CSVFileHandler import CSVFileHandler


class TestCSVFileHandler(unittest.TestCase):
    def test_csv_handler(self):
        str1 = "./test1.csv,./test2.csv,./test3.csv,./test4.csv"
        handle = CSVFileHandler(str1, ';')
        handle.to_no_delimiter_csv()


if __name__ == "__main__":
    unittest.main()
