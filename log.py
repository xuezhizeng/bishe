import logging
import sys


class log(object):
    """docstring for logger"""

    def __init__(self,logname):
        '''入参是日志文件'''
        super(log, self).__init__()
        logfile = 'log.log'
        # 创建一个logger
        # 一定要这样，不然每个类都创建一个log，那么所有文件公用一个相同的log，就会重复打印日志
        self.logger = logging.getLogger(logname)
        self.logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s][%(name)s][%(thread)d][%(levelname)s]%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)


    def saveInfo(self, s=None):
        '''
        记录数据库存储时的错误
        :param s: 信息
        :return: 无返回内容
        '''
        tmp = '[' + sys._getframe().f_back.f_code.co_name + '():' + \
              str(sys._getframe().f_back.f_lineno) + ']## '
        self.logger.info(tmp + s)
