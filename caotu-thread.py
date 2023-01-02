import threading # 导入threading模块
from queue import Queue #导入queue模块
import time  #导入time模块
from bs4 import BeautifulSoup
import requests
import re
import os
import random
from fake_useragent import UserAgent
baseurl = "https://caotu.org"

rex1 = re.compile(r'href="(\/\S+\d.html)"')
rex2 = re.compile(r'src="(.*?)"')

rex3 = re.compile(r'org/(.*?)/')
# rex4 = re.compile(r'[?[\u4e00-\u9fa5]+.*?]')
rex4 = re.compile(r'title="(.*?)"')

rex5 = re.compile(r'href="\/\S+\d.html"\s+\S+\s+\S+>(.*?)</')

session = requests.session()


##文件夹路径
save_path = 'H:\\pa-pic\\caotu-thread\\'

time2 = time.strftime('%Y-%m-%d', time.localtime())
dirpath = save_path + time2
path = save_path + time2  + '\\caotu-%d.jpg'

header = {

}



##图片类型(rq:人妻，nv:女友,sf:少妇，lp:老婆，lc:露出，sh:骚货，ns:内射，dm:动漫，xz:写真，yz:亚洲，om:欧美)
category  = ['rq','ny','sf','lp','lc','sh','ns','dm','xz','yz','om']
# category  = ['rq']

def getHead():
    # ua = random.choice(ualist)
    ua = UserAgent()

    head = {}
    # head['sec-ch-ua-mobile'] = '?0'
    # head['Sec-Fetch-Dest'] = 'document'
    # head['same-origin'] = 'navigate'
    # head['Sec-Fetch-Site'] = 'same-origin'
    # head['Sec-Fetch-User'] = '?1'
    head["referer"] = "https://caotu.org/"
    head['Upgrade-Insecure-Requests'] = '1'
    head["User-Agent"] = ua.random
    return head

def wuhuDIV(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_links = soup.find('div', class_='entry-content')
    return all_links


##列表访问
def getURL(queue,session,list_queue,i):

    time.sleep(2)
    head = getHead()
    ##加上代理防止ip被封
    proxies = {
        #'http': 'http://derrick:111111@54.186.245.186:3128',
         'http': 'http://mark:111111@35.220.216.199:3128',
    }

    while queue.empty() is not True:
        url = queue.get()
        # print('当前url: %s,第%d个线程' % (url,i+1))
        response = session.get(url=url, headers=head,proxies=proxies)
        # response = requests.get(url=url, headers=head, timeout=10)
        # response = requests.get(url=url, headers=head)
        response.encoding = 'utf-8'
        html = response.text
        print('列页访问情况code:%d'% response.status_code + '此url为：%s' % url)
        if response.status_code != 200:
            continue
        # 获取一级页面的所有li
        allli = getLI(html)

        for item in allli:
            if re.findall(rex1, str(item)):
                url = baseurl + re.findall(rex1, str(item))[0]
                title = re.findall(rex4, str(item))
                if title:
                    title = re.findall(rex4, str(item))[0]
                    print('当前抓取的url二级页面地址：%s 标题为：%s' % (url, title))
                list_queue.put(url)  # Queue队列的put方法用于向Queue队列中放置元素，由于Queue是先进先出队列，所以先被Put的URL也就会被先get出来。


def getimg(div, method2):
    img = re.findall(method2, str(div))
    return img



##详情页访问
def paRun(queue,session,result_queue,i):
    time.sleep(2)
    head = getHead()
    ##加上代理防止ip被封
    proxies = {
        'http': 'http://mark:111111@35.220.216.199:3128',
    }
    while queue.empty() is not True:
        url = queue.get()
        # print('当前url: %s,第%d个线程' % (url,i+1))
        response = session.get(url=url, headers=head,proxies=proxies)
        # response = requests.get(url=url, headers=head, timeout=10)
        # response = requests.get(url=url, headers=head)
        response.encoding = 'utf-8'
        html = response.text
        # print('detail访问情况code:%d'% response.status_code)
        if response.status_code != 200:
            continue
        # detail 所有图片
        allli = wuhuDIV(html)

        if re.findall(rex2, str(allli)):
            imgUrlArr = getimg(allli, rex2)
            for img in imgUrlArr:
                result_queue.put(img)
                pass
    pass


##下载图片
def savePic(queue,session,result_queue,i,dirpath,save_path):
    time.sleep(2)
    head = getHead()
    ##加上代理防止ip被封
    proxies = {
        'http': 'http://mark:111111@35.220.216.199:3128',
    }
    while queue.empty() is not True:
        try:
            url = queue.get()
            # print('当前url: %s,第%d个线程' % (url, i + 1))
            response = session.get(url=url, headers=head, proxies=proxies, timeout=15)
            # response = requests.get(url=url, headers=head, timeout=10)
            # response = requests.get(url=url, headers=head)
            print('图片下载情况code:%d' % response.status_code)
            if response.status_code != 200:
                continue
            num = random.randint(1000000000, 9999999999)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            where = save_path % (num)
            f = open(where, 'wb')
            f.write(response.content)
            result_queue.put(url)
        except Exception as e:
            print(e)
            print('异常图片地址：{}'.format(url))
            continue

    pass

def getLI(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_links = soup.find_all('a', class_='card__media')
    return all_links


#主函数
if __name__ == "__main__":
    ##进程开始时间
    start_time = time.time()
    page = int(input("输入爬取的页数目： "))
    base = Queue()
    list_queue = Queue()
    detail_queue = Queue()
    result_queue = Queue()

    for videocategory in category:

        for i in range(page):
            if i == 0:
                index = "/"
            else:
                index = '/page/%d/' % (i + 1)
            url = baseurl + '/topic/' +videocategory + index
            pageurl = baseurl + '/' + index
            print('当前抓取第{}页的url地址：{},类型为{}'.format(i + 1, url,videocategory))
            base.put(url)

    print ("先进先出队列：%s;是否为空：%s；多大,%s;是否满,%s" % (base.queue, base.empty(), base.qsize(), base.full()))
    print('base queue 开始大小 %d' % base.qsize())
    exit()
    ##开启10个进程来获取详情
    list_jin = 20
    detail_jin = 20
    pic_jin = 20

    list_jin = page
    detail_jin = page
    pic_jin = page
    if page > 10:
        list_jin = 10
        detail_jin = 10
        pic_jin = 10

    ##列表进程获取队列
    for index in range(list_jin):
        # print('index:%d' %index)
        thread = threading.Thread(target=getURL, args=(base, session,list_queue,index))
        thread.daemon = True  # 随主线程退出而退出
        thread.start()
        thread.join()
    print('list queue 开始大小 %d' % list_queue.qsize())

    ##detail进程获取队列
    for index in range(detail_jin):
        # print('index:%d' %index)
        threadDetail = threading.Thread(target=paRun, args=(list_queue, session,detail_queue,index))
        threadDetail.daemon = True  # 随主线程退出而退出
        threadDetail.start()
        threadDetail.join()
    print('detail queue 开始大小 %d' % detail_queue.qsize())


    ##图片进程获取队列
    for index in range(pic_jin):
        # print('index:%d' %index)
        threadPic = threading.Thread(target=savePic, args=(detail_queue, session,result_queue,index,dirpath,path))
        threadPic.daemon = True  # 随主线程退出而退出
        threadPic.start()
        threadPic.join()
    print('pic queue 开始大小 %d' % result_queue.qsize())


    print("last time: {} s".format(time.time()-start_time))#等ABCD四个线程都结束后，在主进程中计算总爬取时间。