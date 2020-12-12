import logging

def init():
    logger = logging.getLogger("pundit")
    logger.setLevel(logging.DEBUG)
    ch = logging.FileHandler("../pundit.log")
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[*] %(asctime)s - %(levelname)s - %(message)s ')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

if __name__=='__main__':
    init()