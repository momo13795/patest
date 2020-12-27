# 导入库
from bs4 import BeautifulSoup
import requests
import re
import os
import time
import random
import sys

baseurl = "https://www.666dav.com/"


#rex1 = re.compile(r'href="(/zipaitoupai.*?)"')
rex1 = re.compile(r'href="(/\S+/\d+/)"')
rex2 = re.compile(r'src="(.*?)"')
#rex4 = re.compile(r'title="([\u4e00-\u9fa5]+.*?)"')
rex4 = re.compile(r'title="(.*?)"')

session = requests.session()


##文件夹路径
save_path = 'C:\\Users\\mark\\www\\pic\\66tv\\'
time2 = time.strftime('%Y-%m-%d', time.localtime())
dirpath = save_path + time2
path = save_path + time2  +  '\\66tvtv-%d-%d.jpg'
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

ualist = [
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:23.0) Gecko/20131011 Firefox/23.0",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; nb-NO) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14",
    "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; rv:21.0) Gecko/20130326 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130401 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Windows x86; rv:19.0) Gecko/20100101 Firefox/19.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15",
]


##获取请求头


def getHead(head):
    # head = {}
    # ua = random.choice(ualist)
    # head["referer"] = "http://t66y.com/"
    # head["Upgrade-Insecure-Requests"] = 1
    # head["User-Agent"] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    # head['Upgrade-Insecure-Requests'] =1
    # head['Cookie'] = 'UM_distinctid=1763cf32cb110d-06a8906ad0eb4d-c791039-1fa400-1763cf32cb24dc; CNZZDATA950900=cnzz_eid%3D790364290-1607340338-%26ntime%3D1607428238; __cfduid=d646897a36daff025a3e893736bd21eed1608205360; 227c9_lastvisit=0%091608896266%09%2Fread.php%3Ftid%3D4248452'
    return head


def getURL(url, head, session):
    proxies = {
        # 'http': 'http://derrick:111111@54.186.245.186:3128',
        # 'http': 'http://mark:111111@34.97.129.118:3128',
        'http': 'http://mark:111111@35.220.216.199:3128',
    }
    ##加上代理ip

    response = session.get(url=url, headers=head,proxies=proxies,timeout=5)
    # response = requests.get(url=url, headers=head, timeout=5)
    response.encoding = 'utf-8'

    html = response.text
    print(response.status_code)
    return html


def getLI(html):
    soup = BeautifulSoup(html, 'html.parser')

    allli = soup.find_all('div', class_='thumb')
    return allli


def wuhuDIV(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_links = soup.find('div', class_='news-content')
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
        os.mkdir(dirpath)


    where = save_path % (i,num)
    print(where)

    # where = r'C:\Users\mark\www\pic\美ag%d.jpg' % (i+1)#linux系统的写法
    imgstatus_code = wuhu.status_code
    print('图片地址状态：%d' %imgstatus_code)
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
            index = "zipaitupian/"
        else:
            index = '/zipaitupian/index_%d.html' % (i + 1)
        url = baseurl + index

        page = '当前抓取第{}页的url地址：{}'.format(i + 1, url)
        print(page)
        # print('当前抓取第%s页的url地址：%s' %(i+1,url))
        # exit()

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

                title = re.findall(rex4, str(item))[0]
                if title:
                    print('当前抓取的url二级页面地址：%s 标题为：%s' % (url, title))

                # 请求url地址
                try :
                    html = getURL(url, head, session)
                    div = wuhuDIV(html)
                except Exception :
                    print('当前li异常')
                    continue

                if re.findall(rex2, str(div)):
                    imgUrlArr = getimg(div, rex2)
                    for img in imgUrlArr:

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
