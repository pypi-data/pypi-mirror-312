# CSVFile-Convert Document

Welcome to **CSVFile-Convert**，a simple **.csv file converter**.

## Features
- Load some .csv files at the same time.
- Export .csv files without separator(Actually, with separator <code>\t</code>) </br>
  from .csv files with separator, such as <code>";"</code>, <code>","</code> and so on.

## Usage

There are some usages:

### Operate .csv Files
#### Step 1: Import

```python
from csv_convert.CSVFileHandler import CSVFileHandler
```
#### Step 2: Set File String
You can use a string to include the .csv files which will be processed, </br>
and separate each file with **a Python String**: <code>, </code>(a comma and a space).
```python
csv_file_str = 'test1.csv, test2.csv, test3.csv'
```
#### Step 3: Use The Handler To Operate The Information
Use <code>CSVFileHandler(csv_file_str: str, csv_file_delimiter: str)</code> 
to create a csv file handler.</br>

```python
csv_handler = CSVFileHandler(csv_file_str, ';')
csv_data_list = csv_handler.get_csv_file_list()
```
And then you can use the method: <code>get_csv_file_list()</code> 
to get the information of csv files defined in the 
<code>csv_file_str</code></br>
The method: <code>get_csv_file_list()</code> will return a <code>list</code>
whose element type is <code>pandas.DataFrame</code>.</br>

### Export .csv Files
You can use the method: <code>to_no_delimiter_csv()</code> to 
import the files defined by <code>csv_file_str</code>
to files with separator <code>\t</code>.
```python
handler.to_no_delimiter_csv()
```
