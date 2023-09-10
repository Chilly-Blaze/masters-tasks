#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import datetime
from typing import List, Tuple
import uuid
import json
import language
import requests
from copy import deepcopy

# 全局常量
defaultConf = 'conf.json'
defaultHelp = 'help.txt'
mode = ['t', 'h', 's']
sync = ['u', 'd', 'r', 'i']
resposive = ['', 'q', '?', 'j', 'n', 'f'] + mode + list(language.language.keys()) + sync
line = '─' * 50
taskMax = 0
historyMax = 20
serverPort = 8000
hiddenMax = 0


# 存储类
# ------
class Hidden:

    def __init__(self, name='', color=0):
        self.name = name
        self.color = color

    def isContain(self, s: str):
        return s in self.name


class Task(Hidden):

    def __init__(self, name='', color=0, repeat=False):
        super().__init__(name, color)
        self.repeat = repeat
        self.count = 0
        self.createTime = int(datetime.datetime.now().timestamp())


class History:

    def __init__(self, t=Task()):
        self.task = t
        self.doneTime = int(datetime.datetime.now().timestamp())
        self.duringTime = self.doneTime - t.createTime

    def isContain(self, s: str):
        return s in self.task.name


class Synchronizer:

    def __init__(self, ip='', token=''):
        self.ip = ip
        self.port = serverPort
        self.token = token

    def isActive(self):
        return self.ip != ''

    def request(self, route, f, json=None):
        return f(
            f'http://{self.ip}:{self.port}/{route}',
            headers={'token': self.token},
            json=json,
        )

    def dealSync(self, c: str):
        if c == sync[2]:
            config.synchronizer.reset()
        elif c == sync[3]:
            print(
                lang['fhint'][14].format(
                    config.id, self.token if self.token != '' else lang['ehint'][4]
                )
            )
        elif not (self.isActive()):
            if input(lang['fhint'][0]).lower() == 'n':
                return
            else:
                self.reset()
        elif c == sync[0]:
            config.synchronizer.upload()
        else:
            config.synchronizer.download()

    def isok(self, resp: requests.Response):
        if not (resp.json()['ok']):
            raise Exception(resp.json()['err'])
        return resp.json()

    def ping(self):
        print(lang['fhint'][2])
        try:
            self.isok(self.request('ping', requests.get))
        except Exception as e:
            print(lang['fhint'][4].format(self.ip, self.token))
            print(lang['err'][2].format(e))
            return False
        else:
            print(lang['fhint'][3])
            return True

    def upload(self):
        if self.ping():
            if input(lang['fhint'][5]) == 'n':
                return
            print(lang['fhint'][6])
            try:
                body = {'id': config.id, 'data': obj2json(config)}
                self.isok(self.request('upload', requests.post, body))
            except Exception as e:
                print(lang['fhint'][8].format(e))
                print(lang['err'][2].format(e))
            else:
                print(lang['fhint'][7])

    def download(self):
        if self.ping():
            com = input(lang['fhint'][9])
            if com == 'q':
                return
            elif com == '2':
                id = input(lang['fhint'][10])
            else:
                id = config.id
            try:
                dic = json.loads(
                    self.isok(self.request(f'download/{id}', requests.post))['data']
                )
                if com == '2':
                    path = j(f'{id}.json')
                    with open(path, 'w') as f:
                        f.write(json.dumps(dic))
                    print(lang['fhint'][13].format(path))
                else:
                    json2obj(dic, config)
                    print(lang['fhint'][12])
            except Exception as e:
                print(lang['fhint'][11].format(id))
                print(lang['err'][2].format(e))

    def reset(self):
        self.ip = input(lang['fhint'][1].format('ip'))
        self.token = input(lang['fhint'][1].format('token'))
        self.ping()


class Config:

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.name = self.id
        self.gtime = int(datetime.datetime.now().timestamp())
        self.lang = ''
        self.synchronizer = Synchronizer()
        self.mode = mode[0]
        self.task: List[Task] = []
        self.hidden: List[Hidden] = []
        self.history: List[History] = []

    # Getter
    def getModeElement(self):
        if self.mode == mode[0]:
            return 0, self.task, self.dealNormal, self.normalShow
        if self.mode == mode[1]:
            return 1, self.history, self.dealHistory, self.historyShow
        return 2, self.hidden, self.dealHidden, self.hiddenShow

    # 过滤器Getter，返回元组
    def getFilterElement(self, s: str):
        raw = l2t(self.getModeElement()[1])
        return [i for i in raw if i[1].isContain(s)]

    # 任务处理
    def dealNormal(self, task: Task, para: List[str]):
        if 'd' not in para:
            self.history.append(History(task))
            if task.repeat:
                task.count += 1
                task.createTime = int(datetime.datetime.now().timestamp())
                self.task.append(task)
        if 'h' in para:
            self.hidden.append(Hidden(task.name, task.color))

    def dealHistory(self, task: History, para: List[str]):
        if 'r' in para:
            self.history.append(task)
            task.task.createTime = int(datetime.datetime.now().timestamp())
            self.task.append(task.task)

    def dealHidden(self, task: Hidden, para: List[str]):
        if 'd' not in para:
            self.task.append(Task(task.name, task.color, 'r' in para))

    # 任务展示
    def normalShow(self, task: List[Tuple]):
        for idx, i in task[-taskMax:]:
            print(
                colorChar(
                    lang['tformat'][0].format(
                        idx + 1,
                        i.name,
                        '' if not i.repeat else lang['aformat'][0].format(i.count),
                    ),
                    i.color,
                )
            )

    def historyShow(self, history: List[Tuple]):
        f = datetime.datetime.fromtimestamp
        for idx, i in history[-historyMax:]:
            print(
                colorChar(
                    lang['tformat'][1].format(
                        idx + 1,
                        f(i.doneTime),
                        lang['aformat'][1].format(i.task.count)
                        if i.task.repeat
                        else '',
                        i.task.name,
                        diff(i.duringTime),
                    ),
                    i.task.color,
                )
            )

    def hiddenShow(self, hidden: List[Tuple]):
        for idx, i in hidden[-hiddenMax:]:
            print(colorChar(lang['tformat'][0].format(idx + 1, i.name, ''), i.color))

    # 任务生成
    def generateTask(self, com: str, para: List[str]):
        color = int(next((i for i in para if i.isdigit()), '0'))
        if 'h' in para:
            self.hidden.append(Hidden(com, color))
        else:
            self.task.append(Task(com, color, 'r' in para))


# 工具函数
# ------
# 清屏
def clear():
    os.system('clear' if sys.platform == 'linux' else 'cls')


# 等待回车
def enter():
    input(lang['chint'][3])


# 程序执行路径
def j(s: str):
    return os.path.join(sys.path[0], s)


# 列表转元组
def l2t(li: List):
    return [(idx, i) for idx, i in enumerate(li)]


# 参变分离
def sep(origin: str):
    if origin.find(' -') == -1:
        return origin, []
    para = [i for i in list(origin[origin.find(' -') + 2 :]) if i != '-' and i != ' ']
    return origin[: origin.find(' -')], para


# 彩色字符
def colorChar(s: str, f: int):
    if f == 0:
        return s
    return '\033[3{}m{}\033[0m'.format(f, s)


# 时间显示转换
def diff(ds: int):
    f = False
    st = ''
    la = lang['time']
    if ds // (60 * 60 * 24) != 0:
        st += str(ds // (60 * 60 * 24)) + la[0]
        f = True
    ds %= 3600 * 24
    if ds // (60 * 60) != 0 or f:
        st += str(ds // (60 * 60)) + la[1]
        f = True
    ds %= 60 * 24
    if ds // 60 != 0 or f:
        st += str(ds // 60) + la[2]
        f = True
    st += str(ds % 60) + la[3]
    return st


# json转对象
def json2obj(j, o):
    if isinstance(j, list):
        return [json2obj(i, deepcopy(o)) for i in j]
    if not (isinstance(j, dict)):
        return j
    d = {
        k: (
            json2obj(v, globals()[k.capitalize()]())
            if isinstance(v, (dict, list))
            else json2obj(v, object())
        )
        for k, v in j.items()
    }
    o.__dict__.update(d)
    return o


# 对象转json
def obj2json(o: object):
    return json.dumps(o, default=lambda x: x.__dict__, ensure_ascii=False)


# 过程函数
# ------
# 切换任务配置
def switchConfigration():
    global config, configPath
    fileList = [i for i in os.listdir(sys.path[0]) if i.endswith('.json')]
    for idx, i in enumerate(fileList):
        f = j(i) == configPath
        print(
            lang['tformat'][0].format(idx + 1, i, '') + colorChar(' <' if f else '', 1)
        )
    cmd = input(
        lang['chint'][4].format(
            '/'.join(str(i + 1) for i in range(len(fileList))) + '/q'
        )
    )
    if cmd == 'q':
        return
    if not cmd.isdigit() or int(cmd) > len(fileList):
        print(lang['err'][0])
    else:
        path = j(fileList[int(cmd) - 1])
        try:
            c = Config()
            with open(path, 'r') as f:
                json2obj(json.loads(f.read()), c)
            config = c
            configPath = path
            print(lang['chint'][5])
        except Exception:
            print(lang['err'][1].format(path))


# 设置默认任务配置
def setDefault():
    global configPath
    with open(j(defaultConf), 'r') as f:
        id = json.loads(f.read())['id']
    if j(defaultConf) != configPath:
        os.rename(j(defaultConf), j(f'{id}.json'))
        os.rename(configPath, j(defaultConf))
        configPath = j(defaultConf)
    print(lang['chint'][7])


# 输入控制
def untaskDeal(com: str):
    global config, lang
    clear()
    if com == resposive[1]:
        sys.exit()
    if com == resposive[2]:
        with open(helpPath, 'r') as f:
            print(f.read())
    if com == resposive[3]:
        switchConfigration()
    if com == resposive[4]:
        config.name = input(lang['chint'][6].format(config.name))
    if com == resposive[5]:
        setDefault()
    if com in sync:
        config.synchronizer.dealSync(com)
    if com not in (list(language.language.keys()) + mode) and com != '':
        enter()
    if com in language.language:
        config.lang, lang = com, language.language[com]
    if com in mode:
        config.mode = com


# 指令处理
def deal(com: str, para: List[str], elements: List, f):
    if 'f' not in para:
        if com in resposive:
            # 全局控制
            untaskDeal(com)
            elements = config.getModeElement()[1]
        elif com.isdigit():
            # 任务完成和删除
            if int(com) > len(elements):
                print(colorChar(lang['err'][0], 1))
                enter()
            else:
                f(elements.pop(int(com) - 1), para)
        else:
            # 任务新增
            config.generateTask(com, para)
            elements = config.getModeElement()[1]
        elements = l2t(elements)
    else:
        # 任务查找
        elements = config.getFilterElement(com)
    return elements


# 界面显示
def display(s: str, elements: List):
    clear()
    modeElement = config.getModeElement()
    print(lang['dname'][modeElement[0]] + f' ({config.name})')
    print(line)
    if modeElement[1] == []:
        print(lang['ehint'][modeElement[0]])
    elif elements == []:
        print(lang['ehint'][3].format(colorChar(s, 1)))
    else:
        modeElement[3](elements)
    print(line)


# 逻辑函数
# ------
# 挂载配置文件
def initialization():
    config = Config()
    try:
        with open(configPath, 'r') as f:
            json2obj(json.loads(f.read()), config)
    except Exception:
        la = input(language.langChoose)
        config.lang = la if la in language.language else 'zh'
        lang = language.language[config.lang]
        print(lang['chint'][0])
        with open(configPath, 'w') as f:
            f.write(obj2json(config))
        print(lang['chint'][1])
        print(lang['chint'][3])
    return config


# 主循环
def main():
    display('', l2t(config.getModeElement()[1]))
    while 1:
        # 获取输入
        com, para = sep(input(lang['chint'][2]))
        # 获取实体
        elements, dealF = config.getModeElement()[1:-1]
        # 指令处理
        elements = deal(com, para, elements, dealF)
        # 界面显示
        display(com, elements)
        # 保存
        with open(configPath, 'w') as f:
            f.write(obj2json(config))


clear()
# 全局变量
configPath = j(defaultConf)
helpPath = j(defaultHelp)
config = initialization()
lang = language.language[config.lang]
# 主循环
main()
