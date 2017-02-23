# -*- coding:utf8 -*-
import filecmp
import re
import urllib
import getpass
import urllib2
import cookielib
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import sys
import os

reload(sys)
sys.setdefaultencoding('utf8')


class grade:
    def __init__(self, receiver, sender_passwd, username, password):
        self.cookieJar = cookielib.CookieJar()
        self.host = "smtp.ym.163.com"
        self.sender = "uestc_ccse@fuestck.ml"
        self.path = '/home/huangjunqin/Desktop/'
        self.receiver = receiver
        self.sender_passwd = sender_passwd
        self.username = username
        self.password = password
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar))
        urllib2.install_opener(self.opener)
        self.first_url = "http://idas.uestc.edu.cn/authserver/login?service=http%3A%2F%2Fportal.uestc.edu.cn%2F"
        self.result = self.get_lt_exe()
        self.lt = self.result.group(1)
        self.exe = self.result.group(2)
        self.post_data = urllib.urlencode({
                                        'username':	self.username,
                                        'password':	self.password,
                                        'lt': self.lt,
                                        'dllt':	'userNamePasswordLogin',
                                        'execution': self.exe,
                                        '_eventId':	'submit',
                                        'rmShown': '1'
                                           })
        self.second_url = "http://eams.uestc.edu.cn/eams/teach/grade/course/person!search.action?semesterId=123&projectType="

    def spider(self):
        request = urllib2.Request(self.first_url, data=self.post_data)
        response = self.opener.open(request)
        result = self.opener.open(self.second_url).read()
        return self.handler(result)

    def get_lt_exe(self):
        response = self.opener.open(self.first_url)
        data = response.read()
        pattern = re.compile('name="lt.*?value="(.*?)".*?name="execution.*?value="(.*?)"', re.S)
        result = re.search(pattern, data)
        return result

    def handler(self, result):
        try:
            tbody_pattern = re.compile('<tbody.*?>(.*?)</tbody>', re.S)
            tbody = re.search(tbody_pattern, result)
            tr_pattern = re.compile('<tr>(.*?)</tr>', re.S)
            tr = re.findall(tr_pattern, str(tbody.group(1)))
        except Exception:
            return 1
        if os.path.exists(self.path + self.username):
            fp = open(self.path + self.username, 'r')
            fp_old = open(self.path + self.username + '.old', 'w')
            fp_old.write(fp.read())
            fp.close()
            fp_old.close()
            fp = open(self.path + self.username, 'w+')
        else:
            fp = open(self.path + self.username, 'w+')
        for per_tr in tr:
            td_pattern = re.compile('<td.*?>(.*?)</td>', re.S)
            td = re.findall(td_pattern, per_tr)
            course = ''
            for per_td in td:
                course += per_td.strip() + '|'
            fp.write(course + '\n')
        fp.close()
        lines = []
        isChange = False
        if os.path.exists(self.path + self.username + '.old'):
            fp = open(self.path + self.username, 'r')
            fp_old = open(self.path + self.username + '.old', 'r')
            if filecmp.cmp(self.path + self.username, self.path + self.username + '.old') is not True:
                count_old = len(fp_old.readlines())
                count = len(fp.readlines())
                fp.seek(0)
                if count_old < count:
                    for new_line in fp.readlines():
                        flag = True
                        fp_old.seek(0)
                        for line in fp_old.readlines():
                            if cmp(line, new_line) == 0:
                                flag = False
                                break
                        if flag is True:
                            lines.append(new_line)
                if count_old == count:
                    isChange = True
                    for new_line in fp.readlines():
                    eqChange = False
                    fp_old.seek(0)
                    for line in fp_old.readlines():
                        if cmp(line, new_line) == 0:
                        eqChange = True
                        break
                    if eqChange is False:
                            lines.append(new_line)	    
                        return self.read_lines(lines, isChange)
            else:
                return False
        else:
	        isChange = False
            fp = open(self.path + self.username, 'r')
            lines = fp.readlines()
            return self.read_lines(lines, isChange)


    def read_lines(self, lines ,isChange):
        content = ''
        for line in lines:
            list = line.split('|')
            content += '课程名称：' + list[3] + '\n' + \
                       '课程性质：' + list[4] + '\n' + \
                       '学分：' + list[5] + '\n' + \
                       '成绩：' + list[6] + '\n' + \
                       '绩点：' + list[9] + '\n\n'
        return self.send_mail(content, isChange)

    def send_mail(self, lines, isChange):
        message = MIMEText(lines, 'plain', 'utf-8')
        message['From'] = Header("no-reply", 'utf-8')
        message['To'] = Header(self.username, 'utf-8')
        if isChange:
    	    subject = u'成绩有变动！'
	    else:
            subject = u'有新成绩出来啦！'
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.host, 25)
            smtpObj.login(self.sender, self.sender_passwd)
            smtpObj.sendmail(self.sender, self.receiver, message.as_string())
            print "邮件发送成功"
            return 0
        except smtplib.SMTPException:
            print "Error: 无法发送邮件"
            return 1

if __name__ == '__main__':
    receiver = raw_input(u'Enter your receiver:')
    sender_passwd = getpass.getpass(u'Enter your sender passwd:')
    username = raw_input(u'Enter userId:')
    passwd = getpass.getpass(u'Enter passwd:')
    grade(receiver,sender_passwd,username,passwd).spider()
