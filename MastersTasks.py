#!/usr/bin/env python
# -*- coding: utf-8 -*-
from copy import copy
import json
import datetime
import os

# 函数部分
# --------------------------------------------


# 参变分离
def Sepa(com):
    para = {}
    f = ""
    # 不存在参数
    if (com.find(" -") == -1):
        return com, para
    com = com.split()
    # 提取到字典
    for p in com[1:]:
        if (p[0] == '-'):
            para[p] = ""
            f = p
        else:
            para[f] = p
    return com[0], para


# 计算时间差，并格式化输出
def Diff(ds):
    f = False
    st = ""
    if (ds // (60*60*24) != 0):
        st += str(ds // (60*60*24))+"天"
        f = True
    ds %= 3600*24
    if (ds // (60*60) != 0 or f):
        st += str(ds // (60*60))+"小时"
        f = True
    ds %= 60*24
    if (ds // 60 != 0 or f):
        st += str(ds // 60)+"分钟"
        f = True
    st += str(ds % 60)+"秒"
    return st


# 列出指定内容
def ListT(tas, f=True):
    os.system("clear")
    c = 0
    for i in tas:

        # 分割线
        if (i == DIVID):
            if (c != 0):
                print(i)
            continue
        c += 1
        s = ""

        # 判断标签
        if (i["tag"] != ""):
            s += " Ps: " + i["tag"]
        # 判断任务类型
        if (i.get("repeat") != None and i.get("repeat") != 0):
            s += " (已完成:" + str(i["repeat"]) + "次)"

        print(str(c) + " " + i["value"] + s)
    global dp
    dp = 1

    # 提示信息
    if (c == 0 and f):
        print("当前的任务已经全部完成啦~")
    elif (c == 0 and not(f)):
        print("当前没有隐藏任务~")
    elif (c != 0 and f):
        print("可以输入记录编号表示完成目标任务")
    else:
        dp = 3
        print("可以输入任务编号将其添加到任务列表")
    print(DIVID)


# 列出历史
def ListH(his, f=""):
    os.system("clear")
    c = 0

    for i in his:
        c += 1
        s = ""
        if (i["value"].find(f) == -1):
            continue
        value = i["value"]

        # 判断标签
        if (i.get("tag") != ""):
            value += "(" + i["tag"] + ")"

        # 重复任务移除
        if (i["type"] == 'd'):
            s = "删除了重复任务 " + value + " ,一共完成了" + str(i["repeat"]) + "次"
        # 重复任务
        elif (i["type"] == 'rt'):
            s = "完成了任务 " + value + " ,距上一次完成用了" + \
                Diff(i["doneTime"]-i["lastTime"])
        # 普通任务
        elif (i["type"] == 't'):
            s = "完成了任务 " + value + " ,花费了" + Diff(i["doneTime"]-i["creatTime"])

        # 格式化输出
        d = datetime.datetime.fromtimestamp(i["doneTime"])
        print(str(c) + " 您于" + str(d) + s)

    # 环境及格式化输出
    global dp
    dp = 2
    if (c == 0):
        print("还没有完成过任务呢~")
    else:
        print("可以输入记录编号删除目标记录")
    print(DIVID)


# 生成任务条目
def GenerateT(target, tag, rep=False):
    dic = {}
    dic["creatTime"] = int(datetime.datetime.now().timestamp())
    dic["value"] = target
    dic["tag"] = tag
    # 判断重复任务
    if (rep):
        dic["repeat"] = 0
        dic["lastTime"] = dic["creatTime"]
    return dic


# 生成历史条目
def GenerateH(target, type):
    dic = target.copy()
    dic["doneTime"] = int(datetime.datetime.now().timestamp())
    dic["type"] = type
    return dic


# 主程序
# ---------------------------------------

# 全局变量
dp = 1
PATH = "./conf.json"
DIVID = "-"*30
HELP = "./help.txt"
info = {}
os.system("clear")

# 初始化
if (not(os.path.isfile(PATH))):
    print("检测到本目录下不存在配置文件，正在创建...")
    file = open(PATH, 'w')
    info["CreatTime"] = int(datetime.datetime.now().timestamp())
    info["Task"] = {}
    info["Task"]["Current"] = []
    info["Task"]["Hide"] = []
    info["Task"]["Repeat"] = []
    info["History"] = []
    file.write(json.dumps(info))
    file.close()
    print("创建成功，如需帮助请输入 help 并按回车查看帮助")
else:
    t = json.loads(open(PATH).read())["Task"]
    ListT(t["Repeat"]+[DIVID, ]+t["Current"])

# 主循环
while True:

    # 参变分离
    try:
        com, para = Sepa(input("当前操作: "))
    except Exception as e:
        print(e)
        continue

    # 响应即时性指令
    if (com == ""):
        continue
    if (com == "q"):
        break
    if (com == "c"):
        os.system("clear")
        continue
    if (com == "help"):
        os.system("clear")
        print(open(HELP).read())
        continue

    # 获取文件中的内容
    info = json.loads(open(PATH).read())
    current = list(info["Task"]["Current"])
    hide = list(info["Task"]["Hide"])
    repeat = list(info["Task"]["Repeat"])
    history = list(info["History"])

    # 直接列出内容相关
    if (com == "h"):
        if (para.get("-f") != None):
            ListH(history, para["-f"])
        else:
            ListH(history)
    elif (com == "l"):
        if (para.get("-h") == None):
            ListT(repeat + [DIVID, ] + current)
        else:
            ListT(hide, False)

    # 对指定条目操作
    elif (com[0] > '0' and com[0] <= '9'):
        # 完成任务
        if (dp == 1):
            try:
                num = int(com)
            except ValueError:
                print("任务不应该以数字开头")
            except Exception as e:
                print("奇怪的异常: e")
            else:
                # 重复任务相关
                if (len(repeat) >= num):
                    doneT = repeat[num-1]
                    if (para.get('-r') != None or para.get('-d') != None):
                        if (para.get('-d') == None):
                            history.append(GenerateH(doneT, "d"))
                        repeat.remove(doneT)
                    else:
                        history.append(GenerateH(doneT, "rt"))
                        doneT["repeat"] += 1
                        doneT["lastTime"] = int(
                            datetime.datetime.now().timestamp())
                    ListT(repeat + [DIVID, ] + current)
                # 普通任务相关
                elif (len(current)+len(repeat) >= num):
                    doneT = current[num - len(repeat) - 1]
                    if (para.get('-d') == None):
                        history.append(GenerateH(doneT, "t"))
                    current.remove(doneT)
                    ListT(repeat + [DIVID, ] + current)
                else:
                    print("指定完成的任务序号不存在于表中")
        # 移除历史记录
        if (dp == 2):
            try:
                delH = history[int(com)-1]
            except IndexError:
                print("不存在该历史记录需要删除")
            except ValueError:
                print("错误的删除指令")
            except Exception as e:
                print("奇怪的异常: e")
            else:
                history.remove(delH)
                ListH(history)
        # 添加隐藏任务至任务列表
        if (dp == 3):
            try:
                addH = hide[int(com)-1]
            except IndexError:
                print("不存在该隐藏内容")
            except ValueError:
                print("错误的指令")
            except Exception as e:
                print("奇怪的异常: e")
            else:
                if (para.get("-r") != None and para.get("-d") == None):
                    repeat.append(GenerateT(addH["value"], addH["tag"], True))
                elif (para.get("-d") == None):
                    current.append(GenerateT(addH["value"], addH["tag"]))
                hide.remove(addH)
                ListT(repeat + [DIVID, ] + current)

    # 添加任务
    else:
        # 判断标签
        if (para.get("-t") == None):
            tag = ""
        else:
            tag = para['-t']

        # 选择添加列表
        if (para.get("-h") != None):
            hide.append({"value": com, "tag": tag})
        elif (para.get("-r") != None):
            repeat.append(GenerateT(com, tag, True))
        else:
            current.append(GenerateT(com, tag))
        ListT(repeat + [DIVID, ] + current)

    # 转存到文件
    info["Task"]["Current"] = current
    info["Task"]["Hide"] = hide
    info["Task"]["Repeat"] = repeat
    info["History"] = history
    open(PATH, 'w').write(json.dumps(info, ensure_ascii=False))
