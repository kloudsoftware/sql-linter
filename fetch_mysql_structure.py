#!/usr/bin/env python3

import pymysql
import os
import dis


def main():
    try:
        DB = os.environ["DB_NAME"]
        USER = os.environ["DB_USER"]
        PASSWORD = os.environ["DB_PASSWORD"]
        HOST = os.environ["DB_HOST"]
    except KeyError:
        print("Please set enviroment variables first")
        exit(3)

    for s in [DB, USER, PASSWORD, HOST]:
        if s is None:
            print("Please set enviroment variables first")
            exit(2)

    connection = pymysql.connect(host=HOST,
                             user=USER,
                             password=PASSWORD,
                             db=DB,
                             cursorclass=pymysql.cursors.DictCursor)

    found = []
    with connection.cursor() as cursor:
        sql = "select TABLE_NAME from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = '%s';" % DB
        cursor.execute(sql)
        tables = map(lambda t: t["TABLE_NAME"], cursor.fetchall())

        for table in tables:
            if not table in found:
                found.append(table)
            # Read a single record
            sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s';" % (DB, table)
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                col_name = row["COLUMN_NAME"]
                if not col_name in found:
                    found.append(col_name)

    with open("valid_identifiers", 'w+') as fd:
        fd.write('\n'.join(found))

if __name__ == '__main__':
    main()
