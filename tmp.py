# !/usr/bin/env python
# coding:utf-8
# 绘图模块：draw.py
# 封装成pictures类
import tkinter as tk
import dataoptions as dp
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

    def jobsInCitys():
        pass


def picture1():
    # df = dp.DataOptions()
    # num = df.getJobInCity()
    # # sorted返回的是一个列表
    # num = dict(sorted(num.items(), key=lambda x: x[1], reverse=True)[:10])
    #
    # # 清空图像，以使得前后两次绘制的图像不会重叠
    # figure1.clf()
    # fig = figure1.add_subplot(111)
    # time = datetime.datetime.now()
    # fig.set_title(str(time.year) + '/' + str(time.month) +
    #               '/' + str(time.day) + '职位分布图')
    # fig.bar(num.keys(), num.values(), label="职位数")
    # # 绘制文字，显示柱状图的值
    # for x, y in zip(num.keys(), num.values()):
    #     fig.text(x, y + 5, y, ha='center', va='bottom', fontsize=12)
    # canvas1.show()

    fig = figure1.add_subplot(111)
    fig.set_title('picture1')
    fig.plot([1, 2, 3, 4, 5, 6], [1, 4, 9, 16, 25, 36])
    canvas1.show()


def picture2():
    # figure2.clf()
    fig = figure2.add_subplot(111)
    fig.set_title('picture2')
    fig.plot([1, 2, 3, 4, 5, 6], [1, 4, 9, 16, 25, 36])
    canvas2.show()


def picture3():
    # figure3.clf()
    fig = figure3.add_subplot(111)
    fig.set_title('picture3')
    fig.plot([1, 2, 3, 4, 5, 6], [6,5,4,3,2,1])
    canvas3.show()


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


def clickMe():
    action.configure(text='Hello\n ')
    picture1()
    picture2()
    picture3()
    action.configure(state='disabled')  # Disable the Button Widget


if __name__ == '__main__':
    root = tk.Tk()

    # Adding a Combobox
    city = tk.StringVar()
    cityChosen = ttk.Combobox(root, width=12, textvariable=city)
    # cityChosen['values'] = ('java', 'c++', 'python', 'c#', 'c', 'linux', '大数据', 'web', '数据库')
    cityChosen['values'] = ('北京', '上海', '广州', '深圳', '南京', '成都', '杭州', '武汉', '西安', '郑州')
    cityChosen.grid(row=0, rowspan=3, column=0, columnspan=2, sticky='W')
    cityChosen.current(2)  # 设置初始显示值，值为元组['values']的下标
    cityChosen.config(state='readonly')  # 设为只读模式
    createToolTip(cityChosen, '选择城市.')

    # Adding a Combobox
    job = tk.StringVar()
    jobChosen = ttk.Combobox(root, width=12, textvariable=job)
    jobChosen['values'] = ('java', 'c++', 'python', 'c#', 'c', 'linux', '大数据', 'web', '数据库')
    # cityChosen['values'] = ('北京', '上海', '广州', '深圳', '南京', '成都', '杭州', '武汉', '西安', '郑州')
    jobChosen.grid(row=0, rowspan=3, column=3, columnspan=2, sticky='W')
    jobChosen.current(2)  # 设置初始显示值，值为元组['values']的下标
    jobChosen.config(state='readonly')  # 设为只读模式
    createToolTip(cityChosen, '选择技术.')

    # Adding a Button
    action = ttk.Button(root, text="后台更新数据", width=10, command=clickMe)
    # column:在竖直方向占用单元格数; ipady: 竖直方向内边距
    action.grid(row=0, rowspan=3, column=8, columnspan=2)  # , ipady=7)

    # 在Tk的GUI上放置一个画布，并用.grid()来调整布局
    # figure1 = Figure(figsize=(4, 6), dpi=100, facecolor='red', edgecolor='green')
    figure1 = Figure(figsize=(4, 6), dpi=100)
    canvas1 = FigureCanvasTkAgg(figure1, master=root)
    canvas1.show()
    canvas1.get_tk_widget().grid(row=3, rowspan=22, column=0, columnspan=6)

    # figure2 = Figure(figsize=(4, 3), dpi=100, facecolor='yellow')
    figure2 = Figure(figsize=(4, 3), dpi=100)
    canvas2 = FigureCanvasTkAgg(figure2, master=root)
    canvas2.show()
    canvas2.get_tk_widget().grid(row=3, rowspan=11, column=6, columnspan=5)

    # figure3 = Figure(figsize=(4, 3), dpi=100, facecolor='blue')
    figure3 = Figure(figsize=(4, 3), dpi=100)
    canvas3 = FigureCanvasTkAgg(figure3, master=root)
    canvas3.show()
    canvas3.get_tk_widget().grid(row=14, rowspan=11, column=6, columnspan=5)

    # # 放置标签、文本框和按钮等部件，并设置文本框的默认值和按钮的事件函数
    # tk.Label(root, text='请输入样本数量：').grid(row=1, column=0)
    # inputEntry = tk.Entry(root)
    # inputEntry.grid(row=1, column=1)
    # inputEntry.insert(0, '50')
    # tk.Button(root, text='画图', command=drawPic).grid(
    #     row=1, column=2, columnspan=3)

    # 启动事件循环
    root.mainloop()
