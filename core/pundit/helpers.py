import re
import signal
from asyncio import *
from glob import glob
from os import path
from random import (
    SystemRandom,
    choice
)
from string import (
    ascii_letters,
    ascii_uppercase,
    digits,
)
from time import (
    time,
    sleep as _sleep
)
from zipfile import (
    BadZipFile,
    ZipFile,
)
from binascii import hexlify
from base64 import b64encode


class submission:
    def __init__(self, userid, storage):
        self.userid = userid
        self.submissions = glob(path.join(storage['master'], 'byusers', f"*{userid}", "*"))
        self.ticket = self.ticket_calc(self.submissions)
        self.timestamp = int(time())

    def __repr__(self):
        return '_'.join(map(str, [self.userid, self.ticket, self.timestamp]))
    
    def ticket_calc(self, submissions):
        return b64encode(hexlify(str(len(submissions)+1).zfill(3).encode())).decode().rstrip()


def gen_rand_str(length):
    return ''.join(SystemRandom()
                   .choice(ascii_letters + digits)
             for _ in range(length))

def tag_responses(message):
    responses = [
        "I'm here, Yo!!",
        "What?!",
        "Wassup human?",
        f"Wassup {message.author.mention}?",
        "I'm listening",
        "Duhh, what??",
        "What now?",
        "What do you want?",
        "What is it that you want now?",
        f"What does {message.author.mention} want now??",
        "I'm still here, lol!!",
        "Mehh!! Are you checking on me?",
        "Don't waste my time :angry:",
        "Here take it, https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "Nah nah, not now!!",
        "I'm busy at the moment, tag me later?",
        "Remember, I was born on 11th of September 2020!!",
        "You rock!!",
        "You're awesome!!",
        "Hey!!",
        "Hello!",
        "Yo!!",
        ]
    return choice(responses)

def isUrl(url):
    regex = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return True if regex.search(url) else False

def unzip(file, topath):
    with ZipFile(file, 'r') as refer:
        refer.extractall(topath)

def timeout_handler(signum, frame):
    raise Exception("Timed Out!")

def plagCheck(pundit, task):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(5)
    try:
        report = pundit.plagCheck(task=task)
        _sleep(7) # to prevent raising exception when control flow passed from here
    except Exception:
        try:
            assert report
        except NameError:
            report = "Request for Moss timed out!!"
    return report
    