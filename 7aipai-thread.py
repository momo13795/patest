import threading # 导入threading模块
from queue import Queue #导入queue模块
import time  #导入time模块
from bs4 import BeautifulSoup
import requests
import re
import os
import random
from fake_useragent import UserAgent

baseurl = "https://www.7aipai.com"

rex1 = re.compile(r'href="(\/\S+\d.html)"')
rex2 = re.compile(r'src="(.*?)"')
rex4 = re.compile(r'title="(.*?)"')

session = requests.session()


##文件夹路径
save_path = 'C:\\Users\\mark\\www\\pic\\7aipaithread\\'
time2 = time.strftime('%Y-%m-%d', time.localtime())
dirpath = save_path + time2
path = save_path + time2  +  '\\7aipai-%d.jpg'
header = {

}


def getHead():
    # ua = random.choice(ualist)
    ua = UserAgent()

    head = {}
    # head['sec-ch-ua-mobile'] = '?0'
    # head['Sec-Fetch-Dest'] = 'document'
    # head['same-origin'] = 'navigate'
    # head['Sec-Fetch-Site'] = 'same-origin'
    # head['Sec-Fetch-User'] = '?1'
    head['Upgrade-Insecure-Requests'] = '1'
    head["User-Agent"] = ua.random
    return head

def wuhuDIV(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_links = soup.find('div', class_='content_left')
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
        # print('detail访问情况code:%d'% response.status_code)
        if response.status_code != 200:
            return
        # detail 所有图片
        allli = wuhuDIV(html)

        if re.findall(rex2, str(allli)):
            imgUrlArr = getimg(allli, rex2)
            for img in imgUrlArr:
                img = baseurl + img
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
            print('当前url: %s,第%d个线程' % (url, i + 1))
            response = session.get(url=url, headers=head, proxies=proxies)
            # response = requests.get(url=url, headers=head, timeout=10)
            # response = requests.get(url=url, headers=head)
            print('图片下载情况code:%d' % response.status_code)
            if response.status_code != 200:
                return
            num = random.randint(1000000000, 9999999999)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            where = save_path % (num)
            f = open(where, 'wb')
            f.write(response.content)
            result_queue.put(url)
        except Exception:
            print('异常图片地址：{}' + format(url))
            continue

    pass

def getLI(html):
    soup = BeautifulSoup(html, 'html.parser')
    allli = soup.find_all('li', class_='i_list list_n2')
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

    #
    # # cookie 实例化
    # c = requests.cookies.RequestsCookieJar()
    # # 定义cookie
    # c.set('PHPSESSID', 'n5q3oqqh0qcl7uhirvanj18kik')
    # session.cookies.update(c)

    for i in range(page):
        if i == 0:
            index = ""
        else:
            index = '/index_%d.html' % (i + 1)
        url = baseurl + index
        print('当前抓取第{}页的url地址：{}'.format(i + 1, url))
        base.put(url)

    # print('base queue 开始大小 %d' % base.qsize())
    print ("先进先出队列：%s;是否为空：%s；多大,%s;是否满,%s" % (base.queue, base.empty(), base.qsize(), base.full()))
    print('base queue 开始大小 %d' % base.qsize())

    ##开启10个进程来获取详情
    list_jin = 20
    detail_jin = 20
    pic_jin = 20

    # list_jin = page
    # detail_jin = page
    # pic_jin = page
    # if page > 10:
    #     list_jin = 10
    #     detail_jin = 10
    #     pic_jin = 10

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