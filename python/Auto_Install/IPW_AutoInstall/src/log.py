import logging, sys, os
from logging.handlers import RotatingFileHandler


_cons = logging.getLogger("console")
_file = logging.getLogger("file")
_all = logging.getLogger("all")
_print = logging.getLogger("print")

def Init() :

    global _cons, _file, _all

    # create formatter
    _formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)s - %(funcName)s - %(levelname)s | %(message)s')
    _formatter2 = logging.Formatter('%(message)s')

    if not os.path.exists("log"):
        os.makedirs("log")

    # create handler
    _handler1 = RotatingFileHandler("log/install.log", 'a', 10000000, 9)
    _handler1.setFormatter(_formatter)

    # create handler
    _handler2 = logging.StreamHandler(sys.stdout)
    _handler2.setFormatter(_formatter)

    # create handler
    _handler3 = logging.StreamHandler(sys.stdout)
    _handler3.setFormatter(_formatter2)

    # config console logger
    _cons.addHandler(_handler2)
    _cons.setLevel(logging.DEBUG)

    # config file logger
    _file.addHandler(_handler1)
    _file.setLevel(logging.DEBUG)

    # config all logger
    _all.addHandler(_handler1)
    _all.addHandler(_handler2)
    _all.setLevel(logging.DEBUG)

    # config all logger
    _print.addHandler(_handler1)
    _print.addHandler(_handler3)
    _print.setLevel(logging.DEBUG)

    _file.debug("============= Start Log ==============")





