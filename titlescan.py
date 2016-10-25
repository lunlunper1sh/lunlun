#coding=utf-8
import smtplib
from email.mime.text import MIMEText
import re
import sys
import urllib2
import threading
import Queue

port=[80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,8000,8001,8002,8080,8081,8082,8083,8084,8085,8086,8087,8088,8089,8090,8888,9002,443,873,2601,2604,4848,8008,8880,9999,3128,5432,2049,7001,9200,9871,4440,6082,8099,8649,9000,9090,50000,50030,50070]
q = Queue.Queue() # define a global queue for users

f_f=open('/per1sh/urltt.txt','r+')

def email(url):
    _user = "1132227302@qq.com"
    _pwd  = "密码"
    _to   = "1132227302@qq.com"

    msg = MIMEText(url)
    msg["Subject"] = u"域名来了"
    msg["From"]    = _user
    msg["To"]      = _to

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
        print "Success!"
    except smtplib.SMTPException,e:
        print "Falied,%s"%e

# Create a class for Multi-threading
class myThread (threading.Thread):
    def __init__(self,func,args1,args2):
        threading.Thread.__init__(self)
        self.func = func 
        self.args1 = args1
        self.args2 = args2
    def run(self):
        self.func(self.args1, self.args2)

def htmlurl(url,f):
	for urllt in url:
		for ports in port:
			try:
				if urllt.strip():
					urll="http://"+urllt.strip()+":"+str(ports)
					print urll
					html=urllib2.urlopen(urll,timeout=1)
					htmll=html.read()
					title=r'<title>(.+?)</title>'
					title_user=re.compile(title,re.S)
					title_list=re.findall(title_user,htmll)
					for line in title_list:
						f.write(urll.replace("\n","\t")+line.decode('utf-8').encode('gbk')+"\n")
						f.flush()
						print urll.replace("\n","\t")+line.decode('utf-8').encode('gbk')
						time.sleep(0.01)
					
			except:
				pass

def multihtmlurl(q,f):
	while True:
		if not q.empty():
			try:
				urll=q.get().strip()
				print urll+"\r"
				html=urllib2.urlopen(urll,timeout=1)
				htmll=html.read()
				title=r'<title>(.+)</title>'
				title_user=re.compile(title,re.S)
				title_list=re.findall(title_user,htmll)
				for line in title_list:
					f.write(urll.replace("\n","\t\t")+" "+line.decode('utf-8').encode('gbk')+"\n")
					f.flush()
					print urll.replace("\n","\t\t")+" "+line.decode('utf-8').encode('gbk')+"\r"
					time.sleep(0.01)
			except:
				pass
		else:
			break
				
if __name__ == '__main__':
	#helps="python titlescan.py -u res.txt url.txt"
	helps=u"""
                            titlescan
                            作者：沦沦
    使用说明：
    ＊＊＊默认10个线程＊＊＊
    单线程扫描：python titlescan.py -u res.txt url.txt
    多线程扫描：python titlescan.py -m 10 -u res.txt url.txt
    """
	if len(sys.argv)<2:
		print helps
	else:
		if len(sys.argv)>2:
			if sys.argv[1]=="-u":
				url=open(sys.argv[2],'r')
				f=open(sys.argv[3],'w')
				print htmlurl(url,f)
			elif sys.argv[1]=="-m" and sys.argv[3]=="-u":
				threads = []
				threadList = range(int(sys.argv[2]))
				url=open(sys.argv[4],'r')
				f=open(sys.argv[5],'w')
				for urllt in url:
					for ports in port:
						if urllt.strip():
							q.put("http://"+urllt.strip()+":"+str(ports))
				for i in threadList:
					t = myThread(multihtmlurl, q, f)
					t.setDaemon(True)
					threads.append(t)
					t.start()
				for t in threads:
					t.join()
				f_ff=f_f.read()
				email(f_ff)
		else:
				print helps
