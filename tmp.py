from multiprocessing import Pool
import time
import functools


def timer(func):
    # 把原始函数的__name__等属性复制到wrapper()函数中，否则，有些依赖函数签名的代码执行就会出错。
    @functools.wraps(func)
    def wrapper(*args, **kw):
        start = time.time()
        func(*args, **kw)
        end = time.time()
        print('运行秒数：', str(end - start))

    return wrapper


@timer
def index(s):
    # print(str(s))/
    print(s)


if __name__ == '__main__':
    pool = Pool(processes=2)
    pool.map_async(index, ['linux', 'python', '嵌入式'])
    pool.close()
    pool.join()

#
# func()


#
#
# @timer
# def get_zhaopin(page):
#     print('jjjjj')
#     print(page)
#
# if __name__ == '__main__':
#     # processes: 维持执行的总进程数
#     pool = Pool(processes=2)
#     pages=6
#
#     # apply_async(func[, args[, kwds[, callback]]]) => 非阻塞方式
#     # apply(func[, args[, kwds]]) => 阻塞方式
#     # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
#     pool.map_async(get_zhaopin,range(1,pages+1))
#     # pool.apply_async(get_zhaopin, range(1, pages + 1))
#     # pool.apply_async(get_zhaopin,range(1,pages+1))
#
#     # 执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
#     pool.close()
#     # 调用join之前，先调用close函数，否则会出错。
#     pool.join()
#
#
#
