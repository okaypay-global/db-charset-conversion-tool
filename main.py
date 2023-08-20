import argparse

import pymysql


def convert_database(
    host: str,
    user: str,
    password: str,
    database: str,
    source_charset: str,
    target_charset: str,
) -> None:
    # Connect to the database
    connection = pymysql.connect(
        host=host, user=user, password=password, database=database
    )
    cursor = connection.cursor()

    # Get all table names
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    # Process each table
    for table in tables:
        table_name = table[0]
        print(f"Converting table: {table_name}")

        # Get column names and column types
        cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
        columns = cursor.fetchall()

        # Process each column
        for column in columns:
            column_name = column[0]
            column_type = column[1].lower()
            print(f"  Converting column: {column_name}")

            # Check if the column type is a string type
            if any(
                x in column_type
                for x in ["char", "text", "enum", "set", "binary", "blob", "json"]
            ):
                # Convert column data
                sql = f"""UPDATE `{table_name}`
                          SET `{column_name}` = CONVERT(CAST(CONVERT(`{column_name}` USING {source_charset}) AS BINARY) USING {target_charset})
                          WHERE `{column_name}` IS NOT NULL AND `{column_name}` <> '';"""
                try:
                    cursor.execute(sql)
                except pymysql.err.OperationalError as e:
                    print(f"Error converting column {column_name}: {e}")
                except pymysql.err.InternalError as e:
                    print(f"Error converting column {column_name}: {e}")
                except pymysql.err.IntegrityError as e:
                    print(f"Error converting column {column_name}: {e}")

        # Commit changes
        connection.commit()

    # Close the connection
    cursor.close()
    connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a MySQL database between two character sets."
    )
    parser.add_argument(
        "--host", required=False, help="The database host.", default="localhost"
    )
    parser.add_argument(
        "--user", required=False, help="The database user.", default="root"
    )
    parser.add_argument("--password", required=True, help="The database password.")
    parser.add_argument("--database", required=True, help="The database name.")
    parser.add_argument(
        "--source_charset", required=True, help="The source character set."
    )
    parser.add_argument(
        "--target_charset", required=True, help="The target character set."
    )
    args = parser.parse_args()

    convert_database(
        args.host,
        args.user,
        args.password,
        args.database,
        args.source_charset,
        args.target_charset,
    )
