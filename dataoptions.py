#!/usr/bin/env python
# -*- coding:utf-8 -*-
import cx_Oracle
import pandas as pd
import re
from functools import reduce
import collections
import oracleoptions as oracle


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
        sql = 'select * from info'

        # Index(['网址', '工作名称', '公司名称', '公司网址', '福利', '月工资', '发布日期', '经验', '人数', '工作地点',
        #        '工作性质', '最低学历', '职位类别', '公司规模', '公司性质', '公司行业', '职位描述', '是否失效'])
        self.df = pd.read_sql(sql=sql, con=conn)
        self.jobs = ['java', 'c++', 'python', 'c#',
                     'c', 'linux', '大数据', 'web', '数据库']
        conn.close()
        # self.format()
        # oracle.save_to_oracle(self.df, 'info')
        # return df

    # 筛选java从业职位
    # java = [d for d in df.工作名称 if 'JAVA' in d or 'Java' in d or 'java' in d]

    def format(self):
        '''提取城市'''
        # t = '北京-朝阳区'
        # re.sub(r'-\S*$', '', t)
        # 清除失效信息
        self.df = self.df[self.df.是否失效 == '否']

        for i in range(len(self.df)):
            # 规范城市
            self.df.iloc[i, 9] = re.sub(r'-\S*$', '', self.df.iloc[i, 9])
            # 规范月薪
            try:
                n1 = re.sub(r'-\S*$', '', self.df.iloc[i, 5])
                n2 = re.sub(r'^\S*-', '', self.df.iloc[i, 5])
                n2 = re.sub(r'元/月', '', n2)
                self.df.iloc[i, 5] = (int(n1) + int(n2)) / 2
            except ValueError:
                self.df.iloc[i, 5] = 0
                continue
            # 公司规模
            if re.findall(r'-', str(self.df.iloc[i, 13])):
                try:
                    n1 = re.sub(r'-\S*$', '', self.df.iloc[i, 13])
                    n2 = re.sub(r'^\S*-', '', self.df.iloc[i, 13])
                    n2 = re.sub(r'人', '', n2)
                    self.df.iloc[i, 13] = (int(n1) + int(n2)) / 2
                except ValueError as e:
                    self.df.iloc[i, 13] = 0
                    continue
            else:
                if re.findall(r'人', self.df.iloc[i, 13]):
                    self.df.iloc[i, 13] = int(
                        re.sub(r'人\S*$', '', self.df.iloc[i, 13]))
                else:
                    self.df.iloc[i, 13] = 0
                    continue

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
            # re.I: 正则忽略大小写
            if 'c++' == job or 'C++' == job:
                job = 'c\+\+'
            elif 'c' == job or 'C' == job:
                job += '[^+#]'
            p = re.compile(job, re.I)
            return len(list(filter(lambda s: re.search(p, s), df.工作名称)))

        num = {}
        for job in self.jobs:
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

    def getJobsInfo_v0(self, job):
        '''找出某职位的具体招聘信息
            返回的是df的一个子集'''

        # def process(x, job):
        #     # "java"/"JAVA"/"Java"
        #     if job in x.工作名称 or job.upper() in x.工作名称 or job.capitalize() in x.工作名称:
        #         return True
        #     else:
        #         return False

        # 利用apply方法，已经可以提取出特定招聘信息的条目了
        return self.df[self.df.apply(self.process, axis=1, args=([job]))]

    def process(self, x, job):
        if job in x.工作名称 or job.upper() in x.工作名称 or job.capitalize() in x.工作名称:
            return True
        else:
            return False

    def getJobsInfo(self, job):
        '''找出某职位的城市分布信息
            返回字典{city: num}'''
        jobinfo = self.df[self.df.apply(
            self.process, axis=1, args=([job]))]  # 是df的子集
        data = dict(collections.Counter(list(jobinfo.工作地点)))
        return dict(sorted(data.items(), key=lambda x: x[1], reverse=True)[:12]) # 返回字典{city: num}

    def getCityInfo(self, city):
        '''确定一个城市的职位统计
        :return:{job, num}'''
        data = self.df[self.df.工作地点 == city]
        jobs = ('Java', 'C/C++', 'Python', 'C#', '区块链',
                'Linux', '大数据', 'Web', '数据库', 'HTML5', '.NET')
        count = {}
        for job in jobs:
            count[job] = len(
                data[data.apply(self.process, axis=1, args=([job]))])  # 是df的子集
        return count  # 返回字典{job: num}

    def compress(self, value1, value2, flag):
        if flag == 0:  # 某个职位的城市分布信息
            d1 = self.getJobsInfo(value1)  # value1的具体招聘信息，是字典{city: num}
            d2 = self.getJobsInfo(value2)  # value2的具体招聘信息，是字典{city: num}
        else:  # 某个城市的职位信息统计
            d1 = self.getCityInfo(value1)  # value1的具体招聘信息，是字典{job: num}
            d2 = self.getCityInfo(value2)  # value2的具体招聘信息，是字典{job: num}
        data1 = dict(sorted(d1.items(), key=lambda x: x[1], reverse=True)[:12])  # 获取前12名
        data2 = dict(sorted(d2.items(), key=lambda x: x[1], reverse=True)[:12])
        # print(d1,'\n',d2,'\n',data1,'\n',data2)
        l2 = list(data2.keys())
        l1 = list(data1.keys())
        l = [v for v in l1 if v in l2]
        # print(l)
        data = {}
        for city in l:
            data[city] = (d1[city], d2[city])
        return data

    def jobRequest(self, job):
        '''
        统计职职位要求
        :return:
        '''
        jobNums = getAllJobNum()
        count = reduce(lambda x, y: x + y, jobNums.values())
        return jobNums[job] / count


# df=getData()
# print(getJobInfo(df,'c#'))
if __name__ == '__main__':
    d = DataOptions()
    # d.compress('java', 'c++')
    d.getCityInfo('北京')
# t=d.getJobsInfo('java')
# print(t)
# return t

# 1、某个城市的工作统计
# 2、某项工作的城市统计
