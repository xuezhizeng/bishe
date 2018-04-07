# !/usr/bin/env python
# coding:utf-8
import numpy as np
import tkinter as tk
import matplotlib

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def drawPic():
    try:
        sampleCount = int(inputEntry.get())
    except:
        sampleCount = 50
        print('请输入整数')
        inputEntry.delete(0, tk.END)
        inputEntry.insert(0, '50')

    # 清空图像，以使得前后两次绘制的图像不会重叠
    figure.clf()
    a = figure.add_subplot(111)

    a.spines['right'].set_color('none')
    a.spines['top'].set_color('none')
    a.xaxis.set_ticks_position('bottom')
    a.spines['bottom'].set_position(('data', 0))
    a.yaxis.set_ticks_position('left')
    a.spines['left'].set_position(('data', 0))

    # 绘制这些随机点的散点图，颜色随机选取
    # a.scatter(x, y, s=3, color=color[np.random.randint(len(color))])

    X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
    C, S = np.cos(X), np.sin(X)
    # a.scatter(X, C)
    # a.scatter(X, S)
    a.plot(X, C, color="blue", linewidth=2.5, linestyle="-", label="cosine",
             zorder=-1)
    a.plot(X, S, color="red", linewidth=2.5, linestyle="-", label="sine",
             zorder=-2)


    a.set_xlim(X.min() * 1.1, X.max() * 1.1)
    a.set_xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi],
             [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])

    a.set_ylim(C.min() * 1.1, C.max() * 1.1)
    a.set_yticks([-1, +1],
             [r'$-1$', r'$+1$'])

    a.legend(loc='upper left', frameon=False)

    t = 2 * np.pi / 3
    a.plot([t, t], [0, np.cos(t)],
           color='blue', linewidth=1.5, linestyle="--")
    a.scatter([t, ], [np.cos(t), ], 50, color='blue')
    a.annotate(r'$\sin(\frac{2\pi}{3})=\frac{\sqrt{3}}{2}$',
               xy=(t, np.sin(t)), xycoords='data',
               xytext=(+10, +30), textcoords='offset points', fontsize=16,
               arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

    a.plot([t, t], [0, np.sin(t)],
           color='red', linewidth=1.5, linestyle="--")
    a.scatter([t, ], [np.sin(t), ], 50, color='red')
    a.annotate(r'$\cos(\frac{2\pi}{3})=-\frac{1}{2}$',
               xy=(t, np.cos(t)), xycoords='data',
               xytext=(-90, -50), textcoords='offset points', fontsize=16,
               arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

    for label in a.get_xticklabels() + a.get_yticklabels():
        label.set_fontsize(16)
        label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.65))

    # a.savefig("../figures/exercice_10.png", dpi=72)
    # a.show()

    a.set_title('Demo: Draw N Random Dot')
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
    tk.Button(root, text='画图', command=drawPic).grid(row=1, column=2, columnspan=3)

    # 启动事件循环
    root.mainloop()
