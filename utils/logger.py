import logging
import logging.handlers

def log(name:str, file=True):
    """
    生成日志
    :param name: 日志文件名
    :param file:
    :return:
    """
    logger = logging.getLogger("iam_test_{}".format(name))
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formater = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
    handler.setFormatter(formater)
    if file:
        file_handler = logging.handlers.RotatingFileHandler(filename='./log/{}.txt'.format(name),
                                                            maxBytes= 100 * 1024 * 1024, backupCount=10, \
                                                            encoding='utf-8')
        file_handler.setFormatter(formater)
        logger.addHandler(file_handler)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger