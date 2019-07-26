import mysql.connector
import sys
import time


def connect_to_mysql(user, password, database_name):
    try:
        con = mysql.connector.connect(
            host="localhost",
            user=user,
            passwd=password,
            auth_plugin='mysql_native_password',
            database=database_name
        )
    except Exception as e:
        f = open('../log/connection.log', 'a')
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        f.write(now + ':\n\t' + str(e) + '\n')
        f.close()
        print('Connection to the database failed. Please check connection.log file in xx_tester\\log.')
        sys.exit()
    return con


def drop_table_mysql(table_name, connection):
    cur_mysql = connection.cursor()
    sql_statement = 'drop table ' + table_name
    result = ''
    try:
        cur_mysql.execute(sql_statement)
        result = "Table is dropped."
    except mysql.connector.Error as e:
        result += "Error Drop message :" + e.msg

    return result


def create_table_mysql(table_name, header, connection):
    field = ''
    count = 0
    for row in header:
        if " " == row[0] or " " == row[len(row) - 1]:
            col_no_space = row.replace(" ", "")
        else:
            col_no_space = row.replace(" ", "_")
        count += 1
        if count == 1:
            field += col_no_space + ' int NOT NULL AUTO_INCREMENT PRIMARY KEY'
        else:
            field += col_no_space + ' char(255)'
        if row != header[len(header) - 1]:
            field += ', '

    sql_statement = 'create table ' + table_name + '(' + field + ')'
    result = ''

    cur_mysql = connection.cursor()
    try:
        cur_mysql.execute(sql_statement)
        result += "Table is created."
    except mysql.connector.Error as e:
        result += "Error Create message: " + e.msg
        print(result)
        sys.exit()
    return result


def insert_table_mysql(table_name, header, line, connection):

    col_ins = '('
    for row in header:
        if row == header[0]:
            continue
        if row != header[len(header) - 1]:
            col_ins += row + ', '
        else:
            col_ins += row + ')'

    # Create argument for Insert statement
    arg = ''
    for row in line:
        if row != line[len(line) - 1]:
            arg += '%s, '
        else:
            arg += '%s'
    cur_mysql = connection.cursor()
    try:
        cur_mysql.execute("INSERT INTO " + table_name + col_ins + " VALUES(" + arg + ")", line)
        print('1 row inserted.')
    except mysql.connector.Error as e:
        result = "Error Insert message: " + e.msg
        print(result)
        sys.exit()
