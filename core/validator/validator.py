import re
import shlex
import socket
from os import (
    getcwd,
    mkdir,
    path,
)
from random import randrange
from shutil import copy
from subprocess import call as exe
from threading import (
    Thread,
    Timer,
)
from time import sleep

from pwn import process


class Validator:
    def __init__(self, submission, filename, user, subs, tmp):
        self.user = user
        self.tag = subs
        self.tmp = tmp
        self.submission = submission
        self.filename = filename

    def recv(self):
        len = int(self.conn.recv(8))
        return self.conn.recv(len)

    def replace(self, old, new, filename):
        buf = open(filename).read().replace(old, new)
        open(filename, 'w').write(buf)

    def check(self):
        self.vport = randrange(10000, 65530)
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1,
        )
        sock.bind(("", self.vport))
        sock.listen(10)
        self.conn, _ = sock.accept()
        status = self.recv().decode()
        return status

    def container(self):
        copy(
            "tasks.yaml",
            path.join(self.tmp.name, "templates", "tasks.yaml")
        )
        copy(
            path.join("models", "templates", "Dockerfile"),
            path.join(self.tmp.name, path.join("templates", "Dockerfile"))
        )
        copy(
            path.join("models", "templates", "runner.py"),
            path.join(self.tmp.name, "templates", "runner.py")
        )
        copy(
            path.join("models", "templates", "requirements.txt"),
            path.join(self.tmp.name, "templates", "requirements.txt")
        )
        self.replace(
            "SEDMYZIP",
            path.join(getcwd(), self.filename),
            path.join(self.tmp.name, "templates", "Dockerfile")
        )
        self.replace(
            "SEDMYSUBMISSION",
            repr(self.submission),
            path.join(self.tmp.name, "templates", "Dockerfile")
        )
        try:
            self.replace(
                "SEDMYPORT",
                str(self.vport),
                path.join(self.tmp.name, "templates", "Dockerfile")
            )
        except AttributeError:
            sleep(0.5)
            self.replace(
                "SEDMYPORT",
                str(self.vport),
                path.join(self.tmp.name, "templates", "Dockerfile")
            )
        exe(["docker", "build", "--tag", "{}.{}"
             .format(
                 re.sub(r'[^0-9a-zA-Z]+', '', self.user).lower(),
                 self.tag
             ), path.join(self.tmp.name, "templates")])
        exe(["docker", "run", "-t", "-i", "--rm", "{}.{}"
             .format(
                 re.sub(r'[^0-9a-zA-Z]+', '', self.user).lower(),
                 self.tag,
             )])

    def validate(self):
        cnt = Thread(target=self.container)
        cnt.start()
        report = self.check()
        exe(["docker", "image", "rm", "-f", "{}.{}"
             .format(
                 re.sub(r'[^0-9a-zA-Z]+', '', self.user).lower(),
                 self.tag
             )])
        return report
