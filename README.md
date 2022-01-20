# MastersTasks

> 一个本地（~~未来可能远程同步~~）基于python的管理备忘及记录完成任务的程序？

## 前言

市面上的任务备忘系统都太花里胡哨了，要么功能过于复杂，简单地任务还需要搞一大堆标签时间等等，对于某些灵机一动想要完成的内容却根本没有心情打开软件进行备忘，最终反而忘记了很多需要做的事

虽然说专门搞一个记事本记也不是不可以，但是又感觉档次上不去，而且仅一个记事本像是制定任务的一些属性也不方便保存，而且终端是个好东西不用真是可惜了，自己手写一个程序也不要钱，顺便还可以巩固一下自己薄弱的编程知识，于是就这样说干就干了

## 使用方法

1. 给自己电脑安装一个[python环境](https://www.python.org/)，~~下过来一直next即可~~

2. clone或者Download一下，然后解压

3. 在**有`MastersTasks.py`文件的文件夹**下打开终端

4. 输入`python -u ./MastersTasks.py`即可使用

5. 确认可以使用之后可以自己写个`.bat`或者`.sh`脚本执行，还是不愿意的话文件下的阉割版双击执行即可

   > 请务必保证自己拥有**python的环境（终端下`python -V`检查）**，程序内不涉及第三方依赖，啥版本都行

## 简单的开始

本程序大致分为三种任务类型，分别是普通任务，隐藏任务和重复任务，另外还提供了完成任务的历史记录查看功能

在您第一次运行程序的时候，会在`MastersTasks.py`同目录下生成一个`conf.json`文件，用于本地保存您的任务信息，接着您可以**直接输入**您想要干的事情来添加某普通任务到列表中

不出所料的话接着您的终端上即会出现您刚刚输入的任务信息，前面会用一个1标识，这即是您的任务列表，默认状态下，当程序启动时就会自动展示此列表，以确保提醒到您当前任务的完成情况，当然，您也可以通过输入`l`来手动控制展示此列表

> 注意，由于追求极简的操作，您的有些任务名称可能是不支持的（比如以数字开头的任务名）

当您完成一项任务时，您仅需**直接输入**列表中展示的任务编号即可删除对应任务

如果您想要查看自己任务的完成情况，可以在终端状态下输入`h`来查看任务完成的历史，其中列举了您详细的任务完成经过及时间，对于不满意的历史记录，也可以通过直接输入记录编号进行删除

除了直接输入任务内容来进行添加任务，您还可以通过添加参数的方式添加到别的任务类型，其中隐藏任务不会记录您的制定时间，且在常规任务列表中不可见（可以通过`l -h`查看），您可以随时将他们方便的添加到普通或是重复任务列表中

重复任务在列表中可见，且在输入任务编号后并不会消失，而是记录您完成的次数，直到您通过`[编号] -r`的方式移除他们，相关的记录也可以在历史记录列表中查看到

更多的操作可以查看`help.txt`文档，注意目前尚不支持撤回操作，若误删了相关任务暂且无法恢复

同时请勿改动`conf.json`下的相关内容，出现错误请您自行负责！

## TODO

- 支持历史记录撤回任务列操作
- 连接第三方API支持远程同步任务
- 更多需求可以进行issue~

