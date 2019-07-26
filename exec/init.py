import os
import configparser

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

# Connect to MySQL
conn_sql = database.connect_to_mysql(user=user_mysql, password=password_mysql, database_name=database_name_mysql)
cursor_sql = conn_sql.cursor()

drop_table_test = database.drop_table_mysql(table_name=table_name_mysql_test, connection=conn_sql)
print(drop_table_test)

create_table_test = database.create_table_mysql(table_name=table_name_mysql_test, header=col_names_test, connection=conn_sql)
print(create_table_test)

drop_table_project = database.drop_table_mysql(table_name=table_name_mysql_project, connection=conn_sql)
print(drop_table_project)

create_table_test = database.create_table_mysql(table_name=table_name_mysql_project, header=col_names_project, connection=conn_sql)
print(create_table_test)
