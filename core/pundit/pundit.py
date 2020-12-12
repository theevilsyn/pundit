import re
import git
from shutil import copy, rmtree
from distutils.dir_util import copy_tree
from tempfile import TemporaryDirectory as mktemp
from time import time
from urllib.request import (
    urlretrieve,
    URLError
)
from os import (
    getcwd,
    listdir,
    mkdir,
    makedirs,
    path,
    rename
)
from glob import glob
from mosspy import Moss
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import mysql.connector
from core.pundit.helpers import (
    unzip,
    BadZipFile,
    plagCheck,
    gen_rand_str,
)
from core.validator.validator import Validator
from yaml import (
    load,
    SafeLoader,
)

with open("config.yaml", 'r') as file:
    CONFIG = load(file)
    STORAGE = CONFIG['storage']
    PUNDIT = CONFIG['pundit']

with open("tasks.yaml", 'r') as file:
    TASKS = load(file)


class Pundit:
    def __init__(self):
        self.master = STORAGE['master']
        "" if path.exists(self.master) else mkdir(self.master)
        "" if path.exists(path.join(self.master, 'byusers')) else mkdir(
            path.join(self.master, 'byusers'))
        "" if path.exists(path.join(self.master, 'bytasks')) else mkdir(
            path.join(self.master, 'bytasks'))
        "" if path.exists(path.join(self.master, 'formoss')) else mkdir(
            path.join(self.master, 'formoss'))
        return

    def register(self, user):
        name = str(user)
        userid = str(user.id)
        cnx = mysql.connector.connect(
            host="localhost",
            user=STORAGE['db_user'],
            password=STORAGE['db_pass'],
            database=STORAGE['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = cnx.cursor()
        userpath = name.split("#")[0] + userid
        cursor.execute('SELECT * from users where userid="{}"'.format(userid))
        _ = cursor.fetchall()
        if(len(_)):
            return "Hello {user}, looks like you've already registered. If you think this a mistake, please ping any of the admins.".format(user=name.split("#")[0])
        else:
            reg = ("INSERT INTO users"
                   "(name, userid,userpath)"
                   "VALUES (%s, %s, %s)")
            cursor.execute(reg, (name, userid, userpath))
            cnx.commit()
            cnx.close()
            return "Successfully Registered!!"

    def evaluate(self, user, link, ticket, userid=0):
        tmp = mktemp()
        cnx = mysql.connector.connect(
            host="localhost",
            user=STORAGE['db_user'],
            password=STORAGE['db_pass'],
            database=STORAGE['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = cnx.cursor()
        if(userid==0):
            cursor.execute(
                "SELECT userpath from users where userid={}".format(str(user.id)))
        else:
            cursor.execute(
                "SELECT userpath from users where userid={}".format(str(userid)))
            
        userpath = cursor.fetchone()[0]
        "" if path.exists(path.join(self.master, 'byusers', userpath)) else mkdir(
            path.join(self.master, 'byusers', userpath))
        usersubs = len(listdir(path.join(self.master, 'byusers', userpath)))
        try:
            urlretrieve(
                link,
                path.join(tmp.name, "tasks.zip")
            )
            unzip(
                path.join(tmp.name, "tasks.zip"),
                tmp.name,
            )

            if(len(listdir(tmp.name)) > 0):
                mkdir(path.join(self.master, 'byusers', userpath, "{}_{}"
                                .format(
                                    str(usersubs+1).zfill(3),
                                    ticket
                                )))
                mkdir(path.join(tmp.name, "templates"))
                copy(
                    path.join(tmp.name, "tasks.zip"),
                    path.join(tmp.name, "templates", "tasks.zip")
                )
                rename(
                    path.join(tmp.name, "tasks.zip"),
                    path.join(self.master, 'byusers', userpath, "{}_{}/tasks.zip"
                                  .format(
                                      str(usersubs+1).zfill(3),
                                      ticket
                                  )))
                unzip(
                    path.join(self.master, 'byusers', userpath, "{}_{}/tasks.zip"
                                  .format(
                                      str(usersubs+1).zfill(3),
                                      str(ticket)
                                  )),
                    path.join(self.master, 'byusers', userpath, "{}_{}/"
                                  .format(
                                      str(usersubs+1).zfill(3),
                                      str(ticket)
                                  ))
                )
                if(userid==0):
                    report = Validator(
                        submission=ticket,
                        filename=path.join(self.master, userpath, "{}_{}/tasks.zip"
                                            .format(
                                                str(usersubs+1).zfill(3),
                                                ticket
                                            )),
                        user=str(user).split('#')[0],
                        subs=usersubs+1,
                        tmp=tmp
                    ).validate()
                    report = self.award(
                        user,
                        eval(report),
                        ticket.timestamp,
                        str(usersubs+1).zfill(3)+'_'+str(ticket),
                        userpath,
                    )

                else:
                    report = Validator(
                        submission=ticket,
                        filename=path.join(self.master, userpath, "{}_{}/tasks.zip"
                                            .format(
                                                str(usersubs+1).zfill(3),
                                                ticket
                                            )),
                        user="lalallalalalala",
                        subs=usersubs+1,
                        tmp=tmp
                    ).validate()
                    report = self.award(
                        user,
                        eval(report),
                        ticket.timestamp,
                        str(usersubs+1).zfill(3)+'_'+str(ticket),
                        userpath,
                        userid=int(userid)
                    )

                self.rearrangeTasks(
                    userpath,
                    str(usersubs+1).zfill(3)+'_'+str(ticket)
                )
                tmp.cleanup()
                # self.backup(message=f"Submission {str(usersubs+1)} by {str(user)}")
                return report
            else:
                return(
                    False,
                    "Please submit one or more solution!!"
                )

        except Exception as e:
            tmp.cleanup()
            print(e)
            return (
                False,
                "Error, something went wrong :("
            )


    def award(self, user, report, timestamp, ticket, userpath, userid=0):
        cnx = mysql.connector.connect(
            host="localhost",
            user=STORAGE['db_user'],
            password=STORAGE['db_pass'],
            database=STORAGE['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = cnx.cursor()
        if(userid==0):
            cursor.execute(
                "SELECT tasks, entropy from users where userid={}".format(str(user.id)))
        else:
            cursor.execute(
                "SELECT tasks, entropy from users where userid={}".format(str(userid)))

        solved, entropy = (lambda ret: (
            eval(ret[0]), ret[1]))(cursor.fetchone())
        _solved = []
        scoretobe = 0
        roletobe = None
        for task in report['tasks']:
            try:
                if(report['tasks'][task][0] == True and task not in list(map(lambda submission: submission[0], solved))):
                    scoretobe += TASKS[task]['value']
                    _solved.append((task, str(int(time()))))
            except KeyError:
                if(not any(report['tasks'][task]['failed']) and task not in list(map(lambda submission: submission[0], solved))):
                    scoretobe += TASKS[task]['value']
                    _solved.append((task, str(int(time()))))
        if(not len(_solved)):
            report['roletobe'] = None
            return report
        if(userid==0):
            cursor.execute("UPDATE users set tasks=\"{solved}\", score={score}, entropy={entropy} where userid={userid}".format(
                solved=repr(list(map(lambda x: (x, str(int(time()))), list(set(list(map(
                    lambda x: x[0], solved))) | set(list(set(list(map(lambda x: x[0], _solved))))))))),
                score=sum(
                    list(map(lambda x: TASKS[x]['value'], list(set(list(map(lambda x: x[0], solved))) | set(list(map(lambda x: x[0], _solved))))))),
                entropy=str(int(entropy)+timestamp),
                userid=str(user.id))
            )
        else:
            cursor.execute("UPDATE users set tasks=\"{solved}\", score={score}, entropy={entropy} where userid={userid}".format(
                solved=repr(list(map(lambda x: (x, str(int(time()))), list(set(list(map(
                    lambda x: x[0], solved))) | set(list(set(list(map(lambda x: x[0], _solved))))))))),
                score=sum(
                    list(map(lambda x: TASKS[x]['value'], list(set(list(map(lambda x: x[0], solved))) | set(list(map(lambda x: x[0], _solved))))))),
                entropy=str(int(entropy)+timestamp),
                userid=str(userid))
            )

        cnx.commit()
        cnx.close()
        score = sum(
            list(map(lambda x: TASKS[x]['value'], list(set(list(map(lambda x: x[0], solved))) | set(list(map(lambda x: x[0], _solved)))))))
        for task2move in list(map(lambda submisison: submisison[0], _solved)):
            if(path.exists(path.join(self.master, 'formoss', task2move, f"{userpath}"))):
                pass
            else:
                makedirs(path.join(self.master, 'formoss',
                                   task2move, f"{userpath}"))
                copy(
                    path.join(self.master, 'byusers', f"{userpath}", ticket,
                              task2move, f"{task2move}.{TASKS[task2move]['language'][:2]}"),
                    path.join(self.master, 'formoss', task2move,
                              f"{userpath}", f"{task2move}.{TASKS[task2move]['language'][:2]}")
                ) if not TASKS[task2move]['flageval'] else copy(
                    path.join(
                        self.master, 'byusers', f"{userpath}", ticket, task2move, f"{task2move}.txt"),
                    path.join(self.master, 'formoss', task2move,
                              f"{userpath}", f"{task2move}.txt")
                )
        for rolemin in sorted(PUNDIT['playerroles']['roles']):
            if(score >= rolemin):
                roletobe = PUNDIT['playerroles']['roles'][rolemin]
        report['roletobe'] = roletobe
        return report

    def solvedbyuser(self, param):
        cnx = mysql.connector.connect(
            host="localhost",
            user=STORAGE['db_user'],
            password=STORAGE['db_pass'],
            database=STORAGE['database'],
            auth_plugin='mysql_native_password'
        )
        if(type(param) == int):
            execute = "SELECT tasks from users where userid={}".format(param)
        else:
            execute = "SELECT tasks from users where name={}".format(repr(param))
        cursor = cnx.cursor()
        cursor.execute(execute)
        try:
            solved = list(map(lambda x: x[0], eval(cursor.fetchone()[0])))
        except:
            solved = None
        cnx.close()
        return solved

    def leaderboard(self, count=3, all=False):
        cnx = mysql.connector.connect(
            host="localhost",
            user=STORAGE['db_user'],
            password=STORAGE['db_pass'],
            database=STORAGE['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = cnx.cursor()
        cursor.execute(
            "SELECT userid, score from users ORDER BY score DESC, entropy")
        board = cursor.fetchall()
        cnx.close()
        return board if all else board[:count]

    def firstbloods(self):
        cnx = mysql.connector.connect(
            host="localhost",
            user=STORAGE['db_user'],
            password=STORAGE['db_pass'],
            database=STORAGE['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = cnx.cursor()
        cursor.execute(
            "SELECT name, tasks from users ORDER BY score DESC, entropy")
        data = cursor.fetchall()
        data = list(map(lambda data: (data[0], eval(data[1])), data))
        """
		data = [('userid', [('task1', 'timestamp'), ('task2', 'timestamp2')]), ('userid2', [('task1', 'timestamp'), ('task2', 'timestamp2')])...]
		"""
        bloods = {}
        for task in TASKS:
            solved = []
            for entry in data:
                """
                data = [('userid', [('task1', 'timestamp'), ('task2', 'timestamp2')]), ('userid2', [('task1', 'timestamp'), ('task2', 'timestamp2')])...]
                """
                if(any(t[0] == task for t in entry[1])):
                    solved.append((
                        entry[0],
                        int(list(filter(None,
                            list(map(
                                lambda submission, task: submission[1] if submission[0] == task else None,
                                entry[1],
                                [task for _ in range(len(entry[1]))]
                            ))))[0]
                        )
                    ))
            if(solved):
                bloods[task] = sorted(
                    solved, key=lambda x: x[1])[0]
            else:
                bloods[task] = None
        return bloods

    def getScore(self,id_='',name = ''):
        cnx = mysql.connector.connect(
            host="localhost",
            user=STORAGE['db_user'],
            password=STORAGE['db_pass'],
            database=STORAGE['database'],
            auth_plugin='mysql_native_password'
        )
        if name != '':
            cursor = cnx.cursor()
            cursor.execute(
                "SELECT score from users where name={}".format(repr(name)))
            try:
                return cursor.fetchone()
            except:
                return None

        cursor = cnx.cursor()
        cursor.execute(
            "SELECT score from users where userid={}".format(id_))
        try:
            score = cursor.fetchone()
        except:
            return None
        cnx.close()
        return score


    def rearrangeTasks(self, user, ticket):
        for task in [file for file in listdir(path.join(self.master, 'byusers', user, ticket))
                     if path.isdir(path.join(self.master, 'byusers', user, ticket, file))]:
            "" if path.exists(path.join(self.master, 'bytasks', task, user)) else makedirs(
                path.join(self.master, 'bytasks', task, user))
            copy_tree(path.join(self.master, 'byusers', user, ticket, task),
                     path.join(self.master, 'bytasks', task, user, ticket))

    def plainPlagCheck(self, task):
        student_files = glob(path.join(self.master, "formoss", task, "*", "*.txt"))
        try:
            student_notes = [open(File).read() for File in  student_files]
        except:
            return "No such task :("
        
        vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
        similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])
        
        vectors = vectorize(student_notes)
        s_vectors = list(zip(student_files, vectors))
        plagiarism_results = set()
        
        for student_a, text_vector_a in s_vectors:
            new_vectors =s_vectors.copy()
            current_index = new_vectors.index((student_a, text_vector_a))
            del new_vectors[current_index]
            for student_b , text_vector_b in new_vectors:
                sim_score = similarity(text_vector_a, text_vector_b)[0][1]
                student_pair = sorted((student_a, student_b))
                score = (student_pair[0], student_pair[1],sim_score*100)
                plagiarism_results.add(score)
        if(plagiarism_results):
            rets = ""
            for _ in range(len(plagiarism_results)):
                report = plagiarism_results.pop()
                rets += f"{report[0].split(task+'/')[1].split('/')[0]} * && * {report[1].split(task+'/')[1].split('/')[0]} * Percentage: * {report[2]}\n"
            return rets
        else:
            return "No plagiarised content :)"

    def plagCheck(self, language=None, task=None, tasks=[], users=[], usertasks=[]):
        if(task):
            try:
                checker = Moss(PUNDIT['mossid'], TASKS[task]['language'])
            except KeyError:
                return (True,self.plainPlagCheck(task))
            checker.addFilesByWildcard(
                path.join(self.master, "formoss", task, "*", "*"))
            url = checker.send()
            return (False,url)

        elif(tasks):
            reports = {
                "python": "url",
                "c": "url",
            }
            pytasks = list(filter(None, list(map(lambda task: (
                task if TASKS[task]['language'] == 'python' else None), tasks))))
            ctasks = list(filter(None, list(
                map(lambda task: (task if TASKS[task]['language'] == 'c' else None), tasks))))
            cchecker = Moss(PUNDIT['mossid'], "c")
            pychecker = Moss(PUNDIT['mossid'], "python")
            for pytask in pytasks:
                pychecker.addFilesByWildcard(
                    path.join(self.master, "formoss", pytask, "*", "*"))
            for ctask in ctasks:
                cchecker.addFilesByWildcard(
                    path.join(self.master, "formoss", ctask, "*", "*"))
            reports['python'] = pychecker.send()
            reports['c'] = cchecker.send()
            return reports

        elif(language):
            checker = Moss(PUNDIT['mossid'], language)
            checker.addFilesByWildcard(
                path.join(self.master, 'formoss', '*', '*', f'*.{language[:2]}'))
            return checker.send()

        elif(users):
            reports = {
                "python": "url",
                "c": "url",
            }
            pytasks = list(filter(None, list(map(lambda task: (
                task if TASKS[task]['language'] == 'python' else None), usertasks))))
            ctasks = list(filter(None, list(map(lambda task: (
                task if TASKS[task]['language'] == 'c' else None), usertasks))))
            cchecker = Moss(PUNDIT['mossid'], "c")
            pychecker = Moss(PUNDIT['mossid'], "python")
            for user in users:
                for pytask in pytasks:
                    pychecker.addFilesByWildcard(
                        path.join(self.master, "formoss", pytask, f"{user}*", "*"))
                for ctask in ctasks:
                    cchecker.addFilesByWildcard(
                        path.join(self.master, "formoss", ctask, f"{user}*", "*"))
            reports['python'] = pychecker.send()
            reports['c'] = cchecker.send()
            return reports
        else:
            return

    def backup(self, rbranch="backups", message=""):

        tmp = f"/tmp/{gen_rand_str(16)}"
        repo = git.Repo.clone_from(
            f"https://gitlab-ci-token:{STORAGE['token']}@{re.sub(r'https?://|(www.)?','',STORAGE['repo'])}",
            to_path=tmp,
            branch=rbranch,
        )
        copy_tree(path.join(self.master), tmp)
        repo.index.add(['*'])
        repo.index.commit(message)
        repo.git.push('--set-upstream', 'origin', rbranch)
        rmtree(tmp)