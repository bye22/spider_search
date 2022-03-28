
import random
import requests
from bs4 import BeautifulSoup
import time
import os

config = {
    "fenlei":"dongman",
    "px":"1920x1080",
    "path":"/home/bye/Pictures/waller_pic/www.netbian.com/",
    "startPage":31,
    "endPage":100
}

path = config["path"]

def LoadUserAgents(uafile):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[:-1])
    random.shuffle(uas)
    return uas
fenlei="dongman"

uas = LoadUserAgents("user_agents.txt")
head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "Accept-Encoding": 'gzip, deflate',
    "Accept-Language": 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # "Cache-Control": 'max-age=0',
    "Connection": 'close',
    "Cookie": '__yjs_duid=1_1ded8ba9b536c5b42796529239319dd21635240082530; Hm_lvt_14b14198b6e26157b7eba06b390ab763=1635240084,1635302667; xygkqecookieclassrecord=%2C7%2C; Hm_lpvt_14b14198b6e26157b7eba06b390ab763=1635303536',
    "Host": 'www.netbian.com',
    "Referer": 'http://www.netbian.com/1920x1080/',
    "Upgrade-Insecure-Requests": '1',
}
# head1 = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
#     "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     "Accept-Encoding": 'gzip, deflate',
#     "Accept-Language": 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
#     # "Cache-Control": 'max-age=0',
#     "Connection": 'keep-alive',
#     "Cookie": '__yjs_duid=1_1ded8ba9b536c5b42796529239319dd21635240082530; Hm_lvt_14b14198b6e26157b7eba06b390ab763=1635240084,1635302667; xygkqecookieclassrecord=%2C7%2C; Hm_lpvt_14b14198b6e26157b7eba06b390ab763=1635303536',
#     "Host": 'www.netbian.com',
#     "Referer": 'http://www.netbian.com/%s/' % "desk",
#     "Upgrade-Insecure-Requests": '1',
# }
# 下载图片
def download_img(img_url,desc):
    ua = random.choice(uas)
    head = {
            'User-Agent': ua
        }
    r = requests.get(img_url, headers=head, stream=True,timeout=(5,10))
    if r.status_code == 200:
        # img_name = img_url.split('/').pop()[-12:]  # 截取图片文件名
        img_name = desc  # 截取图片文件名

        if not os.path.exists(path):
            os.makedirs(path)
        # print(img_name)
        with open(path + img_name, 'wb') as f:
            f.write(r.content)
        return True



def getImgUrl1(url):
    response = requests.get(url, headers=head,timeout=(5,10)) 
    content = response.content
    soup = BeautifulSoup(content, "lxml")
    imgUrlList = soup.select('.list > ul > li > a')
    urls=set()
    for i in imgUrlList:
        imgUrl = i['href']
        urls.add(imgUrl.split('.')[0])
        print(imgUrl.split('.')[0] + "---------获取成功")
    return urls

def getImgUrl2(url):
    response = requests.get(url, headers=head,timeout=(5,10)) 
    content = response.content
    if(response.status_code == 200 ) :
        soup = BeautifulSoup(content, "lxml")
        # print(soup)
        if soup.find(id='endimg') != None:
            # 图片列表
            imgUrl=soup.find(id='endimg').img['src']
            desc=soup.find(id='endimg').img['alt']
            ret = download_img(imgUrl,desc)
            print(imgUrl,desc)
            if not ret:
                print(imgUrl + "下载失败")
            return -1
        # imgUrlList = soup.select('.list > ul > li > a > img')
        # for i in imgUrlList:
            # imgUrl = i['src']
    # print(imgUrl + "---------下载成功")
    return -1
    




if __name__ == '__main__':
    # 下载要的图片
    for i in range(config["startPage"], config["endPage"]):
        # http://www.netbian.com/desk/12211-1920x1080.htm
        imgUrl1 = 'http://www.netbian.com/%s/index_%s.htm' % (config["px"],str(i))
        try:
            urls= getImgUrl1(imgUrl1)
            time.sleep(random.randint(1,3))
            for j in urls:
                time.sleep(random.randint(1,3))
                # print("imgUrl",j)
                url2="http://www.netbian.com/"+j+"-"+config["px"]+".htm"
                try:
                    if getImgUrl2(url2) < 0:
                        continue
                except requests.exceptions.RequestException as e:
                    print(e)
                    continue
        except requests.exceptions.RequestException as e:
            print(e)
            continue