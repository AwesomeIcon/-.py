import smtplib
import email.utils
from email.mime.text import MIMEText
import getpass

username = raw_input("Username:")
password = getpass.getpass("password:")

msg = MIMEText('This is a message from huangjunqin.python')
msg ['To'] = email.utils.formataddr(('qq','uestc_ccse@qq.com'))
msg['From'] = email.utils.formataddr(('huangjunqin','uestc_ccse@fuestck.ml'))
msg['Subject'] = 'Simple Test by Python'

server = smtplib.SMTP('smtp.ym.163.com')
server.set_debuglevel(True)
try:
	server.login(username,password)
	server.sendmail(username, ['uestc_ccse@qq.com'], msg.as_string())
finally:
	server.quit()