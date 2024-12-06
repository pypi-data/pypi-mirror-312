import argparse

from csv_convert.CSVFileHandler import CSVFileHandler

def main():
    parser = argparse.ArgumentParser(
        description='Export .csv files without separator(Actually, with separator Tab)  from .csv files with separator, such as \", \".'
    )

    parser.add_argument(
        '--files', '-f',
        type=str,
        required=True,
        help='CSV files to be converted'
    )
    parser.add_argument(
        '--separator', '-s',
        type=str,
        default=';',
        help="The separator of data in origin csv file. Default is ';'"
    )

    args = parser.parse_args()

    print("---------------------------------------------------------------")
    print("Start to read the csv files: ")
    print(args.files)
    print("---------------------------------------------------------------")
    csv_handler = CSVFileHandler(args.files, args.separator)
    print()

    print("---------------------------------------------------------------")
    print("Start to output the csv files: ")
    print("---------------------------------------------------------------")
    csv_handler.to_no_delimiter_csv()
    print()

    print("---------------------------------------------------------------")
    print("The files have been converted successfully and been written to")
    print(csv_handler.get_output_csv_file_str_list())
    print("---------------------------------------------------------------")
    print()


if __name__ == '__main__':
    main()