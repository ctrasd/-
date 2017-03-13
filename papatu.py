# -*- coding: utf-8 -*-
#!/usr/bin/env python3
__author__='ctr'
import urllib  
import http.cookiejar
#import urllib2  
#import cookielib  
import re
import sys
import pytesser
import PIL
from pytesseract import *
from PIL import Image
from PIL import ImageEnhance
import os
import getpass
import  msvcrt
import time

def pwd_input():
	chars = [] 
	while True:
		try:
			newChar = msvcrt.getch().decode(encoding="utf-8")
		except:
			return input("你很可能不是在cmd命令行下运行，密码输入将不能隐藏:")
		if newChar in '\r\n': # 如果是换行，则输入结束             
			break 
		elif newChar == '\b': # 如果是退格，则删除密码末尾一位并且删除一个星号 
			if chars:  
				del chars[-1] 
				msvcrt.putch('\b'.encode(encoding='utf-8')) # 光标回退一格
				msvcrt.putch( ' '.encode(encoding='utf-8')) # 输出一个空格覆盖原来的星号
				msvcrt.putch('\b'.encode(encoding='utf-8')) # 光标回退一格准备接受新的输入                 
		else:
			chars.append(newChar)
			msvcrt.putch('*'.encode(encoding='utf-8')) # 显示为星号
	return (''.join(chars) )


def denglu(usr,psw):
	hosturl='http://wiscom.chd.edu.cn:8080/reader/'
	posturl='http://wiscom.chd.edu.cn:8080/reader/redr_verify.php'
	cj = http.cookiejar.CookieJar()
	cookie_support = urllib.request.HTTPCookieProcessor(cj)
	opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
	urllib.request.install_opener(opener)
	h = urllib.request.urlopen(hosturl)

	#验证码
	captcha=opener.open('http://wiscom.chd.edu.cn:8080/reader/captcha.php')
	f=open('1.jpg','wb')
	buf=captcha.read()
	f.write(buf)
	f.close()
	im=Image.open('1.jpg').convert('L')
	captcha=image_to_string(im)
	print(captcha)


	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'} 
	postData = {'number':usr,'passwd':psw,'captcha':captcha,'select':'cert_no','returnUrl':''}
	postData = urllib.parse.urlencode(postData).encode(encoding='UTF8')
	request = urllib.request.Request(posturl,postData,headers)
	flagg=False
	try:
		rt=opener.open(request)
		text=rt.read().decode('UTF-8')
		f=open('1.html','w')
		f.write(text)
		f.close()
		#rt=urllib.request.urlopen('http://wiscom.chd.edu.cn:8080/reader/redr_verify.php').read()
	except urllib.request.URLError as e:
		print('Login Failed  [%s] ' %e.reason)
	except urllib.request.HTTPError as e:
		print ('Login Failed  [%s] ' %e.code)
	else:
		pattern=r"对不起，密码错误，请查实！"
		pattern=re.compile(pattern)
		matcher1 = re.search(pattern,text)
		#print("matcher1:",matcher1)
		#input()
		if matcher1=="对不起，密码错误，请查实！":
			print("对不起，密码错误，请查实！")
			print("按回车键重新输入")
			input()
			flagg=False
		else:
			flagg=True
	return flagg

def convert(s):
	s=s.strip('&#x;')
	s=bytes(r'\u'+s,'ascii')
	return s.decode('unicode_escape')


def lishi(text):
	f=open('lishi.html','r',encoding='utf-8')
	text=f.read()
	#pattern1=r"t\">(.+?)</td>"
	#pattern1=re.compile(pattern1)
	#text1=pattern1.findall(text)
	#for subtext in text1:
	#	print(subtext, end=' ')
	#print('')
	pattern2=r"<td bgcolor=\"#FFFFFF\"(.+?)>(.+?)</td>\s*?<(.+?)>(.+?)</td>\s*?<(.+?)><a(.+?)>(.+?)</a></td>\s*?<td(.+?)>(.+?)</td>\s*?<(.+?)>(.+?)</td>\s*?<(.+?)>(.+?)</td>\s*?<(.+?)>(.+?)</td>"
	pattern2=re.compile(pattern2)
	text2=pattern2.findall(text)
	
	for t in text2:
		pattern3=r"&#x.+?;"
		pattern3=re.compile(pattern3);
		text3=pattern3.findall(t[6])
		pp=''
		for text in text3:
			pp+=convert(text)
		pattern3=r"&#x.+?;"
		pattern3=re.compile(pattern3);
		text3=pattern3.findall(t[8])
		tt=''
		for text in text3:
			tt+=convert(text)
		print('编号：',t[1],'\n','--条码号：',t[3],'\n','--题名：',pp,'\n','--责任者：',tt,'\n','--借阅日期:',t[10],'\n','--归还日期：',t[12],'\n','--馆藏地：',t[14])
		print('')

def query(usr,psw):
	flag=True
	while flag:
		if denglu(usr,psw)==True:
			t = os.system('cls')
			for x in range(1,17):
				for y in range(1,x*5):
					print('>',end='')
				print('')
				time.sleep(0.3)	

			print('')
			print('                                    登录完毕！                                 ')  
			time.sleep(3)
			t = os.system('cls')
			while flag:
				for x in range(1,5):
					print('')
				print('---------------------------------1:输出基本信息---------------------------------')
				print('                                                                               ')
				print('---------------------------------2:输出到期信息---------------------------------')
				print('                                                                               ')
				print('---------------------------------3:输出历史信息---------------------------------')
				print('                                                                               ')
				print('-----------------------------------4:退出系统-----------------------------------')
				ch=input()
				if ch=='1':
					text=urllib.request.urlopen('http://wiscom.chd.edu.cn:8080/reader/redr_info.php').read().decode('UTF-8')
					f=open('jiben.html','wb')
					key=text
					pattern1=r"\">(.+?)</span>(.+?)</TD>"
					pattern1=re.compile(pattern1)
					text=pattern1.findall(key)
					#print(text)
					for subtext in text:
						print('---',subtext[0],subtext[1],'            ')
					print('')
					f.close()


				if ch=='2':
					text=urllib.request.urlopen('http://wiscom.chd.edu.cn:8080/reader/redr_info.php').read().decode('UTF-8')
					f=open('jiben.html','wb')
					key=text
					#print(key)
					
					pattern1=r"\">(.+?)\[<strong style=\"color:#F00;\">(.+?)</strong>"
					pattern1=re.compile(pattern1)
					text=pattern1.findall(key)
					for subtext in text:
						print('---',subtext[0],subtext[1],'            ')
					print('')
					#f.write(text)
					f.close()


				if ch=='3':
					text=urllib.request.urlopen('http://wiscom.chd.edu.cn:8080/reader/book_hist.php').read()#.decode('UTF-8')
					f=open('lishi.html','wb')
					f.write(text)
					lishi(text)
					f.close()

				if ch=='4':
					flag=False

				input('按回车键继续')
				t = os.system('cls')  
		else:
			t = os.system('cls')  
			usr=input('输入账号:\n')
			print('输入密码:')
			psw=pwd_input()
			print('')



if __name__ == '__main__':
	usr=input('输入账号:\n')
	print('输入密码:')
	psw=pwd_input()
	print('')
	#usr=201512020107
	#psw='ctr123'
	query(usr,psw)
