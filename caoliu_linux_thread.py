#导入库

import threading # 导入threading模块
from queue import Queue #导入queue模块
from bs4 import BeautifulSoup
import requests
import re
import time
import random
import os
from fake_useragent import UserAgent


baseurl = "http://t66y.com/thread0806.php"
base = 'http://t66y.com/'

#获取详情页url正则
rex1 = re.compile(r'"(htm_data/\d+/\d+/.*?\d+.html)"')

#获取详情页实际图片地址
rex2 = re.compile(r'ess-data="(.*?)"')

#匹配是否是原创
rex3 = re.compile(r'\[([\u4e00-\u9fa5]+.*?)\]')

#rex3 = re.compile(r'"htm_data/\d+/\d+/.*?\d+.html"\s+[^>]+\>(.*?)</')
#获取列表页中文标题
rex4 = re.compile(r'>(\[?[\u4e00-\u9fa5]+.*?)</')

session = requests.session()
cfduid = 'd9f4ecb7595c8be46440b8d62894a33bd1608701116'
c9_lastvisit = '0%091608702730%09%2Fthread0806.php%3F'



##文件夹路径
save_path = '/Users/jucce/www/picture/'
time2 = time.strftime('%Y-%m-%d', time.localtime())
dirpath = save_path + time2
path = save_path + time2  +  '/caoliutv-%d.jpg'

list_quene = Queue()
detail_queue = Queue()
img_queue = Queue()

##获取请求头
def getHead():
    ##设置request头
    head = {"referer": "http://t66y.com/index.php"}
    ua = UserAgent()
    head["User-Agent"] = ua.chrome
    return head

def getProxy():
    proxy = f'https://user-tasssa12-country-us:test123@china-gate.visitxiangtan.com:8000'

    # proxy = f'http://user-tasssa12:test123@gate.visitxiangtan.com:7000'
    proxies = {
        'http': proxy,
        'https': proxy,
    }
    return proxies


def getURL( head,session, proxies, queue, i, isyuanchuang ):

    while queue.empty() is not True:
        url = queue.get()
        print('列表页url: %s,第%d个线程' % (url,i+1))

        ##加上代理ip
        if proxies:
            response = session.get(url=url, headers=head, proxies=proxies, timeout=10)
        else:
             response = requests.get(url=url, headers=head,timeout=20)

        html = response.text
        print('列表页访问情况code:%d' % response.status_code)
        if response.status_code != 200:
            continue

        # 获取每个页面的所有li
        allli = getLI(html)


        for item in allli:

            ## 判断是否是[原创]
            if isyuanchuang == 1:
                if not re.findall(rex3, str(item)):
                    continue

            if re.findall(rex1, str(item)):
                urldetail = str("http://t66y.com/") + str(re.findall(rex1, str(item))[0])
                title = re.findall(rex4, str(item))
                if title:
                    title = re.findall(rex4, str(item))[0]
                    print('当前抓取的url二级页面地址：%s 标题为：%s' % (urldetail, title))
                detail_queue.put(urldetail)
        time.sleep(2)


def getImgs( head,session, proxies, queue, i ):

    while queue.empty() is not True:
        url = queue.get()
        print('当前详情页url: %s,第%d个线程' % (url,i+1))

        ##加上代理ip
        if proxies:
            response = session.get(url=url, headers=head, proxies=proxies, timeout=10)
        else:
             response = requests.get(url=url, headers=head,timeout=20)

        html = response.text
        print('详情页访问情况code:%d' % response.status_code)
        if response.status_code != 200:
            continue

        # 获取每个详情页面的所有li
        div = wuhuDIV(html)
        if re.findall(rex2, str(div)):
            imgUrlArr = getimg(div, rex2)
            # print(imgUrlArr)
            for img in imgUrlArr:
                img_queue.put(img)
                pass
        time.sleep(2)
    pass

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

def savepic(head,session,proxies, queue,index,save_path,dirpath):

    while queue.empty() is not True:
        try:
            img = queue.get()
            print('图片url: %s,第%d个线程' % (img, index + 1))

            if proxies:
                wuhu = session.get(url=img, headers=head, timeout=20, proxies=proxies)
            else:
                wuhu = session.get(url=img, headers=head, timeout=20)

            num = random.randint(1000000000, 9999999999)

            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            where = save_path % (num)
            print('图片url 访问情况 %d' %(wuhu.status_code))
            if wuhu.status_code != 200:
                continue
            f = open(where, 'wb')
            f.write(wuhu.content)
            time.sleep(2)

        except Exception:
            print('异常图片地址：{}' + format(url))
            continue
    pass


def setListQuene(page):
    """
      设置列表队列
    :param page:
    :param list_quene:
    :return:
    """
    for i in range(page):
        if i == 0:
            index = "?fid=16"
        else:
            index = '?fid=16&search=&page=%s' % (i + 1)
        url = baseurl + index

        print('当前抓取第{}页的url地址：{}'.format(i + 1, url))
        list_quene.put(url)
    print("先进先出队列：%s;是否为空：%s；多大,%s;是否满,%s" % (list_quene.queue, list_quene.empty(), list_quene.qsize(), list_quene.full()))
    print('base queue 总页数url 大小 %d' % list_quene.qsize())
    return list_quene

def setDetailQuene(num, head, session, proxies, isyuanchuang):
    print("列表队列： %s" % list_quene.queue)

    ##通过列表来获取详情业队列
    for index in range(num):
        print('列表index:%d' % index)
        thread = threading.Thread(target=getURL, args=(head, session, proxies, list_quene, index, isyuanchuang))
        thread.daemon = True  # 随主线程退出而退出
        thread.start()
        thread.join()

def setImgQuene(num, head, session, proxies):
    ##通过详情页来获取图片队列
    for index in range(num):
        print('详情index:%d' % index)
        thread = threading.Thread(target=getImgs, args=(head, session, proxies, detail_queue, index))
        thread.daemon = True  # 随主线程退出而退出
        thread.start()
        thread.join()

def setSavePic(num, head, session, proxies,path, dirpath):
    ##开始下载图片
    for index in range(num):
        print('下载图片index:%d' % index)
        thread = threading.Thread(target=savepic, args=(head, session, proxies, img_queue, index, path, dirpath))
        thread.daemon = True  # 随主线程退出而退出
        thread.start()
        thread.join()

def main():
    ##进程开始时间
    start_time = time.time()

    page = int(input("输入爬取的页： "))
    num = int(input("输入执行的线程数： "))
    isproxy = int(input("输入是否需要代理(1或者0)： "))
    isyuanchuang = int(input("输入是否需要原创(1或者0)： "))

    ##开启多个进程来获取详情
    list_jin = num
    print("当前几个线程: %d" % list_jin)

    """获取请求头"""
    head = getHead()

    """获取代理地址"""
    if isproxy:
        proxies = getProxy()
        print("当前代理地址为：%s" % proxies)
    else:
        proxies = {}

    """ 获取列表的队列"""
    setListQuene(page)

    """ 获取详情的队列"""
    setDetailQuene(list_jin, head, session, proxies, isyuanchuang)
    print('详情页的 queue 开始大小 %d' % detail_queue.qsize())

    """ 获取图片的队列"""
    setImgQuene(list_jin, head, session, proxies)
    print('img queue 开始大小 %d' % img_queue.qsize())


    """ 下载图片"""
    setSavePic(list_jin, head, session, proxies, path, dirpath)



    print("last time: {} s".format(time.time() - start_time))  # 等ABCD四个线程都结束后，在主进程中计算总爬取时间。



if __name__ == '__main__':
    main()

