#导入库
from bs4 import BeautifulSoup
import requests
import re
import time
import random
import sys

baseurl = "http://t66y.com/thread0806.php"
base = 'http://t66y.com/'
method1 = re.compile(r'"(.*?\d+.html)"')
method2 = re.compile(r'src="(.*?)"')

rex1 = re.compile(r'"(htm_data/\d+/\d+/.*?\d+.html)"')
rex2 = re.compile(r'ess-data="(.*?)"')

session = requests.session()
cfduid = 'd9f4ecb7595c8be46440b8d62894a33bd1608701116'
c9_lastvisit = '0%091608702730%09%2Fthread0806.php%3F'


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


def getHead():
    head = {}
    ua = random.choice(ualist)
    # head["referer"] = "http://t66y.com/"
    # head["Upgrade-Insecure-Requests"] = 1
    head["User-Agent"] = ua
    return head

def getURL(url, head,session):
    proxies = {
        # 'http': 'http://60.168.207.4:8888',
        #'http': 'http://derrick:111111@54.186.245.186:3128',
        'http': 'http://mark:111111@34.97.129.118:3128',
    }
    ##加上代理ip
    response = session.get(url=url, headers=head,proxies=proxies,timeout=7)
    # response = requests.get(url=url, headers=head,timeout=5)
    html = response.text
    print(response.status_code)
    return html

def getLI(html):
    soup = BeautifulSoup(html, 'html.parser')

    allli = soup.find_all('tr', class_='tr3 t_one tac')
    return allli


def wuhuDIV(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_links = soup.find('div', class_='tpc_content do_not_catch')
    return all_links
def getimg(div, method2):
    img = re.findall(method2, str(div))
    return img

def savepic(i, img,session):
    head = getHead()
    wuhu = session.get(url=img, headers=head)
    where = r'/Users/mark/Downloads/pictest/mark-ga-%d.jpg' % (i)#linux系统的写法
    f = open(where, 'wb')
    f.write(wuhu.content)

def main():
    print('开始...')
    m = 0
    #wish = int(input("请输入你想要的照片页数，别太多了： "))
    wish =20
    # cookie 实例化
    c = requests.cookies.RequestsCookieJar()
    # 定义cookie
    c.set('__cfduid', cfduid)
    c.set('227c9_lastvisit', c9_lastvisit)
    session.cookies.update(c)
    for i in range(wish):
        if i == 0:
            index = "?fid=16"
            # "http://t66y.com/thread0806.php?fid=16"
        else:
            index = '?fid=16&search=&page=%s' % (i+1)
            # index = "gaoqing_%s.html" % (i+1)


        url = baseurl+index
        # url = "http://www.win4000.com/wallpaper_detail_113430.html"
        page = '当前抓取第{}页的url地址：{}'.format(i+1,url)
        print(page)
        # print('当前抓取第%s页的url地址：%s' %(i+1,url))
        # exit()

        time.sleep(1)


        ##设置request头
        head = getHead()
        print(head)

        # 请求url地址
        html = getURL(url, head, session)
        # 获取一级页面的所有li
        allli = getLI(html)
        ##图片张数定义
        m = 0
        ##tr 标签定义
        y = 0
        for item in allli:
            y +=1
            ##第一页前7条不抓（一般前面几条是发帖的公告和其他注意事项）
            if i ==0 and y <= 9:
                continue
            if re.findall(rex1, str(item)):
                url = base + re.findall(rex1, str(item))[0]
                print('当前抓取的url二级页面地址：%s' % (url))

                ##设置二级页面request头
                head = getHead()
                # 请求url地址
                html = getURL(url, head, session)
                div = wuhuDIV(html)


                # print('div')
                # print(div)
                if re.findall(rex2, str(div)):
                    imgUrlArr = getimg(div,rex2)
                    # print(imgUrlArr)
                    for img in imgUrlArr:
                        m += 1
                        print('第%d页数据，标签地址为：%s,图片地址为：%s,第%d张图片下载' % (i + 1, url, img, m))

                        # 下载当前图片a
                        savepic(m, img,session)
                        time.sleep(1)



if __name__ == '__main__':
    main()