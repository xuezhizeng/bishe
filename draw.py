# !/usr/bin/env python
# coding:utf-8
# 绘图模块：draw.py
# 封装成pictures类
import tkinter as tk
import dataoptions as dp
import numpy as np
import datetime
# matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Spinbox
from tkinter import messagebox as mBox

# 下面两行解决中文显示问题
import pylab

pylab.mpl.rcParams['font.sans-serif'] = ['SimHei']


class draw(object):
    """绘图模块，专注画图"""

    def __init__(self, ):
        super(draw, self).__init__()
        self.df = dp.DataOptions()
        self.root = tk.Tk()
        # self.root.size(12,8)

        # Adding a Combobox
        print('init：创建cityChosen')
        self.city = tk.StringVar()
        self.cityChosen = ttk.Combobox(
            self.root, width=12, textvariable=self.city)
        self.cityChosen['values'] = ('北京', '上海', '广州', '深圳', '南京',
                                     '成都', '杭州', '武汉', '西安', '郑州')
        self.cityChosen.grid(row=0, rowspan=3, column=1,
                             columnspan=2, sticky='W')
        self.cityChosen.current(2)  # 设置初始显示值，值为元组['values']的下标
        self.cityChosen.config(state='readonly')  # 设为只读模式
        createToolTip(self.cityChosen, '选择城市.')

        # Adding a Combobox
        print('init：创建jobChosen')
        self.job = tk.StringVar()
        self.jobChosen = ttk.Combobox(
            self.root, width=12, textvariable=self.job)
        self.jobChosen['values'] = ('Java', 'C/C++', 'Python', 'C#', '区块链',
                                    'Linux', '大数据', 'Web', '数据库', 'HTML5', '.NET')
        self.jobChosen.grid(row=0, rowspan=3, column=3,
                            columnspan=2, sticky='W')
        self.jobChosen.current(2)  # 设置初始显示值，值为元组['values']的下标
        self.jobChosen.config(state='readonly')  # 设为只读模式
        createToolTip(self.jobChosen, '选择技术.')

        # Adding a Button
        print('init：创建action1')
        self.action1 = ttk.Button(
            self.root, text="重画", width=10, command=self.reDraw)
        self.action1.grid(row=0, rowspan=3, column=6,
                          columnspan=2)  # , ipady=7)

        # Adding a Button
        print('init：创建action2')
        self.action2 = ttk.Button(
            self.root, text="后台更新数据", width=12, command=self.updata)
        self.action2.grid(row=0, rowspan=3, column=11,
                          columnspan=2)  # , ipady=7)

        # 在Tk的GUI上放置一个画布，并用.grid()来调整布局
        # self.figure1 = Figure(figsize=(4, 6), dpi=100, facecolor='red')
        print('init：创建canvas1')
        self.figure1 = Figure(figsize=(4, 6), dpi=100)
        self.canvas1 = FigureCanvasTkAgg(self.figure1, master=self.root)
        self.canvas1.get_tk_widget().grid(row=3, rowspan=22, column=0, columnspan=9)
        # self.canvas1.show()
        self.picture1()

        print('init：创建canvas2')
        self.figure2 = Figure(figsize=(4, 3), dpi=100)
        self.canvas2 = FigureCanvasTkAgg(self.figure2, master=self.root)
        self.canvas2.get_tk_widget().grid(row=3, rowspan=11, column=9, columnspan=5)
        # self.canvas2.show()
        self.picture2()

        print('init：创建canvas3')
        self.figure3 = Figure(figsize=(4, 3), dpi=100)
        self.canvas3 = FigureCanvasTkAgg(self.figure3, master=self.root)
        self.canvas3.get_tk_widget().grid(row=14, rowspan=11, column=9, columnspan=5)
        # self.canvas3.show()
        self.picture3()

    def updata(self):
        print('updata:更新数据')
        self.action2.configure(text='Hello')
        self.picture1()
        self.picture2()
        self.picture3()
        self.action2.configure(state='disabled')  # Disable the Button Widget

    def picture1(self):
        self.compareByJob('java', 'c++')
        # print('picture1')
        # num = self.df.getJobInCity()
        # # sorted返回的是一个列表
        # num = dict(sorted(num.items(), key=lambda x: x[1], reverse=True)[:10])
        #
        # # 清空图像，以使得前后两次绘制的图像不会重叠
        # self.figure1.clf()
        # fig = self.figure1.add_subplot(111)
        # time = datetime.datetime.now()
        # fig.set_title(str(time.year) + '/' + str(time.month) +
        #               '/' + str(time.day) + '职位分布图')
        # fig.bar(num.keys(), num.values(), label="职位数")
        # # 绘制文字，显示柱状图的值
        # for x, y in zip(num.keys(), num.values()):
        #     fig.text(x, y + 5, y, ha='center', va='bottom', fontsize=12)
        # self.canvas1.show()

    def picture2(self):
        self.countByCity('北京')
        # # self.figure2.clf()
        # print('picture2')
        # fig = self.figure2.add_subplot(111)
        # fig.set_title('picture2')
        # fig.plot([1, 2, 3, 4, 5, 6], [1, 4, 9, 16, 25, 36])
        # self.canvas2.show()

    def picture3(self):
        self.countByJob('java')
        # self.figure3.clf()
        # print('picture3')
        # fig = self.figure3.add_subplot(111)
        # fig.set_title('picture3')
        # fig.plot([1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1])
        # self.canvas3.show()

    def compare(self, value1, value2, flag):
        data = self.df.compress(value1, value2, flag)
        num1 = np.array([v[0] for v in data.values()])
        num2 = np.array([v[1] for v in data.values()])

        self.figure1.clf()
        fig = self.figure1.add_subplot(111)
        time = datetime.datetime.now()
        fig.set_title(str(time.year) + '/' + str(time.month) +
                      '/' + str(time.day) + '职位分布图')
        fig.bar(data.keys(), num1, label=value1)
        fig.bar(data.keys(), -num2, label=value2)
        # 绘制文字，显示柱状图的值
        for x, y in zip(data.keys(), num1):
            fig.text(x, y + 5, y, ha='center', va='bottom',
                     fontsize=8)  # ,rotation=45)
        for x, y in zip(data.keys(), num2):
            fig.text(x, -y - 8, y, ha='center', va='bottom',
                     fontsize=8)  # ,rotation=45)
        # fig.xaxis.set(rotation=45)
        self.canvas1.show()

    def compareByCity(self, city1, city2):
        self.compare(city1, city2, 1)

    def compareByJob(self, job1, job2):
        self.compare(job1, job2, 0)

    def count(self,value, flag):
        if flag == 0:   # 统计某座城市的招聘信息
            count = self.df.getCityInfo(value)  # 字典{job: num}
        else:       # 统计某种技术的城市分布信息
            count = self.df.getJobsInfo(value)  # 字典{city: num}
        return count

    def countByJob(self, job):
        '''计某种技术的城市分布信息'''
        count = self.df.getJobsInfo(job)  # 字典{job: num}
        print('countByJob')
        self.figure3.clf()
        fig = self.figure3.add_subplot(111)
        fig.set_title('countByJob')
        # fig.plot(count.keys(), count.values())
        fig.bar(count.keys(), count.values(), label='label')
        for x, y in zip(count.keys(), count.values()):
            fig.text(x, y + 5, y, ha='center', va='bottom', fontsize=8)
        self.canvas3.show()



    def countByCity(self, city):
        '''某座城市的招聘信息统计'''
        count = self.df.getCityInfo(city)  # 字典{job: num}
        print('countByCity')
        self.figure2.clf()
        fig = self.figure2.add_subplot(111)
        fig.set_title('countByCity')
        # fig.plot(count.keys(), count.values())
        fig.bar(count.keys(), count.values(), label='label')
        for x, y in zip(count.keys(),count.values()):
            fig.text(x, y + 5, y, ha='center', va='bottom', fontsize=8)
        self.canvas2.show()



    def reDraw(self):
        print('redraw重画')
        # self.picture1()
        # self.picture2()
        # self.picture3()
        self.compareByCity('北京', '深圳')

    def show(self):
        print('show: mainloop')
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
