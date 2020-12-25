import re
from bs4 import BeautifulSoup
import requests
import time
import random

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
method1 = re.compile(r'<a href="(.*?)">')
method2 = re.compile(r'src="(.*?)"')


def gethead():
    head = {}
    ua = random.choice(ualist)
    head["User-Agent"] = ua
    return head


def gethtml(url):
    head = gethead()
    proxies = {
        'http': '139.224.37.83:3128',

    }

    # response = requests.get(url=url, headers=head,proxies=proxies)
    retry_count = 5
    # proxy = get_proxy().get("proxy")
    proxy = '172.100.10.13:9698'
    # proxies = {
    #     'http':'http://{}'.format(proxy),
    # }
    proxies = {
        # 'http': 'http://derrick:111111@172.100.10.13:9698',
        #'http': 'http://derrick:111111@54.186.245.186:3128',
        'http': 'http://mark:111111@34.97.129.118:3128',

    }
    print(proxies)
    # exit()
    while retry_count > 0:
        try:
            #response = requests.get(url=url, headers=head, proxies=proxies)
            # 使用代理访问
            response = requests.get(url=url,headers=head, proxies=proxies,timeout=5)
            html = response.text
            print('success')
            return html
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)

    print('问题代理ip'+ proxy)
    return None

    # response = requests.get(url=url, headers=head)
    # html = response.text
    # return html


def getdiv(html,url):
    i = 0
    while True:
        i += 1
        time.sleep(1)
        print('第%d次尝试' % i)
        while 1:
            if html is None:
                print('html 为none')
                html = gethtml(url)
            else:
                break
        soup = BeautifulSoup(html, "html.parser")
        div = soup.find("div", class_="pic-meinv")

        if div is None:
            html = gethtml(url)
            if html is None:
                html = gethtml(url)
                print('is None')
            soup = BeautifulSoup(html, "html.parser")
            div = soup.find("div", class_="pic-meinv")
        else:
            return div


def geta(div, method1):
    a = re.findall(method1, str(div))[0]
    return a


def getimg(div, method2):
    img = re.findall(method2, str(div))[0]
    return img


def savepic(i, img):
    head = gethead()
    wuhu = requests.get(url=img, headers=head)
    where = r'/Users/mark/Downloads/美g%d.jpg' % (i+1)#linux系统的写法
    f = open(where, 'wb')
    f.write(wuhu.content)


#获取代理ip
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

#删除代理
def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

def main():
    i = 0
    url = "http://www.win4000.com/wallpaper_detail_113430.html"#这个可以选择其他的
    wish = int(input("请输入你想要的照片数，别太多了： "))
    if wish == 1:
        html = gethtml(url)
        div = getdiv(html,url)
        img = getimg(div, method2)
        savepic(i, img)
    for i in range(wish):
        html = gethtml(url)
        # print(html)
        div = getdiv(html,url)
        # print(div)
        # exit()
        img = getimg(div, method2)
        url = geta(div, method1)
        print(url)
        savepic(i, img)
        time.sleep(0.5)


if __name__ == '__main__':
    main()