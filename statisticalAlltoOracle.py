import cx_Oracle
import pandas as pd
import dataoptions as dp
import numpy as np

conn = cx_Oracle.connect("star/star@127.0.0.1/orcl")
cursor = conn.cursor()  # 创建游标对象

database = 'city_job'

obj = dp.DataOptions()
df = obj.statisticalAlltoOracle()
columns = list(df.columns)  # ['北京', '深圳', '广州', '上海']
index = list(df.index)  # ['Linux', 'IOS', 'PHP']

try:  # 表是否存在
    cursor.execute('select count(*) from {}'.format(database))
except cx_Oracle.DatabaseError:
    print(database + '不存在')
    createSQL = 'create table ' + database + ' ( '
    for city in columns:
        createSQL = createSQL + city + '    int, '
    createSQL = createSQL[:-2] + ')'  # 去掉最后的', '，加上')'
    print(createSQL)
    cursor.execute(createSQL)  # 如果表不存在,创建呗
print(database + '存在')

insert = "insert into " + database + " ("
for city in columns:
    insert = insert + city + ", "   # 在这里面换行时会被添加进空格，导致`ORA-00917: 缺失逗号 Oracle`
insert = insert[:-2] + ") values ("
for job in index:
    insertSQL = insert
    for city in columns:
        insertSQL = insertSQL + str(df[city][job]) + ', '
    insertSQL = insertSQL[:-2] + ")"  # 把最后的', '两个字符去掉
    print(insertSQL)
    cursor.execute(insertSQL)
    conn.commit()