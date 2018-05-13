import logging
import time


class log(object):
    """docstring for logger"""

    def __init__(self):
        '''入参是日志文件'''
        super(log, self).__init__()
        t = time.gmtime()
        logfile = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday) + '-' + str(t.tm_hour) + '-' + str(
            t.tm_min) + '-' + str(t.tm_sec) + '.log'
        logfile = 'log.log'
        # 创建一个logger
        self.logger = logging.getLogger(logfile)
        self.logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        # formatter = logging.Formatter(
        #     '[%(asctime)s][%(thread)d][%(filename)s +%(lineno)d][%(funcName)s][%(levelname)s] ## %(message)s')
        formatter = logging.Formatter(
            '[%(asctime)s][%(thread)d][%(levelname)s] ## %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    # return sele.logger

    def saveInfo(self, s=None):
        '''
        记录数据库存储时的错误
        :param e: 系统抛出的错误信息
        :param serise: 存储出错的数据
        :return: 无返回内容
        '''
        pass
        # print(s)
        # if s:
        #     self.logger.info(s)
        # if e:
        #     self.logger.debug(e)

        # s = 'err data:'
        # for x in range(serise.__len__()):
        #     s += '\n' + str(serise.index[x]) + ': ' + str(serise[x])
        # self.logger.info(s)
