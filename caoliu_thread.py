import os
import re
import requests
from bs4 import BeautifulSoup
import requests
import time
import random
from fake_useragent import UserAgent
import threading # 导入threading模块
from queue import Queue #导入queue模块

import caoliu_linux as base_caoliu


class Producer(threading.Thread):
    """
    生产者 - 手机表情包图片地址
    """

    def __init__(self, page_queue, img_queue, isyuanchuang, session, proxies):
        super(Producer, self).__init__()
        self.page_queue = page_queue
        self.img_queue = img_queue
        self.isyuanchuang = isyuanchuang
        self.session = session
        self.proxies = proxies

    def run(self):
        while True:
            url = self.page_queue.get()
            print("获取图片线程名:{}, 列表地址：{}".format(threading.currentThread().getName(), url))
            self.parse_page(url)

    def getProxy(self):
        proxy = f'https://user-tasssa12:test123@china-gate.visitxiangtan.com:8000'
        proxies = {
            'http': proxy,
            'https': proxy,
        }
        return proxies

    def getURL(self, url, head, session, proxies):
        # print("当前请求的 url地址:{}".format(url))
        ##加上代理ip
        if proxies:
            # url = 'http://ipinfo.io/json'
            # url = 'http://youtube.com'
            response = session.get(url=url, headers=head, proxies=proxies, timeout=20, verify=False)
        else:
            response = requests.get(url=url, headers=head, timeout=20)
        html = response.text
        print(response.status_code)
        return html

    def getLI(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        allli = soup.find_all('tr', class_='tr3 t_one tac')
        return allli

    def wuhuDIV(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        all_links = soup.find('div', class_='tpc_content do_not_catch')
        return all_links

    def getimg(self, div, method2):
        img = re.findall(method2, str(div))
        return img

    def parse_page(self, url):
        base = 'http://t66y.com/'

        # 获取详情页url正则
        rex1 = re.compile(r'"(htm_data/\d+/\d+/.*?\d+.html)"')

        # 获取详情页实际图片地址
        rex2 = re.compile(r'ess-data="(.*?)"')

        # 匹配是否是原创
        rex3 = re.compile(r'\[([\u4e00-\u9fa5]+.*?)\]')

        # 获取列表页中文标题
        rex4 = re.compile(r'>(\[?[\u4e00-\u9fa5]+.*?)</')

        ##设置request头
        head = {"referer": "http://t66y.com/index.php"}
        ua = UserAgent()
        head["User-Agent"] = ua.random


        # 请求列表url地址
        html = self.getURL(url, head, self.session, self.proxies)

        # 获取一级页面的所有li
        allli = self.getLI(html)

        ##图片张数定义
        m = 0
        for item in allli:
            ## 判断是否是[原创]
            if self.isyuanchuang == 1:
                if not re.findall(rex3, str(item)):
                    continue

            if re.findall(rex1, str(item)):
                # print(item)
                urldetail = base + re.findall(rex1, str(item))[0]

                title = re.findall(rex4, str(item))
                if title:
                    title = re.findall(rex4, str(item))[0]
                    print('当前抓取的详情页地址：%s 标题为：%s' % (urldetail, title))


                ##设置二级页面request头
                head["referer"] = url

                # 请求详情页的url地址
                print("开始访问详情页+++++++++++++++++++++++++")
                html = self.getURL(urldetail, head, self.session, self.proxies)
                div = self.wuhuDIV(html)

                if re.findall(rex2, str(div)):
                    imgUrlArr = self.getimg(div, rex2)
                    # print(imgUrlArr)
                    for img in imgUrlArr:
                        m += 1
                        print('标签地址为：%s,图片地址为：%s,第%d张图片下载' % (urldetail, img, m))
                        self.img_queue.put(img)
                time.sleep(random.randint(1,2))
        time.sleep(random.randint(1,2))


class Consumer(threading.Thread):
    """
    消费者 - 下载图片
    """

    def __init__(self, page_queue, img_queue, session, proxies, path, dirpath):
        super(Consumer, self).__init__()
        self.page_queue = page_queue
        self.img_queue = img_queue
        self.session = session
        self.proxies = proxies
        self.path = path
        self.dirpath = dirpath

    def run(self):
        head = {"referer": "http://t66y.com/index.php"}
        ua = UserAgent()
        head["User-Agent"] = ua.random
        while True:
            url = self.img_queue.get();
            print('下载图片线程名:{}, 图片地址：{}'.format(threading.currentThread().getName(), url))

            # 下载当前图片
            self.savepic( url, self.session, head, self.path, self.dirpath, self.proxies)
            time.sleep(random.randint(1,2))

    def savepic(self, img, session, head, save_path, dirpath, proxies):
        """
         下载图片
        :param img:
        :param session:
        :param head:
        :param save_path:
        :param dirpath:
        :param proxies:
        :return:
        """
        try:
            if proxies:
                wuhu = session.get(url=img, headers=head, timeout=20, proxies=proxies, verify=False)
            else:
                wuhu = session.get(url=img, headers=head, timeout=20)

            num = random.randint(1000000000, 9999999999)

            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            where = save_path % (num)

            if wuhu.status_code != 200:
                return

            print("当前正在下载的图片地址为：%s" % img)
            f = open(where, 'wb')
            f.write(wuhu.content)

        except Exception:
            print('异常图片地址：{}' + format(img))
def getProxy():
    proxy = f'https://user-tasssa12-country-us:test123@china-gate.visitxiangtan.com:8000'
    # proxy = f'http://user-tasssa12:test123@gate.visitxiangtan.com:7000'
    proxies = {
        'http': proxy,
        'https': proxy,
    }
    return proxies

def main():
    """
     主函数
     :return:
     """

    ##进程开始时间
    start_time = time.time()
    ispage = int(input("输入是否需要爬指定的页(1或者0)： "))

    num = int(input("输入执行的线程数： "))
    isproxy = int(input("输入是否需要代理(1或者0)： "))
    isyuanchuang = int(input("输入是否需要原创(1或者0)： "))
    baseurl = "http://t66y.com/thread0806.php"

    ##文件夹路径
    save_path = '/Users/jucce/www/picture/'
    time2 = time.strftime('%Y-%m-%d', time.localtime())
    dirpath = save_path + time2
    path = dirpath + '/caoliutv-%d.jpg'

    session = requests.session()

    """获取代理地址"""
    if isproxy:
        proxies = getProxy()
        print("当前代理地址为：%s" % proxies)
    else:
        proxies = {}

    page_queue = Queue()
    img_queue = Queue()

    if(ispage):
        page = int(input("输入爬取的指定页数： "))
        range_start, range_end = page-1, page
    else:
        page_start = int(input("输入爬取的开始页数： "))
        page_end = int(input("输入爬取的结束页数： "))
        if page_start == 0:
            range_start, range_end = page_start, page_end
            print('走00000，range_start：{}, range_end：{}'.format(range_start,range_end))

        else:
            range_start, range_end = page_start-1, page_end
            print('非走00000，range_start：{}, range_end：{}'.format(range_start,range_end))


    for i in range(range_start, range_end):
        if i == 0:
            index = "?fid=16"
        else:
            index = '?fid=16&search=&page=%s' % (i + 1)
        url = baseurl + index
        page_queue.put(url)
        print('当前抓取第{}页的url地址：{}'.format(i + 1, url))
        print('列表地址个数：{}'.format(page_queue.qsize()))

     # 定义五个生产者
    for x in range(num):
        t = Producer(page_queue=page_queue, img_queue=img_queue, isyuanchuang=isyuanchuang, session=session, proxies=proxies)
        t.start()


    # 定义三个消费者
    for x in range(num):
        t = Consumer(page_queue=page_queue, img_queue=img_queue, session=session, proxies=proxies, path=path, dirpath=dirpath)
        t.start()


def setImgQuene(url,head, session, proxies, img_queue):
    """
     通过详情页来获取图片地址，并将图片地址放在图片队列
    :param url:
    :param head:
    :param session:
    :param proxies:
    :param img_queue:
    :return:
    """
    ##图片张数定义
    m = 0
    # 访问详情页
    html = base_caoliu.getURL(url, head, session, proxies)
    div = base_caoliu.wuhuDIV(html)

    if re.findall(base_caoliu.rex2, str(div)):
        imgUrlArr = base_caoliu.getimg(div, base_caoliu.rex2)
        for img in imgUrlArr:
            m += 1
            print('详情页地址为：%s,图片地址为：%s,第%d张图片下载' % (url, img, m))
            img_queue.put(img)


def saveImgQuene(head, session, proxies, img_queue, path, dirpath):
    """
     多线程下载图片
    :param head:
    :param session:
    :param proxies:
    :param img_queue:
    :param path:
    :param dirpath:
    :return:
    """
    i=0
    while True:
        if img_queue.empty():
            break
        url = img_queue.get()
        i = i+1
        print('下载图片线程名:{}, 图片地址：{}'.format(threading.currentThread().getName(), url))
        # 下载当前图片
        base_caoliu.savepic(i, url, session, head, path, dirpath, proxies)
        time.sleep(random.randint(1, 2))


'''
  通过详情页去下载图片
'''
def detail():
    url_detail = str(input("请输入详情页地址： "))
    isproxy = int(input("输入是否需要代理(1或者0)： "))
    num = int(input("输入执行的线程数： "))

    page_queue = Queue()
    img_queue = Queue()
    ##文件夹路径
    save_path = '/Users/jucce/www/picture/'
    time2 = time.strftime('%Y-%m-%d', time.localtime())
    dirpath = save_path + time2
    path = dirpath + '/caoliutv-%d-%d.jpg'

    session = requests.session()

    if isproxy:
        proxies = getProxy()
        print("当前代理地址为：%s" % proxies)
    else:
        proxies = {}

    ##设置request头
    head = {"referer": "http://t66y.com/thread0806.php?fid=16"}
    ua = UserAgent()
    head["User-Agent"] = ua.chrome
    # 通过详情页地址获取图片地址
    setImgQuene(url_detail, head, session, proxies, img_queue)

    for x in range(num):
        t = threading.Thread(target=saveImgQuene, args=(head, session, proxies, img_queue, path, dirpath))
        t.start()




if __name__ == '__main__':
    isList = int(input("请选择爬列表还是详情业(1-列表或者0-详情页)： "))
    if isList:
        main()
    else:
        detail()