#!/usr/bin/env python
# -*- coding:utf-8 -*-

from wedfunctions import *
from oracleoptions import *
import time
from multiprocessing import Pool
import pandas as pd
import functools


def gooddata(data):
    pass


def get_data(urls):
    columns = ["网址", "工作名称", "公司名称", "公司网址", "福利", "月工资", "发布日期", "经验", "人数", "工作地点", "工作性质", "最低学历", "职位类别", "公司规模",
               "公司性质", "公司行业", "职位描述", "是否失效"]
    df = pd.DataFrame(data=[], columns=columns)
    links = []
    for url in urls:
        # print('获取职位具体信息, 网址: ' + url)
        data = get_link_info(url)
        df = df.append(data, ignore_index=True)
    return df


def timer(func):
    # 把原始函数的__name__等属性复制到wrapper()函数中,否则,有些依赖函数签名的代码执行就会出错.
    @functools.wraps(func)
    def wrapper(*args, **kw):
        start = time.time()
        func(*args, **kw)
        end = time.time()
        # print('爬取时间：' + str((end - start) / 60) + 'min')

    return wrapper


@timer
def index(url):
    # def index(job, city=''):
    # job = 'linux'
    npage = 1
    # city = ['深圳', '广州']
    # 返回搜索结果列表的所有超链接
    # print('获取' + url + '的所有链接')
    urls = get_links_from(url)
    # urls = get_links_from(job, npage, city)

    # 首先搜索结果进行筛选一遍，因为有些置顶结果有不一样的链接
    # 比如，职位置顶会链接到'https://e.zhaopin.com/products/1/detail.do'
    urls = [u for u in urls if '.htm' in u]
    # print('以下是有效的链接: ')
    # print(urls)
    # print('开始获取具体的职位信息')
    df = get_data(urls)

    # 写到Oracle数据库中

    # print('保存到数据库')
    # job = 'test'
    job = 'zhaopin'
    save_to_oracle(df, database=job)


# if __name__ == '__main__':
#     pool = Pool(processes=2)
#     url = ["http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&in=210500;160000;160200;160100&jl=选择地区&isadv=0",
#            "http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&in=160400;160500;300100;160600&jl=选择地区&isadv=0"]
#     pool.map_async(index, url)
#     pool.close()
#     pool.join()

def main():

    urls = ['http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&in=210500;160000;160200;160100&jl=选择地区&isadv=0',
            'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&in=160400;160500;300100;160600&jl=选择地区&isadv=0']
    return index(url=urls[1])
