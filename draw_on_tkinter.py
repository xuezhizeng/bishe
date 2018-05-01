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

# 下面两行解决中文显示问题
import pylab
pylab.mpl.rcParams['font.sans-serif'] = ['SimHei']


class draw(object):
    """绘图模块，专注画图"""

    def __init__(self, ):
        super(draw, self).__init__()

    def jobsInCitys(slef):
        pass


def drawPic():
    try:
        sampleCount = int(inputEntry.get())
    except:
        sampleCount = 50
        print('请输入整数')
        inputEntry.delete(0, tk.END)
        inputEntry.insert(0, '50')

    df = dp.DataOptions()
    num = df.getJobInCity()
    # sorted返回的是一个列表
    num = dict(sorted(num.items(), key=lambda x: x[1], reverse=True)[:10])

    # 清空图像，以使得前后两次绘制的图像不会重叠
    figure.clf()
    fig = figure.add_subplot(111)

    time = datetime.datetime.now()

    fig.set_title(str(time.year) + '/' + str(time.month) +
                  '/' + str(time.day) + '职位分布图')
    fig.bar(num.keys(), num.values(), label="职位数")

    # 绘制文字，显示柱状图的值
    for x, y in zip(num.keys(), num.values()):
        fig.text(x, y + 5, y, ha='center', va='bottom', fontsize=12)

    canvas.show()


if __name__ == '__main__':
    root = tk.Tk()
    # 在Tk的GUI上放置一个画布，并用.grid()来调整布局
    figure = Figure(figsize=(5, 4), dpi=100)

    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.show()
    canvas.get_tk_widget().grid(row=0, columnspan=3)

    # 放置标签、文本框和按钮等部件，并设置文本框的默认值和按钮的事件函数
    tk.Label(root, text='请输入样本数量：').grid(row=1, column=0)
    inputEntry = tk.Entry(root)
    inputEntry.grid(row=1, column=1)
    inputEntry.insert(0, '50')
    tk.Button(root, text='画图', command=drawPic).grid(
        row=1, column=2, columnspan=3)

    # 启动事件循环
    root.mainloop()
