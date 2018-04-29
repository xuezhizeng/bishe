# import numpy as np
# import tkinter as tk
# from random import random
# from math import sqrt
# import matplotlib.pyplot as plt
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# from matplotlib import animation
#
# def pe():
#     #     输入框1  输入框2      输入框3    复选框
#     print(N.get(), Energy.get(), Step.get(), State.get())
#
#
# def _quit():
#     root.quit()
#     root.destroy()
#
#
# def step(atom, Dv):
#     for i in range(len(atom) - 2):
#         dv = -Dv + Dv * 2 * random()
#         if (atom[i]['v'] + dv) ** 2 / 2 - atom[i]['e'] < atom['demon']['e']:
#             atom['demon']['e'] += -(atom[i]['v'] + dv) ** 2 / 2 + atom[i]['e']
#             atom[i]['v'] = atom[i]['v'] + dv
#             atom[i]['e'] = (atom[i]['v']) ** 2 / 2
#     return atom
#
#
# def enter():
#     # gas()  # 气体状态计算
#     draw_picture()  # 画出图像
#
#
# def gas():
#     #     输入框1  输入框2      输入框3    复选框
#     ideal_gas(N.get(), Energy.get(), Step.get(), State.get())
#
#
# def ideal_gas(
#         N,  # Number of particles 粒子数量
#         totalEnergy,  # total of demon and system energy 系统总能量
#         steps,  # number of simulation steps 模拟步骤
#         state,  # Initial state 1 or 2  初始状态
# ):
#     atom = {}
#     for i in range(N):
#         atom[i] = {}
#         atom[i]['e'] = totalEnergy / N * (2 - state)  # depending on state
#         atom[i]['v'] = sqrt(atom[i]['e'] * 2)  # mass=1
#
#     atom['demon'] = {'e': totalEnergy * (state - 1)}  # depending on state
#     print(atom)
#     for i in range(steps):
#         atom = step(atom, sqrt(2 * totalEnergy / N / 10))
#         atom['demonh'] = atom.get('demonh', []) + [(atom['demon']['e'])]  # store energy of demon for figure
#     print(atom)
#     return atom
#
#
#
# def draw_picture_v2():
#     # fig = plt.figure()
#     fig = figure1.add_subplot(111)
#     data = np.random.random((255, 255))
#     im = plt.imshow(data, cmap='gray')
#
#     # animation function.  This is called sequentially
#
#     def animate(i):
#         data = np.random.random((255, 255))
#         im.set_array(data)
#         return [im]
#
#     anim = animation.FuncAnimation(
#         fig, animate, frames=200, interval=60, blit=True)
#     # plt.show()
#
#
# def draw_picture():
#     ax = figure1.add_subplot(111)
#     X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
#     C, S = np.cos(X), np.sin(X)
#
#     ax.plot(X, C)
#     ax.plot(X, S)
#     # ax.convert_xunits("J")  # x轴上的单位
#     ax.set_xlabel("N")
#     ax.set_ylabel("Energy")
#     ax.set_title('Energy')
#     # plt.pause()
#     # figure1.properties()
#     figure1.clf()
#
#
# def draw_picture_v1():
#     # plt.figure(figsize=(8, 5), dpi=80)
#     # ax = plt.subplot(111)
#     ax = figure1.add_subplot(111)
#     ax.spines['right'].set_color('none')
#     ax.spines['top'].set_color('none')
#     ax.xaxis.set_ticks_position('bottom')
#     ax.spines['bottom'].set_position(('data', 0))
#     ax.yaxis.set_ticks_position('left')
#     ax.spines['left'].set_position(('data', 0))
#
#     X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
#     C, S = np.cos(X), np.sin(X)
#
#     plt.plot(X, C, color="blue", linewidth=2.5, linestyle="-", label="cosine",
#              zorder=-1)
#     plt.plot(X, S, color="red", linewidth=2.5, linestyle="-", label="sine",
#              zorder=-2)
#
#     plt.xlim(X.min() * 1.1, X.max() * 1.1)
#     plt.xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi],
#                [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
#
#     plt.ylim(C.min() * 1.1, C.max() * 1.1)
#     plt.yticks([-1, +1],
#                [r'$-1$', r'$+1$'])
#
#     plt.legend(loc='upper left', frameon=False)
#
#     t = 2 * np.pi / 3
#     plt.plot([t, t], [0, np.cos(t)],
#              color='blue', linewidth=1.5, linestyle="--")
#     plt.scatter([t, ], [np.cos(t), ], 50, color='blue')
#     plt.annotate(r'$\sin(\frac{2\pi}{3})=\frac{\sqrt{3}}{2}$',
#                  xy=(t, np.sin(t)), xycoords='data',
#                  xytext=(+10, +30), textcoords='offset points', fontsize=16,
#                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
#
#     plt.plot([t, t], [0, np.sin(t)],
#              color='red', linewidth=1.5, linestyle="--")
#     plt.scatter([t, ], [np.sin(t), ], 50, color='red')
#     plt.annotate(r'$\cos(\frac{2\pi}{3})=-\frac{1}{2}$',
#                  xy=(t, np.cos(t)), xycoords='data',
#                  xytext=(-90, -50), textcoords='offset points', fontsize=16,
#                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
#
#     for label in ax.get_xticklabels() + ax.get_yticklabels():
#         label.set_fontsize(16)
#         label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.65))
#
#     # plt.savefig("../figures/exercice_10.png", dpi=72)
#     # plt.show()
#
#
# def draw_picture_v0():
#     a1 = figure1.add_subplot(111)
#     sys_e = []
#     x = []
#     total_e = []
#     for N in range(50, 501, 50):
#         atom = ideal_gas(N, 500, 1000, 1)
#         sys_e.append(500 - atom['demon']['e'])
#         x.append(N)
#         total_e.append(500)
#     a1.plot(x, total_e)
#     a1.plot(x, sys_e)
#     a1.convert_xunits('J')  # x轴上的单位
#     a1.set_xlabel("N")
#     a1.set_ylabel("Energy")
#     a1.set_title('Energy')
#
#     a2 = figure2.add_subplot(111)
#     fr = {}
#     f = []
#     x = []
#     for i in range(N):
#         fr[atom[i]['v'] // 1] = fr.get(atom[i]['v'] // 1, 0) + 1
#     for key in fr:
#         x.append(key)
#         f.append(fr[key])
#     a2.bar(x, f, width=1)
#     a2.convert_xunits('J')
#     a2.set_xlabel("v")
#     a2.set_ylabel("Frequency")
#     a2.set_title('V-Frequency')
#
#     a3 = figure3.add_subplot(111)
#     fr = {}
#     f = []
#     x = []
#     for i in range(Step):
#         fr[atom['demonh'][i] // 1] = fr.get(atom['demonh'][i] // 1, 0) + 1
#     for key in fr:
#         x.append(key)
#         f.append(fr[key])
#     a3.bar(x, f, width=1)
#     a3.convert_xunits('J')
#     a3.set_xlabel("Demon Energy")
#     a3.set_ylabel("Frequency")
#     a3.set_title('Demon Energy-Frequency')
#
#
# def p1():
#     # 显示一张图片
#     canvas = FigureCanvasTkAgg(figure1, root)
#     canvas.get_tk_widget().pack(anchor=tk.E, side=tk.RIGHT, expand=1)
#     canvas.show()
#
#
# def p2():
#     canvas = FigureCanvasTkAgg(figure2, root)
#     canvas.get_tk_widget().pack(anchor=tk.E, side=tk.RIGHT, expand=1)
#     canvas.show()
#
#
# def p3():
#     canvas = FigureCanvasTkAgg(figure3, root)
#     canvas.get_tk_widget().pack(anchor=tk.E, side=tk.RIGHT, expand=1)
#     canvas.show()
#
#
# root = tk.Tk()
# root.wm_title('Gas')
#
# ##################### 三张空白画布 ########################
# figure1 = Figure(figsize=(5, 4), dpi=100)
# figure2 = Figure(figsize=(5, 4), dpi=100)
# figure3 = Figure(figsize=(5, 4), dpi=100)
# # 在root下面呈现画布1
# canvas = FigureCanvasTkAgg(figure=figure1, master=root)
# canvas.get_tk_widget().pack(anchor=tk.E, expand=1)
#
# root.geometry('960x600')
#
# ################## 下面是创建了两个按钮 ###################
# button_enter = tk.Button(root, text='Enter', command=enter)
# button_enter.pack()
# # button的高、宽、所在位置
# button_enter.place(height=30, width=100, x=75, y=500)
#
# button_quit = tk.Button(root, text='Quit', command=_quit)
# button_quit.pack()
# # button的高、宽、所在位置
# button_quit.place(height=30, width=100, x=225, y=500)
#
# ################## 下面创建三个标签 ######################
# label_N = tk.Label(root, text='Please input the number of atoms:')
# label_N.pack()
# label_N.place(x=20, y=100, anchor=tk.NW)
#
# label_Energy = tk.Label(root, text='Please input the energy of atoms:')
# label_Energy.pack()
# label_Energy.place(x=20, y=150, anchor=tk.NW)
#
# label_Step = tk.Label(root, text='Please input the step you want to go:')
# label_Step.pack()
# label_Step.place(x=20, y=200, anchor=tk.NW)
#
# ################## 下面是创建三个输入框 ##################
# N = tk.IntVar()     # 整型变量
# entry_N = tk.Entry(root, textvariable=N)
# entry_N.pack()
# entry_N.place(in_=label_N, relx=1.03)
#
# Energy = tk.IntVar()    # 整型变量
# entry_Energy = tk.Entry(root, textvariable=Energy)
# entry_Energy.pack()
# entry_Energy.place(in_=label_Energy, relx=1.03)
#
# Step = tk.IntVar()  # 整型变量
# entry_Step = tk.Entry(root, textvariable=Step)
# entry_Step.pack()
# entry_Step.place(in_=label_Step, relx=1.03)
#
# ################ 下面创建两个单选框 #####################
# State = tk.IntVar()
# radiobutton_demon = tk.Radiobutton(root, variable=State, text='Give all the energy to demon', value=1)
# radiobutton_demon.pack()
# radiobutton_demon.place(x=20, y=250)
#
# radiobutton_system = tk.Radiobutton(root, variable=State, text='Give all the energy to system', value=2)
# radiobutton_system.pack()
# radiobutton_system.place(x=20, y=300)
#
# ################## 下面创建了三个按钮 ###############
# button_figure1 = tk.Button(root, text='Figure1', command=p1)
# button_figure1.pack()
# button_figure1.place(height=30, width=100, x=20, y=350)
#
# button_figure2 = tk.Button(root, text='Figure2', command=p2)
# button_figure2.pack()
# button_figure2.place(height=30, width=100, x=20, y=400)
#
# button_figure3 = tk.Button(root, text='Figure3', command=p3)
# button_figure3.pack()
# button_figure3.place(height=30, width=100, x=20, y=450)
#
# root.mainloop()
#
#
#
#


####################################################################################
####################################################################################
####################################################################################

# !/usr/bin/env python
# coding:utf-8
import numpy as np
import tkinter as tk
import matplotlib
import dataoptions as dp
import datetime
# matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# 下面两行解决中文显示问题
import pylab
pylab.mpl.rcParams['font.sans-serif'] = ['SimHei']


def drawPic():
    try:
        sampleCount = int(inputEntry.get())
    except:
        sampleCount = 50
        print('请输入整数')
        inputEntry.delete(0, tk.END)
        inputEntry.insert(0, '50')

    # 清空图像，以使得前后两次绘制的图像不会重叠
    # figure.clf()
    # a = figure.add_subplot(111)

    df = dp.DataOptions()
    #

    # info=df.getJobsInfo('C++')
    # print(info)

    num = df.getJobInCity()
    # print(num)
    # sorted返回的是一个列表
    num = dict(sorted(num.items(), key=lambda x: x[1], reverse=True)[:10])

    # 清空图像，以使得前后两次绘制的图像不会重叠
    figure.clf()
    fig = figure.add_subplot(111)

    # plt.figure(figsize=(8, 5), dpi=80)
    # ax=plt.subplot(111)

    # 用来正常显示中文标签和正负号
    # fig.set_sketch_params()
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['axes.unicode_minus'] = False


    time =  datetime.datetime.now()

    fig.set_title(str(time.year) + '/' + str(time.month) + '/' + str(time.day) + '职位分布图')
    fig.bar(num.keys(), num.values(), label="职位数")
    # fig.bar()

    # 绘制文字，显示柱状图的值
    for x, y in zip(num.keys(), num.values()):
        # plt.text(x, y + 5, y, ha='center', va='bottom', fontsize=12)
        fig.text(x, y + 5, y, ha='center', va='bottom', fontsize=12)
        # pass


    # fig.set_title('Demo: Draw N Random Dot')
    fig.legend()
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
