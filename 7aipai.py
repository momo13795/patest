# 导入库
from bs4 import BeautifulSoup
import requests
import re
import os
import time
import random
import sys
from fake_useragent import UserAgent

baseurl = "https://www.7aipai.com"

rex1 = re.compile(r'href="(\/\S+\d.html)"')
rex2 = re.compile(r'src="(.*?)"')
rex4 = re.compile(r'title="(.*?)"')

session = requests.session()


##文件夹路径
save_path = 'H:\\pa-pic\\7aipai\\'

time2 = time.strftime('%Y-%m-%d', time.localtime())
dirpath = save_path + time2
path = save_path + time2  +  '\\7aipai-%d-%d.jpg'
header = {

}


##获取请求头


def getHead(head):
    # head = {}
    # ua = random.choice(ualist)
    ua = UserAgent()
    head["referer"] = "https://www.7aipai.com/"
    head["Upgrade-Insecure-Requests"] = '1'
    head["User-Agent"] = ua.random
    return head


def getURL(url, head, session):
    proxies = {
        # 'http': 'http://derrick:111111@54.186.245.186:3128',
        # 'http': 'http://mark:111111@34.97.129.118:3128',
        'http': 'http://mark:111111@35.220.216.199:3128',
    }
    ##加上代理ip

    response = session.get(url=url, headers=head,proxies=proxies,timeout=15)
    #response = requests.get(url=url, headers=head, timeout=25)
    response.encoding = 'utf-8'

    html = response.text
    print(response.status_code)
    return html


def getLI(html):
    soup = BeautifulSoup(html, 'html.parser')

    allli = soup.find_all('li', class_='i_list list_n2')
    return allli


def wuhuDIV(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_links = soup.find('div', class_='content_left')
    return all_links


def getimg(div, method2):
    img = re.findall(method2, str(div))
    return img


def savepic(i, img, session, head, save_path,dirpath):
    head = getHead(head)
    wuhu = session.get(url=img, headers=head,timeout=3)
    time2 = time.strftime('%Y-%m-%d', time.localtime())
    num = random.randint(1000000000, 9999999999)


    if not os.path.exists(dirpath):
        os.makedirs(dirpath)


    where = save_path % (i,num)
    # where = r'C:\Users\mark\www\pic\美ag%d.jpg' % (i+1)#linux系统的写法
    imgstatus_code = wuhu.status_code
    # print('图片地址状态：%d' %imgstatus_code)
    if wuhu.status_code != 200:
        return
    f = open(where, 'wb')
    f.write(wuhu.content)


def main():
    print('开始...')
    ##图片张数定义
    m = 0
    guolv = int(input("输入过滤的数目： "))
    wish = 20
    isguolv = int(input("输入是否过滤： "))
    first = int(input("输入起始页数： "))
    end = int(input("输入结束页数： "))

    for i in range(first,end):
        if i == 0:
            index = ""
        else:
            index = '/index_%d.html' % (i + 1)
        url = baseurl + index
        pageurl = baseurl + index

        page = '当前抓取第{}页的url地址：{}'.format(i + 1, url)
        print(page)

        time.sleep(1)
        ##设置request头

        head = getHead(header)

        # 请求url地址
        html = getURL(url, head, session)
        # 获取一级页面的所有li
        allli = getLI(html)

        ##tr 标签定义
        y = 0
        for item in allli:
            y += 1
            ##过滤指定条数
            if isguolv == 1 and y <= guolv:
                continue

            print('当前第%d条li' % y)
            if re.findall(rex1, str(item)):
                url = baseurl + re.findall(rex1, str(item))[0]

                title = re.findall(rex4, str(item))
                if title:
                    title = re.findall(rex4, str(item))[0]
                    print('当前抓取的url二级页面地址：%s 标题为：%s' % (url, title))

                # 请求url地址
                try :
                    head['referer'] = pageurl
                    html = getURL(url, head, session)
                    div = wuhuDIV(html)
                except Exception :
                    print('当前li异常')
                    continue

                if re.findall(rex2, str(div)):
                    imgUrlArr = getimg(div, rex2)
                    for img in imgUrlArr:
                        img  = baseurl + img
                        # # 下载当前图片a
                        try :
                             m += 1
                             print('第%d页数据，标签地址为：%s,图片地址为：%s,第%d张图片下载' % (i + 1, url, img, m))
                             savepic(m, img, session, head, path,dirpath)
                             time.sleep(1)
                        except Exception:
                            print('第%d页数据，标签地址为：%s,图片地址为：%s,第%d张图片下载异常' % (i + 1, url, img, m))

                            continue

if __name__ == '__main__':
    main()
