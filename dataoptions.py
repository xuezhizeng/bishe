#!/usr/bin/env python
# -*- coding:utf-8 -*-
import cx_Oracle
import pandas as pd
import re
from functools import reduce
import collections
import oracleoptions as oracle
import log


# from oracleoptions import save_to_oracle


class DataOptions(object):

    def __init__(self):
        '''初始化就是从数据库里读取数据'''
        try:
            conn = cx_Oracle.connect("star/star@127.0.0.1/orcl")
        except(cx_Oracle.DatabaseError, cx_Oracle.OperationalError) as e:
            exit(-1)
        sql = 'select * from info'

        # Index(['网址', '工作名称', '公司名称', '公司网址', '福利', '月工资', '发布日期', '经验', '人数', '工作地点',
        #        '工作性质', '最低学历', '职位类别', '公司规模', '公司性质', '公司行业', '职位描述', '是否失效'])
        self.df = pd.read_sql(sql=sql, con=conn)
        # self.jobs = ['java', 'c++', 'python', 'c#',
        #              'c', 'linux', '大数据', 'web', '数据库']
        self.jobs = (
            'Java', 'C/C++', 'Python', 'C#', '区块链', 'Linux', '大数据', 'Web', '数据库', 'HTML5', '.NET', 'PHP', 'IOS',
            'Android', 'CSS', 'FPGA', '算法')
        conn.close()
        self.log = log.log()
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
        self.log.saveInfo('规范化数据')
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
                except ValueError:
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

    def statisticalAlltoOracle(self):
        '''统计所有的城市职业信息，并返回dataframe
            这个函数应该是在爬虫爬去所有的数据之后立即执行
            执行完这个函数后应该将ddff保存到数据库cty_job中
            后续需要分析的话就直接读取数据库city_job中的数据就行了'''
        citys = tuple(set(self.df.工作地点))
        l=[]
        # print(self.ddff)
        for city in citys:
            cityInfo = self.df[self.df.工作地点 == city]
            count = {}
            for job in self.jobs:
                # 统计一座城市的所有职位量
                # print(job)
                count[job] = len(
                    cityInfo[cityInfo.apply(self.process, axis=1, args=([job]))])  # 是df的子集
            print(count)  # 字典{job: num}
            l.append(count)
            # self.ddff = self.ddff.append(count, ignore_index=True)
            # self.ddff[city] = count
        self.ddff = pd.DataFrame(l,index=citys)
        self.ddff = self.ddff.T
        print(self.ddff)
        print(self.ddff)
        return self.ddff



    def getJobInCity(self):
        '''统计职位数分布情况
            返回字典'''
        self.log.saveInfo('统计所有职位分布')
        return dict(self.df.工作地点.value_counts())  # {city: nums}

    def cityOfJob(self, job):
        '''找出某职位的城市分布信息
            返回字典{city: num}'''
        self.log.saveInfo('统计{}的城市分布信息'.format(job))
        jobinfo = self.df[self.df.apply(
            self.process, axis=1, args=([job]))]  # 是df的子集
        data = dict(collections.Counter(list(jobinfo.工作地点)))
        # 返回字典{city: num}
        return dict(sorted(data.items(), key=lambda x: x[1], reverse=True)[:12])

    def getAllJobNum(self):
        self.log.saveInfo('统计所有职位量')
        num = {}
        for job in self.jobs:
            num[job] = sum(self.cityOfJob(job).values())
        return num  # {job: num}

    def getAllJobNum_v0(self):
        '''找出各职位的招聘信息
            这个方法已经过时了，应该用下面的新的cityOfJob'''
        self.log.saveInfo('统计职位量')

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
        return num  # {job: nums}

    # 得找出具体职位的城市分布
    # 这是一张三维图

    def jobinfo(self, job):
        '''找出各职位的具体招聘信息'''
        # re.I: 正则忽略大小写
        self.log.saveInfo('筛选{}的招聘信息'.format(job))
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

    def cityOfJob_v0(self, job):
        '''找出某职位的具体招聘信息
            返回的是df的一个子集'''

        # 利用apply方法，已经可以提取出特定招聘信息的条目了
        self.log.saveInfo('筛选{}的招聘信息'.format(job))
        return self.df[self.df.apply(self.process, axis=1, args=([job]))]

    def process(self, x, job):
        if job in x.工作名称 or job.upper() in x.工作名称 or job.capitalize() in x.工作名称 or job in x.职位描述 or job.upper() in x.职位描述 or job.capitalize() in x.职位描述:
            return True
        else:
            return False

    def jobsInCity(self, city):
        '''确定一个城市的职位统计
        :return:{job, num}'''
        self.log.saveInfo('统计{}的招聘情况'.format(city))
        data = self.df[self.df.工作地点 == city]
        # jobs = ('Java', 'C/C++', 'Python', 'C#', '区块链',
        #         'Linux', '大数据', 'Web', '数据库', 'HTML5', '.NET')
        count = {}
        for job in self.jobs:
            print(job)
            count[job] = len(
                data[data.apply(self.process, axis=1, args=([job]))])  # 是df的子集
        print(count)
        return count  # 返回字典{job: num}

    def compress(self, value1, value2):
        self.log.saveInfo('比较{}和{}'.format(value1, value2))
        # if flag == 0:  # 某个职位的城市分布信息
        #     d1 = self.cityOfJob(value1)  # value1的具体招聘信息，是字典{city: num}
        #     d2 = self.cityOfJob(value2)  # value2的具体招聘信息，是字典{city: num}
        # else:  # 某个城市的职位信息统计
        #     d1 = self.jobsInCity(value1)  # value1的具体招聘信息，是字典{job: num}
        #     d2 = self.jobsInCity(value2)  # value2的具体招聘信息，是字典{job: num}
        d1 = self.cityOfJob(value1)  # value1的具体招聘信息，是字典{city: num}
        d2 = self.cityOfJob(value2)  # value2的具体招聘信息，是字典{city: num}
        data1 = dict(sorted(d1.items(), key=lambda x: x[
            1], reverse=True)[:16])  # 获取前12名
        data2 = dict(sorted(d2.items(), key=lambda x: x[1], reverse=True)[:16])
        print('d1:', d1, '\n', 'd2:', d2, '\n',
              'data1:', data1, '\n', 'data2:', data2)
        l2 = list(data2.keys())
        l1 = list(data1.keys())
        l = [v for v in l1 if v in l2]
        print(l)
        data = {}
        for city in l:
            data[city] = (d1[city], d2[city])
        print(data)
        return data

    def jobRequest(self, job):
        '''
        统计职职位要求
        :return:
        '''
        self.log.saveInfo('%{}占比'.format(job))
        jobNums = self.getAllJobNum()
        count = reduce(lambda x, y: x + y, jobNums.values())
        return jobNums[job] / count


# df=getData()
# print(getJobInfo(df,'c#'))
if __name__ == '__main__':
    d = DataOptions()
    # d.compress('java', 'c++')
    # d.jobsInCity('北京')
    d.statisticalAlltoOracle()
    # print(d.getJobInCity())
# t=d.cityOfJob('java')
# print(t)
# return t
