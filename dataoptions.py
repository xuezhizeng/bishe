#!/usr/bin/env python
# -*- coding:utf-8 -*-
import cx_Oracle
import pandas as pd
import re


# from oracleoptions import save_to_oracle


class DataOptions(object):
    def __init__(self):
        '''初始化就是从数据库里读取数据'''
        try:
            conn = cx_Oracle.connect("star/star@127.0.0.1/orcl")
        except(cx_Oracle.DatabaseError, cx_Oracle.OperationalError) as e:
            print("读取数据库失败")
            print(e)
            exit(-1)
        sql = 'select * from zhaopin_city'

        # Index(['网址', '工作名称', '公司名称', '公司网址', '福利', '月工资', '发布日期', '经验', '人数', '工作地点',
        #        '工作性质', '最低学历', '职位类别', '公司规模', '公司性质', '公司行业', '职位描述', '是否失效'])
        self.df = pd.read_sql(sql=sql, con=conn)
        conn.close()
        # return df

    # 筛选java从业职位
    # java = [d for d in df.工作名称 if 'JAVA' in d or 'Java' in d or 'java' in d]

    def clearCity(self):
        '''提取城市'''
        # t = '北京-朝阳区'
        # re.sub(r'-\S*$', '', t)
        for i in range(len(self.df)):
            self.df.iloc[i, 9] = re.sub(r'-\S*$', '', self.df.iloc[i, 9])

        # 已经失效的招聘信息就不要了
        return self.df[self.df.是否失效 == '否']

    # print(df)

    # df = clearCity(df)
    # # 那下一次就直接从数据库里取zhaopin_city了
    # save_to_oracle(df, "zhaopin_city")

    def getJobInCity(self):
        '''统计职位数分布情况
            返回字典'''
        return dict(self.df.工作地点.value_counts())

    def getAllJobNum(self):
        '''找出各职位的招聘信息
            这个方法已经过时了，应该用下面的新的getJobsInfo'''
        def jobNum(df, job):
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
            num[job] = jobNum(self.df, job)

        return num


    # 得找出具体职位的城市分布
    # 这是一张三维图

    def jobinfo(self, job):
        '''找出各职位的具体招聘信息'''
        # re.I: 正则忽略大小写
        if 'c++' == job or 'C++' == job:
            job = 'c\+\+'
        elif 'c' == job or 'C' == job:
            job += '[^+#]'
        p = re.compile(job, re.I)
        # 创建一盒空的
        # df_tmp = pd.DataFrame(columns=self.df.columns)
        # 忽略索引，往DataFrame中插入一行
        # df_tmp=df_tmp.append(df.loc[re.search(p,df.工作名称)], ignore_index=True)
        # 还是不理想，其余列都是NaN
        return self.df.loc[filter(lambda s: re.search(p, s), self.df.工作名称)]


    def getJobsInfo(self, job):
        '''找出某职位的具体招聘信息
            返回的是df的一个子集'''
        def process(x, job):
            # "java"/"JAVA"/"Java"
            if job in x.工作名称 or job.upper() in x.工作名称 or job.capitalize() in x.工作名称:
                return True
            else:
                return False

        # 利用apply方法，已经可以提取出特定招聘信息的条目了
        return self.df[self.df.apply(process, axis=1, args=([job]))]

# df=getData()
# print(getJobInfo(df,'c#'))
