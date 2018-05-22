# !/usr/bin/env python
# coding:utf-8
# 绘图模块：draw.py
# 封装成pictures类
import tkinter as tk
import dataoptions as dp
import numpy as np
import datetime
import matplotlib

matplotlib.use('TkAgg')
# 解决负号不正常显示问题
matplotlib.rcParams['axes.unicode_minus'] = False
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk
import log
# from tkinter import scrolledtext
# from tkinter import Menu
# from tkinter import Spinbox
# from tkinter import messagebox as mBox

# 下面两行解决中文显示问题
import pylab

pylab.mpl.rcParams['font.sans-serif'] = ['SimHei']


class draw(object):
    """绘图模块，专注画图"""

    def __init__(self, ):
        super(draw, self).__init__()
        self.log = log.log()

        self.log.saveInfo('实例化draw')
        self.df = dp.DataOptions()
        # 每个城市的职位总数
        self.root = tk.Tk()
        self.root.title('基于Python技术的基础数据可视化应用')
        # self.root.setvar()
        # 设置窗口图标
        self.root.iconbitmap(r'e:\15970\Pictures\123.ico')
        # 设置窗口的大小宽x高+偏移量
        self.root.geometry('1000x630+100+30')
        self.root.resizable(0, 0)
        self.analytic = ""
        self.values = {
            'job_all': ('all', 'Java', 'C/C++', 'Python', 'C#', '区块链', 'Linux', '大数据', 'Web', '数据库', 'HTML5', '.NET'),
            'city_all': ('all', '北京', '上海', '广州', '深圳', '南京', '成都', '杭州', '武汉', '西安', '郑州'),
            'job': ('all', 'Java', 'C/C++', 'Python', 'C#', '区块链', 'Linux', '大数据', 'Web', '数据库', 'HTML5', '.NET'),
            'city': ('all', '北京', '上海', '广州', '深圳', '南京', '成都', '杭州', '武汉', '西安', '郑州')}

        self.createCombobox()
        self.createButton()
        self.creatCanvas()

    # def func(self):

    def createCombobox(self):
        # Adding a Combobox

        self.log.saveInfo('创建选择框')

        print('init：创建Chosen1')
        self.value1 = tk.StringVar()
        self.Chosen1 = ttk.Combobox(
            self.root, width=12, textvariable=self.value1)
        # jobs = ('Java', 'C/C++', 'Python', 'C#', '区块链',
        #         'Linux', '大数据', 'Web', '数据库', 'HTML5', '.NET')
        self.Chosen1['values'] = self.values['job']
        self.Chosen1.grid(row=0, column=1,
                          columnspan=4, sticky='W')
        self.Chosen1.current(3)  # 设置初始显示值，值为元组['values']的下标
        self.Chosen1.config(state='readonly')  # 设为只读模式
        createToolTip(self.Chosen1, '选择1.')

        # Adding a Combobox
        print('init：创建Chosen2')
        self.value2 = tk.StringVar()
        self.Chosen2 = ttk.Combobox(
            self.root, width=12, textvariable=self.value2)
        self.Chosen2['values'] = self.values['job']
        self.Chosen2.grid(row=1, column=1,
                          columnspan=4, sticky='W')
        self.Chosen2.current(2)  # 设置初始显示值，值为元组['values']的下标
        self.Chosen2.config(state='readonly')  # 设为只读模式
        createToolTip(self.Chosen2, '选择2.')

        print('init：创建action0')
        self.action0 = ttk.Button(
            self.root, text="比较", width=10, command=self.compare)
        self.action0.grid(row=0, rowspan=2, column=6)


        # 创建单选框
        self.createRadiobutton()
        # Adding a Combobox
        print('init：创建jobChosen')
        self.Combobox1Value = tk.StringVar()
        self.Combobox1 = ttk.Combobox(
            self.root, width=12, textvariable=self.Combobox1Value)
        # jobs = ('all', 'Java', 'C/C++', 'Python', 'C#', '区块链',
        #         'Linux', '大数据', 'Web', '数据库', 'HTML5', '.NET')
        self.Combobox1['values'] = self.values['job_all']
        self.Combobox1.grid(row=1, column=8,
                            columnspan=4, sticky='W')
        self.Combobox1.current(0)  # 设置初始显示值，值为元组['values']的下标
        self.Combobox1.config(state='readonly')  # 设为只读模式
        createToolTip(self.Combobox1, '选择技术.')

        print('init：创建action1')
        self.action1 = ttk.Button(
            self.root, text="重绘", width=10, command=self.reDraw)
        self.action1.grid(row=0, rowspan=2, column=12)

        print('init：创建action2')
        self.action2 = ttk.Button(
            self.root, text="后台更新数据", width=12, command=self.updata)
        self.action2.grid(row=0, rowspan=2, column=15,
                          columnspan=4)  # , ipady=7)

    def createButton(self):
        # Adding a Button
        # self.log.saveInfo('创建按钮')

        pass

        # columnspan=2)  # , ipady=7)


        # columnspan=2)  # , ipady=7)

        # Adding a Button


    def createRadiobutton(self):
        self.CityorJob = tk.IntVar()
        self.CityorJob.set(0)  # 初始化为技术
        tk.Radiobutton(self.root, text='技术', variable=self.CityorJob, value=0,
                       command=self.echoRadiobutton).grid(row=0, column=8, sticky=tk.W)
        tk.Radiobutton(self.root, text='城市', variable=self.CityorJob, value=1,
                       command=self.echoRadiobutton).grid(row=0, column=9, sticky=tk.W)

    def creatCanvas(self):
        self.log.saveInfo('创建画板')
        # print('init：创建canvas1')
        self.figure1 = Figure(figsize=(6, 6), dpi=100)
        self.canvas1 = FigureCanvasTkAgg(self.figure1, master=self.root)
        self.canvas1.get_tk_widget().grid(row=2, rowspan=4, column=0, columnspan=18)
        self.canvas1.show()

        # print('init：创建canvas2')
        self.figure2 = Figure(figsize=(4, 3), dpi=100)
        self.canvas2 = FigureCanvasTkAgg(self.figure2, master=self.root)
        self.canvas2.get_tk_widget().grid(row=2, rowspan=2, column=18, columnspan=10)
        self.canvas2.show()

        # print('init：创建canvas3')
        self.figure3 = Figure(figsize=(4, 3), dpi=100)
        self.canvas3 = FigureCanvasTkAgg(self.figure3, master=self.root)
        self.canvas3.get_tk_widget().grid(row=4, rowspan=2, column=18, columnspan=10)
        self.canvas3.show()

    def echoRadiobutton(self):
        print(self.CityorJob.get())
        if self.CityorJob.get() == 0:
            self.Combobox1['values'] = self.values['job_all']
        else:
            self.Combobox1['values'] = self.values['city_all']

    def updata(self):
        self.log.saveInfo('更新数据')

    def picture1(self):
        pass

    def picture2(self):
        pass

    def picture3(self):
        pass

    def compare(self):
        '''对两个字典进行比较，比如：
            job1和job2的城市分布前12名
            city1和city2的job分布前12名'''
        # self.log.saveInfo('比较{}和{}'.format(value1, value2))
        value1 = self.value1.get()
        value2 = self.value2.get()
        self.log.saveInfo('比较{}和{}'.format(value1, value2))
        data = self.df.compress(value1, value2)
        # print(data)
        num1 = np.array([v[0] for v in data.values()])
        num2 = np.array([v[1] for v in data.values()])

        self.figure1.clf()
        fig = self.figure1.add_subplot(111)
        time = datetime.datetime.now()
        fig.set_title(str(time.year) + '/' + str(time.month) +
                      '/' + str(time.day) + '职位分布图')
        fig.bar(data.keys(), num1, label=value1)
        fig.bar(data.keys(), -num2, label=value2)
        fig.legend(loc='upper right')
        fig.set_xticklabels(data.keys(), minor=False, rotation=45)
        # 绘制文字，显示柱状图的值
        # for x, y in zip(data.keys(), num1):
        #     fig.text(x, y + 5, y, ha='center', va='bottom',
        #              fontsize=8)  # ,rotation=45)
        # for x, y in zip(data.keys(), num2):
        #     fig.text(x, -y - 8, y, ha='center', va='bottom',
        #              fontsize=8)  # ,rotation=45)
        # fig.xaxis.set(rotation=45)
        self.canvas1.show()

    # def compareByCity(self, city1, city2):
    #     self.compare(city1, city2, 1)
    #
    # def compareByJob(self, job1, job2):
    #     self.compare(job1, job2, 0)

    def count(self, value, flag):
        if flag == 0:  # 统计某座城市的招聘信息
            return self.df.jobsInCity(value)  # 字典{job: num}
        else:  # 统计某种技术的城市分布信息
            return self.df.cityOfJob(value)  # 字典{city: num}

    def countAllJobs(self, figure, canvas):
        '''统计每个城市的所有职位数，不分行业'''
        self.log.saveInfo('绘制所有的职位信息的柱状图')
        # print('countAllJobs')
        num = self.df.getJobInCity()
        num = dict(sorted(num.items(), key=lambda x: x[
            1], reverse=True)[:10])  # {city: num}

        # 清空图像，以使得前后两次绘制的图像不会重叠
        figure.clf()
        fig = figure.add_subplot(111)
        fig.set_title('职业概况图')
        fig.bar(num.keys(), num.values(), label="职位数")
        fig.set_xticklabels(num.keys(), minor=False, rotation=45)
        # 绘制文字，显示柱状图的值
        for x, y in zip(num.keys(), num.values()):
            fig.text(x, y + 5, y, ha='center', va='bottom', fontsize=12)
        canvas.show()

    def countByJob(self, job, figure, canvas):
        '''统计某种技术的城市分布信息'''
        self.log.saveInfo('绘制{}的城市分布情况柱状图'.format(job))
        count = self.df.cityOfJob(job)  # 字典{city: num}
        print('countByJob')
        figure.clf()
        fig = figure.add_subplot(111)
        fig.set_title('{}的城市分布图'.format(job))
        # fig.plot(count.keys(), count.values())
        fig.bar(count.keys(), count.values(), label='label')
        # for x, y in zip(count.keys(), count.values()):
        #     fig.text(x, y + 5, y, ha='center', va='bottom', fontsize=8)
        canvas.show()

    def countByCity(self, city, figure, canvas):
        '''某座城市的招聘信息统计'''
        self.log.saveInfo('绘制{}的招聘情况柱状图'.format(city))
        count = self.df.jobsInCity(city)  # 字典{job: num}
        print('countByCity')
        figure.clf()
        fig = figure.add_subplot(111)
        fig.set_title('countByCity')
        # fig.plot(count.keys(), count.values())
        fig.bar(count.keys(), count.values(), label='label')
        # for x, y in zip(count.keys(), count.values()):
        #     fig.text(x, y + 5, y, ha='center', va='bottom', fontsize=8)
        canvas.show()

    def cityCountOfjob(self, job, figure, canvas):
        '''某种职业的城市分布饼图'''
        # pass
        self.log.saveInfo('绘制{}的招聘情况柱状图'.format(job))
        data0 = self.df.cityOfJob(job)  # 字典{job: num}
        count = dict(
            sorted(data0.items(), key=lambda x: x[1], reverse=True)[:6])
        count['其他'] = sum(data0.values()) - sum(count.values())
        print('countByCity')
        figure.clf()
        fig = figure.add_subplot(111)
        fig.set_title('{}的城市分布图'.format(job))
        # fig.plot(count.keys(), count.values())
        fig.bar(count.keys(), count.values(), label='label')
        fig.set_xticklabels(count.keys(), minor=False, rotation=45)
        # for x, y in zip(count.keys(), count.values()):
        #     fig.text(x, y + 5, y, ha='center', va='bottom', fontsize=8)
        canvas.show()

    def cityCountOfjob_pie(self, job, figure, canvas):
        '''某种职业的城市分布饼图'''
        self.log.saveInfo('绘制{}的城市分布饼图'.format(job))
        data0 = self.df.cityOfJob(job)
        data = dict(
            sorted(data0.items(), key=lambda x: x[1], reverse=True)[:6])
        data['其他'] = sum(data0.values()) - sum(data.values())
        figure.clf()
        fig = figure.add_subplot(111)
        fig.set_title('{}城市分布图'.format(job))
        fig.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
        fig.set_aspect('equal')
        fig.set_xticks([])
        fig.set_yticks([])
        canvas.show()

    def jobsCountInCity(self, city, figure, canvas):
        self.log.saveInfo('绘制{}职位分布柱状图'.format(city))
        # print('In jobsCountInCity city: %s' % city)
        data0 = self.df.jobsInCity(city)  # 字典{job: num}
        print(data0)
        data = dict(
            sorted(data0.items(), key=lambda x: x[1], reverse=True)[:6])
        data['其他'] = sum(data0.values()) - sum(data.values())
        print(data)
        figure.clf()
        fig = figure.add_subplot(111)
        fig.set_title('{}职位数分布图'.format(city))
        fig.bar(data.keys(), data.values())
        fig.set_xticklabels(data.keys(), minor=False, rotation=45)
        # for x, y in zip(data.keys(), data.values()):
        #     fig.text(x, y + 5, y, ha='center', va='bottom', fontsize=8)
        canvas.show()

    def jobsCountInCity_pie(self, city, figure, canvas):
        self.log.saveInfo('绘制{}职位信息饼图'.format(city))
        '''某座城市的职位分布饼图'''
        data0 = self.df.jobsInCity(city)  # 字典{job: num}
        data = dict(
            sorted(data0.items(), key=lambda x: x[1], reverse=True)[:6])
        data['其他'] = sum(data0.values()) - sum(data.values())
        figure.clf()
        fig = figure.add_subplot(111)
        fig.set_title('{}职位统计图'.format(city))
        fig.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
        fig.set_aspect('equal')
        fig.set_xticks([])
        fig.set_yticks([])
        canvas.show()

    def allCity_pie(self, figure, canvas):
        self.log.saveInfo('绘制城市职位概总饼图')
        '''所有城市的所有职位的总图'''
        citys = self.df.getJobInCity()  # {'武汉':123, '北京':231}
        data = dict(
            sorted(citys.items(), key=lambda x: x[1], reverse=True)[:6])
        data['其他'] = sum(citys.values()) - sum(data.values())
        figure.clf()
        fig = figure.add_subplot(111)
        fig.set_title('城市职位总图')
        fig.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
        fig.set_aspect('equal')
        fig.set_xticks([])
        fig.set_yticks([])
        canvas.show()

    def allJobs_pie(self, figure, canvas):
        self.log.saveInfo('绘制职位信息概总饼图')
        '''所有职位的所有城市的总图'''
        jobs = self.df.getAllJobNum()  # {'java':234, 'python':234}
        data = dict(
            sorted(jobs.items(), key=lambda x: x[1], reverse=True)[:6])
        data['其他'] = sum(jobs.values()) - sum(data.values())
        figure.clf()
        fig = figure.add_subplot(111)
        fig.set_title('职位总图')
        fig.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
        fig.set_aspect('equal')
        fig.set_xticks([])
        fig.set_yticks([])
        canvas.show()

    def reDraw(self):
        # print('redraw重画')
        # print(self.city.get(), self.job.get())
        self.log.saveInfo('重绘')
        # citys = self.df.getJobInCity()  # {'武汉':123, '北京':231}
        # city = self.city.get()
        # city = '深圳'
        # job = self.job.get()
        value = self.Combobox1Value.get()
        if value == 'all':  # 概况
            print('No1')
            # self.countAllJobs(self.figure1, self.canvas1)
            self.allCity_pie(self.figure2, self.canvas2)
            self.allJobs_pie(self.figure3, self.canvas3)
        elif self.CityorJob.get() == 0:  # 某种职业的城市分布
            print('No2')
            self.cityCountOfjob(value, self.figure2, self.canvas2)
            self.cityCountOfjob_pie(value, self.figure3, self.canvas3)
        else:  # 某座城市的职业分布
            print('No3')
            self.jobsCountInCity(value, self.figure2, self.canvas2)
            self.jobsCountInCity_pie(value, self.figure3, self.canvas3)
        # else:  # 某种做城市的某种职业的情况
        #     pass

    def show(self):
        print('show: mainloop')
        self.reDraw()
        self.compare()
        self.root.mainloop()


# ===================================================================
# 由于tkinter中没有ToolTip功能，所以自定义这个功能如下

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        '''Display text in tooltip window'''
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))

        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


# ===================================================================

# createToolTip(spin, '这是一个Spinbox.')
# 悬浮框提醒控件

def createToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


if __name__ == '__main__':
    d = draw()
    d.show()
    # d.jobsCountInCity('深圳', d.figure2, d.canvas2)
    # d.root.mainloop()
