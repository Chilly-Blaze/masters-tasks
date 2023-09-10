# MastersTasks

一个基于终端的极简备忘录/任务管理器

https://github.com/Chilly-Blaze/MastersTasks/assets/74091261/8358df85-2ab8-4da8-bd96-03b7a5d1ce55

## 快速开始

假设只需要本地部署使用，则非常简单，下载项目中的MastersTasks.py，直接使用python3启动，详细指令可看help.txt

## 远程部署

1. 在服务器上安装python并下载项目中的server.py至服务器

2. 使用pip下载Sanic，`pip install sanic`

3. 启动服务，`sanic server.app`，屏幕上会显示出当前服务的token

4. 在客户端使用`r`命令设置服务信息ip和token

5. 通过`u`指令上传信息至远程

## 高级

你可以通过修改language.py和MastersTasks.py的全局常量来自定义提示词和不同指令使用的快捷字符
