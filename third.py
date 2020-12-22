#导入库
from bs4 import BeautifulSoup
import requests
import re
import time
import random
import sys

baseurl = "http://www.win4000.com/zt/"
method1 = re.compile(r'"(.*?\d+.html)"')
method2 = re.compile(r'src="(.*?)"')

rex1 = re.compile(r'"(http://www.win4000.com/wallpaper_detail_.*?\d+.html)"')
rex2 = re.compile(r'src="(.*?)"')
rex3 = re.compile(r'<a href="(.*?)">')
rex4 = re.compile(r'"http://www.win4000.com/wallpaper_detail_.*?(\d+).html"')
rex5 = re.compile(r'"http://www.win4000.com/wallpaper_detail_(.*?\d+).html"')
rex6 = re.compile(r'\d+')



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
    head["User-Agent"] = ua
    return head

# 获取页面的html


def getURL(url, head):
    response = requests.get(url=url, headers=head)
    html = response.text
    return html


def getdiv(html):
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div", class_="tab_box")
    return div

def getDivLi(div, method1):
    a = re.findall(method1, str(div))
    return a

# 分析一级页面


def getLI(html):
    soup = BeautifulSoup(html, 'html.parser')
    allli = soup.find_all('li')
    return allli

# 分析二级页面


def getSecondDIV(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_links = soup.find('div', class_='pic-meinv')
    return all_links




def getimg(div, method2):
    img = re.findall(method2, str(div))[0]
    return img

def geta(div, method1):
    a = re.findall(method1, str(div))[0]
    return a


def getaNextNum(div, method):
    a = re.findall(method, str(div))[0]
    return a

def getaNextNum2(b,method):
    a = re.findall(method, str(b))[0]
    return a


def savepic(i, img):
    head = getHead()
    wuhu = requests.get(url=img, headers=head)
    where = r'/Users/mark/Downloads/pictest/mark%d.jpg' % (i)#linux系统的写法
    f = open(where, 'wb')
    f.write(wuhu.content)

def main():
    print('开始...')
    m = 0
    wish = int(input("请输入你想要的照片页数，别太多了： "))
    for i in range(wish):
        if i == 0:
            index = "gaoqing.html"
        else:
            index = "gaoqing_%s.html" % (i+1)

        url = baseurl+index
        print('当前抓取的url地址：%s' % (url))
        ##设置request头
        head = getHead()

        #获取一级页面html
        html = getURL(url, head)

        #获取一级页面的所有li
        allli = getLI(html)

        for item in allli:
            # print(item)
            if re.findall(rex1, str(item)):
                url = re.findall(rex1, str(item))[0]
                print('当前抓取的url二级页面地址：%s' % (url))

                #获取url的数字
                urlNum = re.findall(rex4, str(item))[0]

                while 1:
                    m +=1
                    print('当前抓取的第%d张图片' % (m))

                    # print(urlNum)
                    #请求二级页面
                    head = getHead()
                    html = getURL(url, head)
                    # print(html)
                    #获取解析后的div
                    div = getSecondDIV(html)
                    # print(div)
                    #获取img地址
                    img = getimg(div, rex2)
                    #获取下一张图片的地址
                    url = geta(div, rex3)
                    nextNum = getaNextNum(div, rex5)
                    nextNum2 = getaNextNum2(nextNum, rex6)

                    # print(nextNum)
                    # print(nextNum2)

                    #下载当前图片
                    savepic(m, img)
                    time.sleep(0.5)

                    if urlNum != nextNum2:
                        break



if __name__ == '__main__':
    main()