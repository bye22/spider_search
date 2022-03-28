
import random
import requests
from bs4 import BeautifulSoup
import time

config = {
    "fenlei":"dongman",
    "path":"/home/bye/Pictures/waller_pic/www.netbian.com/",
    "startPage":3,
    "endPage":10
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
    "Connection": 'keep-alive',
    "Cookie": '__yjs_duid=1_1ded8ba9b536c5b42796529239319dd21635240082530; Hm_lvt_14b14198b6e26157b7eba06b390ab763=1635240084,1635302667; xygkqecookieclassrecord=%2C7%2C; Hm_lpvt_14b14198b6e26157b7eba06b390ab763=1635303536',
    "Host": 'www.netbian.com',
    "Referer": 'http://www.netbian.com/%s/' % (config["fenlei"]),
    "Upgrade-Insecure-Requests": '1',
}
# 下载图片
def download_img(img_url):
    ua = random.choice(uas)
    head = {
            'User-Agent': ua
        }
    r = requests.get(img_url, headers=head, stream=True)
    if r.status_code == 200:
        img_name = img_url.split('/').pop()[-12:]  # 截取图片文件名
        print(img_name)
        with open(path + img_name, 'wb') as f:
            f.write(r.content)
        return True


def getImgUrl(url):
    response = requests.get(url, headers=head).content
    # print(response, '========')
    soup = BeautifulSoup(response, "lxml")
    # print(soup)
    # 图片列表
    imgUrlList = soup.select('.list > ul > li > a > img')
    for i in imgUrlList:
        imgUrl = i['src']
        ret = download_img(imgUrl)
        time.sleep(3)
        if not ret:
            print(imgUrl + "下载失败")
        print(imgUrl + "---------下载成功")





if __name__ == '__main__':
    # 下载要的图片
    for i in range(config["startPage"], config["endPage"]):
        # http://www.netbian.com/desk/12211-1920x1080.htm
        imgUrl = 'http://www.netbian.com/%s/index_%s.htm' % (config["fenlei"],str(i))
        time.sleep(10)
        print("imgUrl",imgUrl)
        getImgUrl(imgUrl)