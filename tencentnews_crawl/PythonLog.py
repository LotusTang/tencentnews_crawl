import logging
import datetime


def setlogger(old_handler):
    # create logger with 'spam_application'
    logger = logging.getLogger('tencentenws_application')
    # 每次先移除老的handler
    for handler in old_handler:
        logger.removeHandler(handler)
    old_handler.clear()

    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    time_str = str(datetime.datetime.now())
    time_str = time_str[:time_str.rindex(":")].replace(":", " ")
    file_name = 'F:\\news_log\\' + time_str + '.log'
    fh = logging.FileHandler(file_name)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    old_handler.append(fh)
    old_handler.append(ch)


# logger.info('creating an instance of auxiliary_module.Auxiliary')
#
# logger.info('created an instance of auxiliary_module.Auxiliary')
# logger.info('calling auxiliary_module.Auxiliary.do_something')
#
# logger.info('finished auxiliary_module.Auxiliary.do_something')
# logger.info('calling auxiliary_module.some_function()')
#
# logger.info('done with auxiliary_module.some_function()')












