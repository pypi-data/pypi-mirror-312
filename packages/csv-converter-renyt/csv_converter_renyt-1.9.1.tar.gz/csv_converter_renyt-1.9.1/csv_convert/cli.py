import argparse

from csv_convert.CSVFileHandler import CSVFileHandler

def main():
    parser = argparse.ArgumentParser(
        description='Export .csv files without separator(Actually, with separator Tab)  from .csv files with separator, such as \", \". \n Usage:csv_convert -f "test1.csv,test2.csv,test3.csv" -s ";" '
    )

    parser.add_argument(
        '--files', '-f',
        type=str,
        required=True,
        help='CSV files to be converted, eg. "test1.csv,test2.csv,test3.csv"'
    )
    parser.add_argument(
        '--separator', '-s',
        type=str,
        default=';',
        help="The separator of data in origin csv file. Default is ';'"
    )

    args = parser.parse_args()

    csv_handler = CSVFileHandler(args.files, args.separator)
    print()

    csv_handler.to_no_delimiter_csv()


if __name__ == '__main__':
    main()