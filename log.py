import logging


# def get_a_log(job):
class log(object):
    """docstring for logger"""

    def __init__(self, file):
        '''入参是日志文件'''
        super(log, self).__init__()
        self.file = file
        # 创建一个logger
        self.logger = logging.getLogger(self.file)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(file + '.log')
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    # return sele.logger

    def saveInfo(self, e, serise):
        '''
        记录数据库存储时的错误
        :param e: 系统抛出的错误信息
        :param serise: 存储出错的数据
        :return: 无返回内容
        '''
        self.logger.info(e)
        s = 'err data:'
        for x in range(serise.__len__()):
            s += '\n' + str(serise.index[x]) + ': ' + str(serise[x])
        self.logger.info(s)
