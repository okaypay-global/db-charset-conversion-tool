# Database Charset Conversion Tool

This script is a tool to convert all the columns of all the tables in a MySQL database from GBK to utf8mb4
character set. This can be useful if your data was initially inserted using the wrong character set and needs to be
converted to utf8mb4 for better Unicode support.

## Requirements

- Python 3.x
- pymysql

## Installation

### Using venv

1. Create a virtual environment:
    ```shell
    python -m venv venv
    ```
2. Activate the virtual environment:
    * On Windows:
       ```shell
       venv\Scripts\activate.bat
       ```
    * On Unix or MacOS:
        ```shell
       source venv/bin/activate
       ```
3. Install the dependencies:
    ```shell
    pip install -r requirements.txt
    ```

### Using conda

1. Create a conda environment:
    ```shell
    conda create -n db-charset-conversion-tool python=3.10
    ```
2. Activate the conda environment:
    ```shell
    conda activate db-charset-conversion-tool
    ```
3. Install the dependencies:
    ```shell
    pip install -r requirements.txt
    ```

## Usage

1. Make sure you have completed step 2 from the original instructions, updating the database and table charset to utf8mb4.
2. Run the script and pass the required arguments:
    ```shell
    python main.py --host your_host --user your_username --password your_password --database your_database_name
    ```
3. Follow the console output to track the progress of the conversion.

## Caution

Make sure to backup your database before running this script and verify its functionality in a test environment before applying it to a production database.

## License

This script is provided as-is under the MIT License. Use at your own risk.
