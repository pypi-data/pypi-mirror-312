import logging
def create_logger():

    logger = logging.getLogger('log')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s]%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # 创建文件处理器，并将日志写入文件
    file_handler = logging.FileHandler('my_log_file.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


logger = create_logger()
