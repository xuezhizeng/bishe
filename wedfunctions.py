#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
import urllib
import string
from bs4 import BeautifulSoup
import formatstaing
import sys, io

# 用来配置请求包的头，否则有些服务器会拒绝请求
headers = [
    "Mozilla/5.0 (Windows NT 6.1; Win64; rv:27.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:27.0) Gecko/20100101 Firfox/27.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:10.0) Gecko/20100101 Firfox/10.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/21.0.1180.110 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686 rv:10.0) Gecko/20100101 Firfox/27.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/34.0.1838.2 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686 rv:27.0) Gecko/20100101 Firfox/27.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 ",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
]


def get_content(url):
    '''
    获取url中的网页内容，最终返回HTML的树形结构，每个节点都是一个HTML对象
    :param url: 需要获取内容的网页链接
    :return: 经lxml解析后的网页内容
    '''
    random_header = random.choice(headers)
    req = urllib.request.Request(url)
    # random_header="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"
    req.add_header("User-Agent", random_header)  # 需要随机设定用户代理以隐藏身份,否则有些服务器会拒绝请求
    req.add_header("Get", url)  # 所请求页面
    try:
        html = urllib.request.urlopen(req)  # 打开请求网页
    except (urllib.error.HTTPError, TimeoutError) as e:
        print(e)
    # html = urllib.request.urlopen(req)  # 打开请求网页
    else:
        contents = html.read()  # html.read()只能执行一次，再次执行返回结果为空，所以得先把结果保存下来
        if isinstance(contents, bytes):  # 判断输出内容contents是否是字节格式
            contents = contents.decode('utf-8')  # 转成字符串格式，这样才能显示中文啊
        contents = BeautifulSoup(contents, "lxml")  # 设置解析器为“lxml”
        return (contents)


def get_links_from(ur):
    # def get_links_from(job, npage=1, city='全国'):
    '''
    搜索页面,返回搜索结果前npage页的职位超链接
    :param job: 工作名称
    :param city: 工作地点
    :param npage: 需要多少页的搜索结果
    :return: 所有列表的超链接，即子页网址
    '''
    # city_tmp = "jl={}".format('全国')
    # if isinstance(city, str) and city:
    #     city_tmp += "%2B{}".format(city)
    # else:
    #     for i in range(len(city)):
    #         city_tmp += "%2B{}".format(str(city[i]))
    urls = []
    npage = 90  # 智联招聘最多就只显示90页
    for i in range(1, npage + 1):
        # 这里这个url是囊括了IT行业几乎所有的搜索页面
        # url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&in=210500;160400;160000;300100;160600&jl=全国&p={}&isadv=0'.format(
        #     str(i))
        # p='&p={}'.format(str(i))
        url = ur + '&p=%s' % str(i)
        print('get content: ' + url)
        print(type(url))

        # url = "http://sou.zhaopin.com/jobs/searchresult.ashx?kw={}&p={}&".format(str(job), str(i)) + city_tmp
        # quote('枝桠') -> '%E6%9E%9D%E6%A1%A0'
        url = urllib.parse.quote(url, safe=string.printable)  # 进行URL编码，safe是不编码的字符集
        content = get_content(url)
        link_urls = content.select('td.zwmc a')  # 分析智联招聘搜索网页知这是在拉取搜索结果的职位链接
        for url in link_urls:
            urls.append(url.get('href'))
    return (urls)  # 前npage页的职位链接都在这里了


# 这个函数不适合校园招聘
def get_link_info(url):
    '''
    获取此网站的有用信息并保存成字典形式
    @url: 爬取的地址
    @return: 此网站的有用信息
    '''

    # 获取网页内容
    print("获取网页: " + str(url) + " 有用信息")
    content = get_content(url)
    # 校园招聘的HTML格式与其他不同，所以这里要分开选择
    if 'xiaoyuan' in url:
        job = content.select('div.cJobDetailInforWrap h1')[0]  # 工作名称
        company = content.select('div.cJobDetailInforWrap li')[1]  # 公司名称
        company_url = content.select('div.cJobDetailInforWrap li a')[0]  # 公司网址
        date = content.select('div.cJobDetailInforWrap li')[15]  # 发布日期
        num = content.select('div.cJobDetailInforWrap li')[13]  # 人数
        area = content.select('div.cJobDetailInforWrap li')[9]  # 工作地点
        cate = content.select('div.cJobDetailInforWrap li')[11]  # 职位类别
        com_scale = content.select('div.cJobDetailInforWrap li')[5]  # 公司规模
        com_nature = content.select('div.cJobDetailInforWrap li')[7]  # 公司性质
        com_eatcatee = content.select('div.cJobDetailInforWrap li')[3]  # 公司行业
        discribe = content.select('div.cJobDetail_tabSwitch  div.cJobDetail_tabSwitch_content p')[0]  # 加注职位描述
        # 实习生没有这三项
        welfare = None,
        pay = None,
        exper = None,
        job_nature = '实习'
        educate = None
    else:
        job = content.select('div.fixed-inner-box h1')[0]  # 工作名称
        company = content.select('div.fixed-inner-box h2')[0]  # 公司名称
        company_url = content.select('div.inner-left.fl h2 a')[0]  # 公司网址
        welfare = content.select('div.welfare-tab-box')[0]  # 福利
        pay = content.select('div.terminalpage-left strong')[0]  # 月薪
        date = content.select('div.terminalpage-left strong')[2]  # 发布日期
        exper = content.select('div.terminalpage-left strong')[4]  # 经验
        num = content.select('div.terminalpage-left strong')[6]  # 人数
        area = content.select('div.terminalpage-left strong')[1]  # 工作地点
        job_nature = content.select('div.terminalpage-left strong')[3]  # 工作性质
        educate = content.select('div.terminalpage-left strong')[5]  # 最低学历
        cate = content.select('div.terminalpage-left strong')[7]  # 职位类别
        com_scale = content.select('ul.terminal-ul.clearfix li strong')[8]  # 公司规模
        com_nature = content.select('ul.terminal-ul.clearfix li strong')[9]  # 公司性质
        com_eatcatee = content.select('ul.terminal-ul.clearfix li strong')[10]  # 公司行业
        discribe = content.select('div.terminalpage-main div.tab-inner-cont')[0]  # 职位描述
        # 为了保持data赋值一致
        welfare = welfare.text.strip()
        pay = pay.text.strip()
        exper = exper.text.strip()
        job_nature = job_nature.text.strip()
        educate = educate.text.strip()

    # 这里对职位描述进行规范化
    # 否则有些晦涩的字符导致写Oracle失败
    discribe = discribe.text.split()
    disc = ''
    for i in discribe:
        disc += str(i)
    disc = formatstaing.format_str(disc)

    if content.select('li.outmoded_container_img'):  # 是否有职位失效印章
        outmoded = '是'
    else:
        outmoded = '否'

    data = {
        #  strip() 方法用于移除字符串头尾指定的字符（默认为空格）
        "网址": url,
        "工作名称": job.text.strip(),
        "公司名称": company.text.strip(),
        "公司网址": company_url.get('href'),
        "福利": welfare,
        "月工资": pay,
        "发布日期": date.text.strip(),
        "经验": exper,
        "人数": num.text.strip(),
        "工作地点": area.text.strip(),
        "工作性质": job_nature,
        "最低学历": educate,
        "职位类别": cate.text.strip(),
        "公司规模": com_scale.text.strip(),
        "公司性质": com_nature.text.strip(),
        "公司行业": com_eatcatee.text.strip(),
        "职位描述": disc,
        "是否失效": outmoded,
    }
    return (data)
