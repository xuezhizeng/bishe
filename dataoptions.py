#!/usr/bin/env python
# -*- coding:utf-8 -*-
import cx_Oracle
import pandas as pd
import re
import log


class DataOptions(object):

    def __init__(self):
        '''初始化就是从数据库里读取数据'''
        try:
            conn = cx_Oracle.connect("star/star@127.0.0.1/orcl")
        except(cx_Oracle.DatabaseError, cx_Oracle.OperationalError) as e:
            exit(-1)
        sql = 'select * from city_job'

        # Index(['网址', '工作名称', '公司名称', '公司网址', '福利', '月工资', '发布日期', '经验', '人数', '工作地点',
        #        '工作性质', '最低学历', '职位类别', '公司规模', '公司性质', '公司行业', '职位描述', '是否失效'])
        self.jobs = ['.NET', 'Android', 'C#', 'C/C++', 'CSS', 'FPGA', 'HTML5', 'IOS', 'Java', 'Linux', 'PHP', 'Python',
                     'Web', '区块链', '大数据', '数据库', '算法']
        self.df = pd.read_sql(sql=sql, con=conn)
        self.df.index = self.jobs
        conn.close()
        self.log = log.log()

    def format(self, df):
        '''提取城市'''
        # 清除失效信息
        self.log.saveInfo('规范化数据')
        df = df[df.是否失效 == '否']
        for i in range(len(df)):
            # 规范城市
            df.iloc[i, 9] = re.sub(r'-\S*$', '', df.iloc[i, 9])
            # 规范月薪
            try:
                n1 = re.sub(r'-\S*$', '', df.iloc[i, 5])
                n2 = re.sub(r'^\S*-', '', df.iloc[i, 5])
                n2 = re.sub(r'元/月', '', n2)
                df.iloc[i, 5] = (int(n1) + int(n2)) / 2
            except ValueError:
                df.iloc[i, 5] = 0
                continue
            # 公司规模
            if re.findall(r'-', str(df.iloc[i, 13])):
                try:
                    n1 = re.sub(r'-\S*$', '', df.iloc[i, 13])
                    n2 = re.sub(r'^\S*-', '', df.iloc[i, 13])
                    n2 = re.sub(r'人', '', n2)
                    df.iloc[i, 13] = (int(n1) + int(n2)) / 2
                except ValueError:
                    df.iloc[i, 13] = 0
                    continue
            else:
                if re.findall(r'人', df.iloc[i, 13]):
                    df.iloc[i, 13] = int(
                        re.sub(r'人\S*$', '', df.iloc[i, 13]))
                else:
                    df.iloc[i, 13] = 0
                    continue
        return df

    def process(self, x, job):
        if job == 'C/C++':
            job = 'c++'
        if job in x.工作名称 or job.upper() in x.工作名称 or job.capitalize() in x.工作名称 or job in x.职位描述 or job.upper() in x.职位描述 or job.capitalize() in x.职位描述:
            return True
        else:
            return False

    def statisticalAlltoOracle(self, df):
        '''统计所有的城市职业信息，并返回dataframe
            这个函数应该是在爬虫爬去所有的数据之后，西安执行format格式化，然后执行这个函数
            执行完这个函数后应该将ddff保存到数据库cty_job中
            后续需要分析的话就直接读取数据库city_job中的数据就行了'''
        citys = tuple(set(df.工作地点))
        l = []
        for city in citys:
            cityInfo = df[df.工作地点 == city]
            count = {}
            for job in self.jobs:
                # 统计一座城市的所有职位量
                count[job] = len(
                    cityInfo[cityInfo.apply(self.process, axis=1, args=([job]))])  # 是df的子集
            l.append(count)
        ddff = pd.DataFrame(l, index=citys)
        ddff = ddff.T
        return ddff

    def getJobInCity(self):
        '''统计职位数分布情况
            返回字典'''
        self.log.saveInfo('统计所有职位分布')
        count = {}
        for city in self.df.columns:
            count[city] = sum(self.df[city])
        return count  # {city: nums}

    def cityOfJob(self, job):
        '''找出某职位的城市分布信息
            返回字典{city: num}'''
        self.log.saveInfo('统计{}的城市分布信息'.format(job))
        return dict(self.df.ix[job])  # 返回字典{city: num}

    def getAllJobNum(self):
        self.log.saveInfo('统计所有职位量')
        count = {}
        for job in self.df.index:
            count[job] = sum(self.df.ix[job])
        return count  # {job: num}

    def jobinfo(self, job):
        '''找出各职位的具体招聘信息'''
        # re.I: 正则忽略大小写
        self.log.saveInfo('筛选{}的招聘信息'.format(job))
        pass
        if 'c++' == job or 'C++' == job:
            job = 'c\+\+'
        elif 'c' == job or 'C' == job:
            job += '[^+#]'
        p = re.compile(job, re.I)
        return self.df.loc[filter(lambda s: re.search(p, s), self.df.工作名称)]

    def cityOfJob_v0(self, job):
        '''找出某职位的具体招聘信息
            返回的是df的一个子集'''

        # 利用apply方法，已经可以提取出特定招聘信息的条目了
        self.log.saveInfo('筛选{}的招聘信息'.format(job))
        pass
        return self.df[self.df.apply(self.process, axis=1, args=([job]))]

    def jobsInCity(self, city):
        '''确定一个城市的职位统计
        :return:{job, num}'''
        self.log.saveInfo('统计{}的招聘情况'.format(city))
        return dict(self.df[city])

    def compress(self, value1, value2):
        self.log.saveInfo('比较{}和{}'.format(value1, value2))
        d1 = self.cityOfJob(value1)  # value1的具体招聘信息，是字典{city: num}
        d2 = self.cityOfJob(value2)  # value2的具体招聘信息，是字典{city: num}
        data1 = dict(sorted(d1.items(), key=lambda x: x[1], reverse=True)[:13])  # 获取前12名
        data2 = dict(sorted(d2.items(), key=lambda x: x[1], reverse=True)[:13])
        l2 = list(data2.keys())
        l1 = list(data1.keys())
        l = [v for v in l1 if v in l2]
        data = {}
        for city in l:
            data[city] = (d1[city], d2[city])
        return data  # {'北京': ('324', '532')}

    def jobRequest(self, job):
        '''
        统计职位所占比
        :return:
        '''
        self.log.saveInfo('%{}占比'.format(job))
        jobNums = self.getAllJobNum()
        return jobNums[job] / sum(jobNums.values())


if __name__ == '__main__':
    d = DataOptions()
    d.statisticalAlltoOracle()
