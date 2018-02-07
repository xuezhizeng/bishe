#!/usr/bin/env python
# -*- coding:utf-8 -*-

from wedfunctions import *
from oracleoptions import *


def gooddata(data):
    pass


def get_data(urls):
    columns = ["网址", "工作名称", "公司名称", "公司网址", "福利", "月工资", "发布日期", "经验", "人数", "工作地点", "工作性质", "最低学历", "职位类别", "公司规模",
               "公司性质", "公司行业", "职位描述", "是否失效"]
    df = pd.DataFrame(data=[], columns=columns)
    links = []
    for url in urls:
        print('获取职位具体信息, 网址: ' + url)
        data = get_link_info(url)
        df = df.append(data, ignore_index=True)
    return df


def index(job, city=''):
    # job = 'linux'
    npage = 10
    # city = ['深圳', '广州']
    # 返回搜索结果列表的所有超链接
    print('获取'+job+'的所有链接')
    urls = get_links_from(job, npage, city)

    # 首先搜索结果进行筛选一遍，因为有些置顶结果有不一样的链接
    # 比如，职位置顶会链接到'https://e.zhaopin.com/products/1/detail.do'
    urls = [url for url in urls if '.htm' in url]
    print('以下是有效的链接: ')
    print(urls)
    print('开始获取具体的职位信息')
    df = get_data(urls)

    # 写到Oracle数据库中

    print('保存到数据库')
    save_to_oracle(df, database=job)

# print('搜索Linux')
# index('linux')
# print()
#
#
# print('搜索python')
# index('python')
# print()

print('搜索java')
index('java')
print()

print('***************************************************************************************')
print('***************************************************************************************')
print('***************************************************************************************')
print('***************************************************************************************')
print('***************************************************************************************')
print('***************************************************************************************')
print('***************************************************************************************')

# print('搜索C#')
# index('linux')
# print()
