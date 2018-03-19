import cx_Oracle
import pandas as pd
import re
from oracleoptions import save_to_oracle

conn = cx_Oracle.connect("star/star@127.0.0.1/orcl")

sql = 'select * from zhaopin where rownum<=100'
sql = 'select * from zhaopin_city where rownum<=100'

# Index(['网址', '工作名称', '公司名称', '公司网址', '福利', '月工资', '发布日期', '经验', '人数', '工作地点',
#        '工作性质', '最低学历', '职位类别', '公司规模', '公司性质', '公司行业', '职位描述', '是否失效'])
df = pd.read_sql(sql=sql, con=conn)
conn.close()

# 筛选java从业职位
java = [d for d in df.工作名称 if 'JAVA' in d or 'Java' in d or 'java' in d]


def getCity(df):
    # 提取城市
    t = '北京-朝阳区'
    re.sub(r'-\S*$', '', t)
    for i in range(len(df)):
        df.iloc[i, 9] = re.sub(r'-\S*$', '', df.iloc[i, 9])

    # 已经失效的招聘信息就不要了
    return df[df.是否失效 == '否']


# print(df)


# df = getCity(df)
# 那下一次就直接从数据库里取zhaopin_city了
# save_to_oracle(df, "zhaopin_city")


# 统计工作地点信息
dict(df.工作地点.value_counts())


# 找出各职位的招聘信息条数
def jobNum(job):
    # 找出java职位数
    # len(list(filter(lambda s: 'JAVA' in s or 'Java' in s or 'java' in s, df.工作名称)))
    # re.I: 正则忽略大小写
    if 'c++' == job or 'C++' == job:
        job = 'c\+\+'
    elif 'c' == job or 'C' == job:
        job += '[^+#]'
    p = re.compile(job, re.I)
    return len(list(filter(lambda s: re.search(p, s), df.工作名称)))


jobs = ['java', 'c++', 'python', 'c#', 'c', 'linux', '大数据', 'web', '数据库']
# 这里应该要把含有上面职位的招聘信息拳头提取出来形成一个子集，而不是光统计一个数字
# num=pd.Series(data=[],index=jobs)
num = {}
for job in jobs:
    # print(job)
    num[job] = jobNum(job)


# 得找出具体职位的城市分布
# 这是一张三维图

# 找出各职位的具体招聘信息
def jobinfo(job):
    # re.I: 正则忽略大小写
    if 'c++' == job or 'C++' == job:
        job = 'c\+\+'
    elif 'c' == job or 'C' == job:
        job += '[^+#]'
    p = re.compile(job, re.I)
    # 创建一盒空的
    df_tmp = pd.DataFrame(columns=df.columns)
    # 忽略索引，往DataFrame中插入一行
    # df_tmp=df_tmp.append(df.loc[re.search(p,df.工作名称)], ignore_index=True)
    # 还是不理想，其余列都是NaN
    tmp = df.loc[filter(lambda s: re.search(p, s), df.工作名称)]
    return tmp


def process(x):
    if "JAVA" in x.工作名称 or "Java" in x.工作名称 or "java" in x.工作名称:
        return True
    else:
        return False
# 利用apply方法，已经可以提取出特定招聘信息的条目了
print(df[df.apply(process, axis=1)])
