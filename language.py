language = {
    'zh': {
        'time': ['天', '小时', '分钟', '秒'],
        'dname': ['普通任务列表', '历史任务列表', '隐藏任务列表'],
        'tformat': ['{}:\t{}  {}', '{}:\t于 {} {}完成了 {} ,花费了 {} '],
        'aformat': ['(已完成{}次)', '第{}次'],
        'chint': ['未检测到配置文件，正在创建', '创建成功', '当前操作:', '按下回车返回...', '请选择切换配置序号({}):', '切换成功', '请输入新的任务箱名称（当前:{}):', '已将当前任务箱设置为默认任务箱！'],
        'ehint': ['已完成所有任务！', '无历史记录', '无隐藏任务', '未找到记录包含{}', '未设置'],
        'fhint': ['当前任务列表未配置远端同步设置，是否配置(Y/n):', '请输入服务器{}:', '测试连接...', '测试成功', '测试失败，请检查配置内容(ip:{},token:{})，输入s可重设', '确认上传?(Y/n)', '正在上传...', '上传成功', '上传失败，错误信息({})', '请选择下载模式\n\t1:本地更新\n\t2:拉取新任务箱\n请输入(1/2/q,默认1):', '请输入新任务箱uuid:', '未找到远端配置(uuid:{})', '更新成功', '拉取成功，路径:{}，可使用t切换', '您的任务箱id是:{}，服务器token为:{}，请妥善保存相关信息'],
        'err': ['输入的序号不存在', '读取文件{}失败，请检查文件内容是否符合要求', '错误信息({})']
    },
    'mi': {
        'time': ['d', 'h', 'm', 's'],
        'dname': ['Tsk', 'Hst', 'hTsk'],
        'tformat': ['{}:\t{}  {}', '{}:\tt:{}{}  n:{}({})'],
        'aformat': ['d:{}', '  r:{}'],
        'chint': ['cfg create', 'succ', ':', 'Enter...', 'choose({}):', 'succ', 'new name(o:{}):', 'succ'],
        'ehint': ['empty', 'empty', 'empty', 'empty f:{}', 'empty'],
        'fhint': ['No sync, Add?(Y/n)', 'ipt {}:', 'ping...', 'test succ', 'test fail i:{} t:{}', 'cfm?(Y/n)', 'upload...', 'succ', 'fail m:{}', 'mode:\n\t1:upd\n\t2:pull\n(1/2/q):', 'uuid:', 'not found u:{}', 'upd succ', 'pull succ {}', 'uuid:{}, token:{}'],
        'err': ['num err', 'read err m:{}', 'err m:{}']
    },
    'en': {
        'time': [' day', ' hour', ' minute', ' second'],
        'dname': ['Normal Tasks', 'History', 'Hidden Tasks'],
        'tformat': ['{}:\t{}  {}', '{}:\tAt {}{}, Complete {}, Spend {}'],
        'aformat': ['(done:{})', ',(done {} time)'],
        'chint': ['Config File Not Found, Creating', 'Create Success', 'Current operation:', 'Press Enter to return...', 'Please choose target configration num({}):', 'Switch Configration Success', 'Please Input New TaskList Name(Now is {}):', 'The current TaskList has been set as the default'],
        'ehint': ['You have completed all tasks', 'No History Record', 'No Hidden Task Record', 'No record containing {} was found', '[NOT SET]'],
        'fhint': ['Sync settings not detected, do you need to set them up?(Y/n)', 'Please input server {}:', 'Test connection...', 'Test Success', 'Test Fail, Please Check the Configration(ip:{},token:{}), Press \'s\' to Reset', 'Confirm to Upload?(Y/n)', 'Uploading...', 'Upload Success', 'Upload Fail, Error Message: {}', 'Please Choose the Download Mode\n\t1:Local update\n\t2:Pull new Task Configration\nselect(1/2/q,default 1):', 'Please input new Task Configration uuid:', 'Configration not found(uuid:{})', 'Update Success', 'Pull Success, path is {}, you can input \'t\' to switch', 'Your uuid is:{}, and Your server token is:{}, Please Keep relevant information properly'],
        'err': ['The number you entered is not found', 'Read file \'{}\' failed, Please check whether the contents of the file meet the requirements', 'Error Message:{}']
    }
}
langChoose = '''\
还未选择语言，请选择显示语言(zh表示中文，en表示英文，mi表示简单的英文)
Language Not Found, Please Choose Display Language('zh' for Chinese, 'en' for English, 'mi' for easy english)
如果输入错误，默认显示中文，之后可以通过直接输入zh,en,mi切换语言
If Input Error, Chinese is Default, After that, you can switch languages by directly entering zh, en, mi
另外，之后你还可以通过输入'?'来查看使用说明
In addition, you can also enter '?' to check the instructions for use
: '''
