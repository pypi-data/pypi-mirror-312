import chardet
import pandas as pd

from .CONSTS import CMD_FILE_STR_SEPARATOR
from logging_utils.logger import Logger


class CSVFileHandler:
    def __init__(self, csv_file_list_str: str, csv_file_delimiter: str = ';') -> None:
        if not csv_file_list_str:
            raise ValueError('The csv_file_list_str cannot be empty')

        self.logger = Logger()
        self.logger.get_logger().info("Initializing CSVFileHandler.")

        self.__csv_file_str_list = csv_file_list_str.split(CMD_FILE_STR_SEPARATOR)
        self.__csv_file_delimiter = csv_file_delimiter
        self.__csv_file_list = self.__read_csv_file()
        self.__output_csv_file_str_list = self.__gen_output_csv_file_str_list()


    def __read_csv_file(self) -> list[pd.DataFrame]:
        print("----------------------------Reading CSV File-----------------------------------")
        csv_file_list = []
        for csv_file in self.__csv_file_str_list:
            try:
                with open(csv_file, 'rb') as f:
                    data = f.read()
                encoding = chardet.detect(data)['encoding']
                # 记录读取文件的信息
                self.logger.log_info(f"Attempting to read CSV file: {csv_file}")
                print(f"Attempting to read CSV file: {csv_file}")

                csv_file_list.append(
                    pd.read_csv(
                        csv_file,
                        delimiter=self.__csv_file_delimiter,
                        encoding=encoding,
                        engine='python',
                    )
                )
                print(f"Loaded CSV file:{csv_file}" )
                self.logger.log_info(f"Successfully read CSV file: {csv_file}")
            except FileNotFoundError:
                print(f"Can not read CSV file: {csv_file}, because it doesn't exist")
                self.logger.log_error(f"File {csv_file} is not found.")
            except pd.errors.EmptyDataError:
                print(f"Can not read CSV file: {csv_file}, because it is empty")
                self.logger.log_error(f"File {csv_file} is empty.")
            except Exception as e:
                self.logger.log_exception(e)
        print("--------------------------Finished reading CSV Files---------------------------")
        print("")
        return csv_file_list

    def __gen_output_csv_file_str_list(self) -> list:
        output_csv_file_str_list = []
        for csv_file_str in self.__csv_file_str_list:
            dot_index = csv_file_str.rfind('.')
            if dot_index == -1:
                output_csv_file_str_list.append(f'{csv_file_str}_out')
            else:
                output_csv_file_str_list.append(
                    f'{csv_file_str[:dot_index]}_out{csv_file_str[dot_index:]}'
                )
        return output_csv_file_str_list

    def to_no_delimiter_csv(self):
        print("---------------------------------Save Files------------------------------------")
        for origin_csv_file, output_csv_file_name in zip(
                self.__csv_file_list,
                self.__output_csv_file_str_list
        ):
            try:
                self.logger.log_info(f"Saving converted CSV to {output_csv_file_name}")
                print(f"Saving converted CSV to {output_csv_file_name}")
                origin_csv_file.to_csv(
                    output_csv_file_name,
                    sep="\t",
                    index=False,
                    encoding='utf-8'
                )
                print(f"Successfully save converted CSV to {output_csv_file_name}")
                self.logger.log_info(f"Successfully saved converted CSV to {output_csv_file_name}")
            except Exception as e:
                self.logger.log_exception(e)
        print("---------------------------------Saved Files-----------------------------------")

    def get_csv_file_list(self) -> list:
        return self.__csv_file_list

    def get_output_csv_file_str_list(self) -> list:
        return self.__output_csv_file_str_list
