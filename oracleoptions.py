#!/usr/bin/env python
# -*- coding:utf-8 -*-

import cx_Oracle
import pandas as pd

import log


# pd.set_option('large_repr', 'info')

def sqlSelect(sql, db):
    '''查询'''
    cr = db.cursor()
    cr.execute(sql)
    rs = cr.fetchall()
    cr.close()
    return rs


def sqlDML(sql, db, params=None):
    '''插入、更新、删除'''
    cr = db.cursor()
    if params:
        cr.execute(sql, params)
    else:
        cr.execute(sql)
    cr.close()
    db.commit()


def read_from_oracle(sql):
    conn = cx_Oracle.connect("star/star@127.0.0.1/orcl")
    # cursor = conn.cursor()  # 创建游标对象
    data = pd.read_sql(sql, conn)
    conn.close()
    return data


# 这是可用的版本,下面再测试一下添加日志进去
def save_to_oracle_v0(df, database=''):
    conn = cx_Oracle.connect("star/star@127.0.0.1/orcl")
    cursor = conn.cursor()  # 创建游标对象
    # cursor.execute('drop table {}'.format(database))

    columns = ["网址", "工作名称", "公司名称", "公司网址", "福利", "月工资", "发布日期", "经验", "人数", "工作地点", "工作性质", "最低学历", "职位类别", "公司规模",
               "公司性质", "公司行业", "职位描述", "是否失效"]

    # database = 'test'
    # df = pd.DataFrame(data=np.arange(36).reshape(2, 18), columns=columns)
    # df = pd.read_csv(r'e:\15970\Desktop\tmp3.csv',encoding='utf-8')
    try:  # 表是否存在
        cursor.execute('select count(*) from {}'.format(database))
    except cx_Oracle.DatabaseError:
        create = 'create table {} ({} VARCHAR(256), {} VARCHAR(256), {} VARCHAR(256), ' \
                 '{} VARCHAR(256), {} VARCHAR(1024), {} VARCHAR(256), {} VARCHAR(256), ' \
                 '{} VARCHAR(256), {} VARCHAR(256), {} VARCHAR(256), {} VARCHAR(256), ' \
                 '{} VARCHAR(256), {} VARCHAR(256), {} VARCHAR(256), {} VARCHAR(256),' \
                 '{} VARCHAR(256), {} VARCHAR(3889), {} VARCHAR(8))'.format(database, str(df.columns[0]),
                                                                            str(df.columns[
                                                                                1]),
                                                                            str(df.columns[2]), str(
                                                                                df.columns[3]),
                                                                            str(df.columns[4]), str(
                                                                                df.columns[5]),
                                                                            str(df.columns[6]), str(
                                                                                df.columns[7]),
                                                                            str(df.columns[8]), str(
                                                                                df.columns[9]),
                                                                            str(df.columns[10]), str(
                                                                                df.columns[11]),
                                                                            str(df.columns[12]), str(
                                                                                df.columns[13]),
                                                                            str(df.columns[14]), str(
                                                                                df.columns[15]),
                                                                            str(df.columns[16]), str(df.columns[17]))

        cursor.execute(create)  # 如果表不存在,创建呗

    columns = "({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}," \
              "{}, {})".format(str(df.columns[0]), str(df.columns[1]),
                               str(df.columns[2]), str(df.columns[3]),
                               str(df.columns[4]), str(df.columns[5]),
                               str(df.columns[6]), str(df.columns[7]),
                               str(df.columns[8]), str(df.columns[9]),
                               str(df.columns[10]), str(df.columns[11]),
                               str(df.columns[12]), str(df.columns[13]),
                               str(df.columns[14]), str(df.columns[15]),
                               str(df.columns[16]), str(df.columns[17]))

    insert = "insert into " + database + " " + columns + \
             " values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
    for i in range(len(df)):
        try:
            cursor.execute(insert % (df.iloc[i, 0], df.iloc[i, 1], df.iloc[i, 2], df.iloc[i, 3],
                                     df.iloc[i, 4], df.iloc[i, 5], df.iloc[
                                         i, 6], df.iloc[i, 7],
                                     df.iloc[i, 8], df.iloc[i, 9], df.iloc[
                                         i, 10], df.iloc[i, 11],
                                     df.iloc[i, 12], df.iloc[i, 13], df.iloc[
                                         i, 14], df.iloc[i, 15],
                                     df.iloc[i, 16], df.iloc[i, 17]))
        except [cx_Oracle.DatabaseError, UnicodeEncodeError] as e:
            print('写入失败')
            print('i=' + str(i))
            for j in range(len(df)):
                print(df.iloc[i, j])
        except UnicodeEncodeError:
            print(
                "'gbk' codec can't encode character xxx in position 173: illegal multibyte sequence")
            print('i=' + str(i))
            for j in range(len(df)):
                print(df.iloc[i, j])
    conn.commit()

    cursor.close()
    conn.close()


# 这个测试添加日志
def save_to_oracle_var(df, database=''):
    # 创建日志文件
    logger = log.log(file=database)
    conn = cx_Oracle.connect("star/star@127.0.0.1/orcl")
    cursor = conn.cursor()  # 创建游标对象
    # cursor.execute('drop table {}'.format(database))

    columns = ["网址", "工作名称", "公司名称", "公司网址", "福利", "月工资", "发布日期", "经验", "人数", "工作地点", "工作性质", "最低学历", "职位类别", "公司规模",
               "公司性质", "公司行业", "职位描述", "是否失效"]

    try:  # 表是否存在
        cursor.execute('select count(*) from {}'.format(database))
    except cx_Oracle.DatabaseError:
        create = 'create table {} ({} VARCHAR(256), {} VARCHAR(256), {} VARCHAR(256), ' \
                 '{} VARCHAR(256), {} VARCHAR(1024), {} VARCHAR(256), {} VARCHAR(256), ' \
                 '{} VARCHAR(256), {} VARCHAR(256), {} VARCHAR(256), {} VARCHAR(256), ' \
                 '{} VARCHAR(256), {} VARCHAR(256), {} VARCHAR(256), {} VARCHAR(256),' \
                 '{} VARCHAR(256), {} VARCHAR(3889), {} VARCHAR(8))'.format(database,
                                                                            str(df.columns[0]), str(
                                                                                df.columns[1]),
                                                                            str(df.columns[2]), str(
                                                                                df.columns[3]),
                                                                            str(df.columns[4]), str(
                                                                                df.columns[5]),
                                                                            str(df.columns[6]), str(
                                                                                df.columns[7]),
                                                                            str(df.columns[8]), str(
                                                                                df.columns[9]),
                                                                            str(df.columns[10]), str(
                                                                                df.columns[11]),
                                                                            str(df.columns[12]), str(
                                                                                df.columns[13]),
                                                                            str(df.columns[14]), str(
                                                                                df.columns[15]),
                                                                            str(df.columns[16]), str(df.columns[17]))

        cursor.execute(create)  # 如果表不存在,创建呗

    columns = "({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}," \
              "{}, {})".format(str(df.columns[0]), str(df.columns[1]),
                               str(df.columns[2]), str(df.columns[3]),
                               str(df.columns[4]), str(df.columns[5]),
                               str(df.columns[6]), str(df.columns[7]),
                               str(df.columns[8]), str(df.columns[9]),
                               str(df.columns[10]), str(df.columns[11]),
                               str(df.columns[12]), str(df.columns[13]),
                               str(df.columns[14]), str(df.columns[15]),
                               str(df.columns[16]), str(df.columns[17]))

    insert = "insert into " + database + " " + columns + \
             " values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
    for i in range(len(df)):
        try:
            cursor.execute(insert % (df.iloc[i, 0], df.iloc[i, 1], df.iloc[i, 2], df.iloc[i, 3],
                                     df.iloc[i, 4], df.iloc[i, 5], df.iloc[
                                         i, 6], df.iloc[i, 7],
                                     df.iloc[i, 8], df.iloc[i, 9], df.iloc[
                                         i, 10], df.iloc[i, 11],
                                     df.iloc[i, 12], df.iloc[i, 13], df.iloc[
                                         i, 14], df.iloc[i, 15],
                                     df.iloc[i, 16], df.iloc[i, 17]))
        except (cx_Oracle.DatabaseError, UnicodeEncodeError) as e:
            # 如果写数据库失败,这里会保存系统抛出的报错
            # 同时,也会保存导致出错的信息
            logger.saveInfo(e, df.iloc[i])
    conn.commit()

    cursor.close()
    conn.close()


def save_to_oracle_int(df, database=""):
    conn = cx_Oracle.connect("star/star@127.0.0.1/orcl")
    cursor = conn.cursor()  # 创建游标对象

    # database = 'city_job'

    # obj = dp.DataOptions()
    # df = obj.statisticalAlltoOracle()
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
        insert = insert + city + ", "  # 在这里面换行时会被添加进空格，导致`ORA-00917: 缺失逗号 Oracle`
    insert = insert[:-2] + ") values ("
    for job in index:
        insertSQL = insert
        for city in columns:
            insertSQL = insertSQL + str(df[city][job]) + ', '
        insertSQL = insertSQL[:-2] + ")"  # 把最后的', '两个字符去掉
        print(insertSQL)
        cursor.execute(insertSQL)
        conn.commit()

    cursor.close()
    conn.close()
