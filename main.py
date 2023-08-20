import pymysql
import argparse


def convert_database(host: str, user: str, password: str, database: str) -> None:
    # 连接到数据库
    connection = pymysql.connect(
        host=host, user=user, password=password, database=database
    )
    cursor = connection.cursor()

    # 获取所有表名
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    # 对每一个表进行操作
    for table in tables:
        table_name = table[0]
        print(f"Converting table: {table_name}")

        # 获取列名
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = cursor.fetchall()

        # 对每一个列进行操作
        for column in columns:
            column_name = column[0]
            print(f"  Converting column: {column_name}")

            # 转换列数据
            sql = f"""UPDATE {table_name}
                      SET {column_name} = CONVERT(CAST(CONVERT({column_name} USING gbk) AS BINARY) USING utf8mb4)
                      WHERE {column_name} IS NOT NULL AND {column_name} <> '';"""
            cursor.execute(sql)

        # 提交更改
        connection.commit()

    # 关闭连接
    cursor.close()
    connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a MySQL database from GBK to utf8mb4."
    )
    parser.add_argument("--host", required=True, help="The database host.")
    parser.add_argument("--user", required=True, help="The database user.")
    parser.add_argument("--password", required=True, help="The database password.")
    parser.add_argument("--database", required=True, help="The database name.")
    args = parser.parse_args()

    convert_database(args.host, args.user, args.password, args.database)
