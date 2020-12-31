import threading # 导入threading模块
from queue import Queue #导入queue模块
import time  #导入time模块
from bs4 import BeautifulSoup
import requests
import re
import os
import random
baseurl = "https://www.666dav.com/"

##会话
session = requests.session()
rex1 = re.compile(r'href="(/\S+/\d+/)"')
rex4 = re.compile(r'title="(.*?)"')
rex2 = re.compile(r'src="(.*?)"')


##文件夹路径
save_path = '/Users/mark/www/66tv/'
time2 = time.strftime('%Y-%m-%d', time.localtime())
dirpath = save_path + time2

path = save_path + time2 + '/66tvtv-%d.jpg'

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


def getHead():
    ua = random.choice(ualist)

    head = {}
    # head['sec-ch-ua-mobile'] = '?0'
    # head['Sec-Fetch-Dest'] = 'document'
    # head['same-origin'] = 'navigate'
    # head['Sec-Fetch-Site'] = 'same-origin'
    # head['Sec-Fetch-User'] = '?1'
    # head['Upgrade-Insecure-Requests'] = '1'
    # head["User-Agent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    head["User-Agent"] = ua
    return head

def wuhuDIV(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_links = soup.find('div', class_='news-content')
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
        print('当前url: %s,第%d个线程' % (url,i+1))
        response = session.get(url=url, headers=head,proxies=proxies)
        # response = requests.get(url=url, headers=head, timeout=10)
        # response = requests.get(url=url, headers=head)
        response.encoding = 'utf-8'
        html = response.text
        print('列页访问情况code:%d'% response.status_code)
        if response.status_code != 200:
            return
        # 获取一级页面的所有li
        allli = getLI(html)

        for item in allli:
            if re.findall(rex1, str(item)):
                url = baseurl + re.findall(rex1, str(item))[0]
                title = re.findall(rex4, str(item))
                if title:
                    title = re.findall(rex4, str(item))
                    # print('当前抓取的url二级页面地址：%s 标题为：%s' % (url, title))
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
        print('当前url: %s,第%d个线程' % (url,i+1))
        response = session.get(url=url, headers=head,proxies=proxies)
        # response = requests.get(url=url, headers=head, timeout=10)
        # response = requests.get(url=url, headers=head)
        response.encoding = 'utf-8'
        html = response.text
        print('detail访问情况code:%d'% response.status_code)
        if response.status_code != 200:
            return
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
        url = queue.get()
        print('当前url: %s,第%d个线程' % (url,i+1))
        response = session.get(url=url, headers=head,proxies=proxies)
        # response = requests.get(url=url, headers=head, timeout=10)
        # response = requests.get(url=url, headers=head)
        print('图片下载情况code:%d'% response.status_code)
        if response.status_code != 200:
            return
        num = random.randint(1000000000, 9999999999)
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        where = save_path % (i, num)
        f = open(where, 'wb')
        f.write(response.content)
        result_queue.put(url)
    pass

def getLI(html):
    soup = BeautifulSoup(html, 'html.parser')
    allli = soup.find_all('div', class_='thumb')
    return allli

# 爬取文章详情页
def get_detail_html(detail_url_list, id):
    while True:
        url = detail_url_list.get() #Queue队列的get方法用于从队列中提取元素
        if url is None:
            break
        time.sleep(2)  # 延时2s，模拟网络请求和爬取文章详情的过程
        print("thread {id}: get {url} detail finished".format(id=id,url=url)) #打印线程id和被爬取了文章内容的url

# 爬取文章列表页
def get_detail_url(queue):
    for i in range(10000):
        time.sleep(1) # 延时1s，模拟比爬取文章详情要快
        queue.put("http://testedu.com/{id}".format(id=i))#Queue队列的put方法用于向Queue队列中放置元素，由于Queue是先进先出队列，所以先被Put的URL也就会被先get出来。
        print("get detail url {id} end".format(id=i))#打印出得到了哪些文章的url

#主函数
if __name__ == "__main__":
    ##进程开始时间
    start_time = time.time()
    page = int(input("输入爬取的页数目： "))
    base = Queue()
    list_queue = Queue()
    detail_queue = Queue()
    result_queue = Queue()


    # cookie 实例化
    c = requests.cookies.RequestsCookieJar()
    # 定义cookie
    c.set('PHPSESSID', 'n5q3oqqh0qcl7uhirvanj18kik')
    session.cookies.update(c)

    for i in range(page):
        if i == 0:
            index = "zipaitupian/"
        else:
            index = 'zipaitupian/index_%d.html' % (i + 1)
        url = baseurl + index
        print('当前抓取第{}页的url地址：{}'.format(i + 1, url))
        base.put(url)

    # print('base queue 开始大小 %d' % base.qsize())
    print ("先进先出队列：%s;是否为空：%s；多大,%s;是否满,%s" % (base.queue, base.empty(), base.qsize(), base.full()))

    # exit()
    ##开启10个进程来获取详情
    list_jin = page
    detail_jin = page
    if page > 10:
        list_jin = 10
        detail_jin = 10
    ##列表进程获取队列
    for index in range(list_jin):
        # print('index:%d' %index)
        thread = threading.Thread(target=getURL, args=(base, session,list_queue,index))
        thread.daemon = True  # 随主线程退出而退出
        thread.start()
        thread.join()

    print('base queue 开始大小 %d' % base.qsize())
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
    # for index in range(10):
    #     # print('index:%d' %index)
    #     threadPic = threading.Thread(target=savePic, args=(detail_queue, session,result_queue,index,dirpath,path))
    #     threadPic.daemon = True  # 随主线程退出而退出
    #     threadPic.start()
    #     threadPic.join()
    #
    # print('pic queue 开始大小 %d' % detail_queue.qsize())

    exit()



        # #定义拉取详情的进程数
        # jin = 10
        #
        # for index in range(10):
        #     thread = threading.Thread(target=get_detail_html, args=(detail_url_queue, i,))
        #     thread.daemon = True  # 随主线程退出而退出
        #     thread.start()
        #
        # detail_url_queue.join()  # 队列消费完 线程结束
        # end = time.time()
        # print('总耗时：%s' % (end - start_time))
        # print('queue 结束大小 %d' % detail_url_queue.qsize())
        # # print('result_queue 结束大小 %d' % result_queue.qsize())
        #
        # exit()
        # # 先创造四个线程
        # thread = threading.Thread(target=getURL, args=(url,detail_url_queue,)) #A线程负责抓取列表url
        #
        # html_thread = []
        # for i in range(jin):
        #     thread2 = threading.Thread(target=get_detail_html, args=(detail_url_queue, i))
        #     html_thread.append(thread2)  # B C D 线程抓取文章详情
        #
        #
        # # 启动四个线程
        # thread.start()
        # thread.join()
        #
        # for i in range(jin):
        #     html_thread[i].daemon = True
        #     html_thread[i].start()
        #
        # detail_url_queue.join()
        # # 等待所有线程结束，thread.join()函数代表子线程完成之前，其父进程一直处于阻塞状态。
        # #
        # # for i in range(jin):
        # #     html_thread[i].join()
        #
        # print ("先进先出队列：%s;是否为空：%s；多大,%s;是否满,%s" % (detail_url_queue.queue, detail_url_queue.empty(), detail_url_queue.qsize(), detail_url_queue.full()))
        #
        # sum = detail_url_queue.qsize()
        # print('总的队列数：{id}'.format(id=sum))


    exit()

    # 启动四个线程
    thread.start()

    # 等待所有线程结束，thread.join()函数代表子线程完成之前，其父进程一直处于阻塞状态。
    thread.join()
    for i in range(3):
        html_thread[i].join()

    print("last time: {} s".format(time.time()-start_time))#等ABCD四个线程都结束后，在主进程中计算总爬取时间。