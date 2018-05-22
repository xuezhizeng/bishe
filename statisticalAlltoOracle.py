import cx_Oracle
import pandas as pd
import dataoptions as dp
import numpy as np

conn = cx_Oracle.connect("star/star@127.0.0.1/orcl")
cursor = conn.cursor()  # 创建游标对象

database = 'city_job'


def process(x, job):
    if job == 'C/C++':
        job = 'c++'
    if job in x.工作名称 or job.upper() in x.工作名称 or job.capitalize() in x.工作名称 or job in x.职位描述 or job.upper() in x.职位描述 or job.capitalize() in x.职位描述:
        return True
    else:
        return False


def statisticalAlltoOracle():
    '''统计所有的城市职业信息，并返回dataframe
        这个函数应该是在爬虫爬去所有的数据之后，西安执行format格式化，然后执行这个函数
        执行完这个函数后应该将ddff保存到数据库cty_job中
        后续需要分析的话就直接读取数据库city_job中的数据就行了'''

    jobs = (
        'Java', 'C/C++', 'Python', 'C#', '区块链', 'Linux', '大数据', 'Web', '数据库', 'HTML5', '.NET', 'PHP', 'IOS',
        'Android', 'CSS', 'FPGA', '算法')
    conn = cx_Oracle.connect("star/star@127.0.0.1/orcl")
    sql = 'select * from info'
    df = pd.read_sql(sql=sql, con=conn)

    citys = tuple(set(df.工作地点))
    l = []
    # print(ddff)
    for city in citys:
        cityInfo = df[df.工作地点 == city]
        count = {}
        for job in jobs:
            # 统计一座城市的所有职位量
            # print(job)
            count[job] = len(
                cityInfo[cityInfo.apply(process, axis=1, args=([job]))])  # 是df的子集
        # print(count)  # 字典{job: num}
        l.append(count)
        # ddff = ddff.append(count, ignore_index=True)
        # ddff[city] = count
    ddff = pd.DataFrame(l, index=citys)
    ddff = ddff.T
    # print(ddff)
    # print(ddff)
    return ddff

df = statisticalAlltoOracle()
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