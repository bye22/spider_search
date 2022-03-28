from logging import exception
from bs4 import BeautifulSoup
import requests
from urllib import request
import time

# soup=BeautifulSoup(open('test.html'))
# print(soup)
# desc=soup.find(id='endimg').img['alt']
# url=soup.find(id='endimg').img['src']

# print(soup.find(id='endimg'))
# if soup.find(id='endimg') != None:
#   print(soup.find(id='endimg').img['alt'])
# print("-1")
# for in range (1,10000):
# try:
#     # resp=request.urlopen('http://www.netbian.com/desk/43-1920x1080.htm')
#     resp=request.urlopen('http://www.netbian.com/desk/82-1920x1080.htm')
#     print(resp.content)
#     print("you")
# except Exception as e:
#     print("wuxiao")
#     print(e)

# resp=requests.get("http://www.netbian.com/desk/26210.htm")
# content=resp.content
# content = BeautifulSoup(content, "lxml")
# print(content)

# print('/desk/24197.htm'.split('.')[0])


url = 'http://www.google.com.hk'

print(time.strftime('%Y-%m-%d %H:%M:%S'))
for i in range(1,10):
    try:
            html = requests.get(url, timeout=5).text
            print('success')
    except requests.exceptions.RequestException as e:
        print(e)
        continue

print(time.strftime('%Y-%m-%d %H:%M:%S'))