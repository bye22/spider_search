# coding: utf-8
import random
import time
import json
import requests
from db import REDIS
import pymysql

REPO_SHOW = '1'
REPO_HIDDEN = '0'

SEARCH_API = 'https://api.github.com/search/repositories?q=%s&sort=updated&order=desc&page=%s'
def LoadUserAgents(uafile):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[:-1])
    random.shuffle(uas)
    return uas


uas = LoadUserAgents("user_agents.txt")
head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://space.bilibili.com/45388',
    'Origin': 'http://space.bilibili.com',
    'Host': 'space.bilibili.com',
    'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}

def search_github(keyword):
    ua = random.choice(uas)
    head = {
            'User-Agent': ua
        }
    # 爬取 20 页最新的列表
    for i in range(1, 21):
        res = requests.get(SEARCH_API % (keyword, i),headers=head)
        repo_list = res.json()['items']
	
        for repo in repo_list:
            repo_name = repo['html_url'].strip()
            desc = {
                'repo_desc': repo['description'],
                'star': repo['stargazers_count'],
                'is_show': REPO_SHOW
            }
            ticks=str(time.time()).replace('.', '')
             # Please write your MySQL's information.
            try:
                    conn = pymysql.connect(
                        host='localhost', user='root', passwd='cogs.com', db='spider', charset='utf8')
                    cur = conn.cursor()
                    cur.execute('INSERT INTO github(`id`,`respo_name`, `desc`, `stars`, `is_show`) \
                    VALUES ("%s","%s","%s","%s","%s")'
                                %
                                (ticks,repo_name.strip(),str(desc['repo_desc']).replace("\"","\"\""),desc['star'],desc['is_show'] ))
                    print(ticks,',',repo_name)
                    conn.commit()
            except Exception as e:
                print(e)
            # if REDIS.hsetnx('repos', repo_name.strip(), json.dumps(desc)):
                # print(repo_name)
        time.sleep(10)


if __name__ == '__main__':
    keywords = ['爬虫', 'spider', 'crawl','批量']
    REDIS.set('keywords', ' '.join(keywords))
    for keyword in keywords:
        search_github(keyword)
