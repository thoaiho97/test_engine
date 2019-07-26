# Description
    # This script is used for automated test your project.
    # It will automatically execute your test and then insert it into the database.

# Usage
    # After downloading and extracting the file, please:
        # - Install Python 3.7 and MySQL if you have not installed.
        # - Open xx_tester\conf\database.ini and edit the properties accordings to your settings. If you run project on PyCharm, please change the shell = True.
        # - You can copy your project to xx_tester\input to test.
        # - Project folders have to 'test' folder.
    # Run the project:
        # - Open and run Command Prompt.
        # - Run command: 'pip install mysql-connector-python' (if you have not installed mysql connector).
        # - Run command: 'python' + your path of 'init.py'
            # Example my path: 'python D:\projects\xx-project\xx_tester\exec\venv\init.py'.
            # Script init.py only runs the first time.
        # - Run command: 'python' + your path of 'tester.py'
            # Example my path: 'python D:\projects\xx-project\xx_tester\exec\venv\tester.py'.

# Difficult
    # - Synchronize the file path and Python Interpreter path.
    # - Choose the method to execute the test cases.


import os
import configparser
import subprocess
import time
import sys

current_path_project = os.path.abspath(os.path.dirname(__file__))
os.chdir(current_path_project)

import database


# Get parameters from config file
config = configparser.ConfigParser()
config.read('../conf/database.ini')

user_mysql = config['MySQL']['user']
password_mysql = config['MySQL']['password']
database_name_mysql = config['MySQL']['database_name']

table_name_mysql_test = config['table']['table_test']
col_names_test = []
for key in config['column_names_test']:
    col_names_test.append(config['column_names_test'][key])

table_name_mysql_project = config['table']['table_project']
col_names_project = []
for key in config['column_names_project']:
    col_names_project.append(config['column_names_project'][key])

shell = config['parameter_shell']['shell']

# Connect to MySQL
conn_sql = database.connect_to_mysql(user=user_mysql, password=password_mysql, database_name=database_name_mysql)
cursor_sql = conn_sql.cursor()


try:

    now = time.strftime('%Y-%m-%d %H:%M:%S')
    project_file = ''
    if len(os.listdir('../input')) == 0: # If no project
        comment = "There is no project in this folder."
        data = [now, '', '', '', comment]
        database.insert_table_mysql(table_name=table_name_mysql_test, header=col_names_test, line=data, connection=conn_sql)
        print('input/')

    for project_file in os.listdir('../input'):  # Access project & test folders.
        list_test_error = []
        result_project = 'OK';
        try:

            now = time.strftime('%Y-%m-%d %H:%M:%S')
            if len(os.listdir('../input/' + project_file + '/test')) == 0:    # If no test script.
                comment = "There is no test file in this project."
                result_project = 'ERROR'
                data = [now, project_file, '', '', comment]
                data_project = [now, project_file, result_project, comment]
                database.insert_table_mysql(table_name=table_name_mysql_test, header=col_names_test, line=data, connection=conn_sql)
                database.insert_table_mysql(table_name=table_name_mysql_project, header=col_names_project, line=data_project, connection=conn_sql)

            for test_file in os.listdir('../input/' + project_file + '/test'):
                # Execute test case and get result
                now = time.strftime('%Y-%m-%d %H:%M:%S')
                print('/input/' + project_file + '/test/' + test_file)

                try:
                    p = subprocess.check_output([sys.executable, '../input/' + project_file + '/test/' + test_file], stderr=subprocess.STDOUT, shell=shell)

                    output = str(p)
                    output = output[1:]

                    if 'True' in output:
                        result = 'OK'
                        comment = ''
                    else:
                        list_test_error.append(test_file)
                        result = 'ERROR'
                        result_project = 'ERROR'
                        comment = output
                        if 'Traceack (most recent call last):' in output:
                            comment = 'Test file has error.'
                    data = [now, project_file, test_file, result, comment]
                    database.insert_table_mysql(table_name=table_name_mysql_test, header=col_names_test, line=data, connection=conn_sql)

                except Exception as err_test_case_error:
                    list_test_error.append(test_file)
                    result = 'ERROR'
                    result_project = 'ERROR'
                    comment = str(err_test_case_error)
                    data = [now, project_file, test_file, result, comment]
                    database.insert_table_mysql(table_name=table_name_mysql_test, header=col_names_test, line=data,
                                               connection=conn_sql)
            if len(list_test_error) != 0:
                comment = 'ERROR: '
                for error in list_test_error:
                    if error != list_test_error[len(list_test_error) - 1]:
                        comment += error + ', '
                    else:
                        comment += error + '.'

            data_project = [now, project_file, result_project, comment]
            database.insert_table_mysql(table_name=table_name_mysql_project, header=col_names_project, line=data_project, connection=conn_sql)

        except Exception as err_no_test_folder:
            comment = str(err_no_test_folder)
            data = [now, project_file, '', '', comment]
            result_project = 'ERROR'
            data_project = [now, project_file, result_project, comment]
            database.insert_table_mysql(table_name=table_name_mysql_project, header=col_names_project,
                                        line=data_project, connection=conn_sql)
            data = [now, project_file, '', '', comment]
            database.insert_table_mysql(table_name=table_name_mysql_test, header=col_names_test, line=data,
                                        connection=conn_sql)

except Exception as err_no_input_folder:
    comment = str(err_no_test_folder)
    data = [now, '', '', '', comment]
    database.insert_table_mysql(table_name=table_name_mysql_test, header=col_names_test, line=data, connection=conn_sql)


cursor_sql.close()
conn_sql.commit()
conn_sql.close()

