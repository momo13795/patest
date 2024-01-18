# 导入库
from bs4 import BeautifulSoup
import requests
import re
import time
import random
import os
from fake_useragent import UserAgent
import threading
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures.thread
import concurrent
import tkinter as tk
from tkinter import ttk
from io import BytesIO
from PIL import Image

import sys


baseurl = "http://t66y.com/thread0806.php"
base = 'http://t66y.com/'
# method1 = re.compile(r'"(.*?\d+.html)"')
# method2 = re.compile(r'src="(.*?)"')

# 获取详情页url正则
rex1 = re.compile(r'"(htm_data/\d+/\d+/.*?\d+.html)"')

# 获取详情页实际图片地址
rex2 = re.compile(r'ess-data="(.*?)"')

# 匹配是否是原创
rex3 = re.compile(r'\[([\u4e00-\u9fa5]+.*?)\]')

# rex3 = re.compile(r'"htm_data/\d+/\d+/.*?\d+.html"\s+[^>]+\>(.*?)</')
# 获取列表页中文标题
rex4 = re.compile(r'>(\[?[\u4e00-\u9fa5]+.*?)</')

session = requests.session()
cfduid = 'd9f4ecb7595c8be46440b8d62894a33bd1608701116'
c9_lastvisit = '0%091608702730%09%2Fthread0806.php%3F'

# save_path = r'C:\Users\mark\www\pic\caoliu\caoliu-%d-%d.jpg'

usable_ip_list = []  # 用于存放通过检测ip后是否可以使用
all_ip_list = []  # 用于存放从网站上抓取到的ip

# save_path = 'H:\\pa-pic\\caoliu\\'
# time2 = time.strftime('%Y-%m-%d', time.localtime())
# dirpath = save_path + time2
# # path = dirpath  +  '\\caoliutv-%d-%d.jpg'
# path = dirpath + '\\caoliutv-%d(总)-%d(分)-%d(随机数).jpg'

header = {}

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
    ua = UserAgent()

    # head["referer"] = "http://t66y.com/"
    # head["Upgrade-Insecure-Requests"] = 1
    head["User-Agent"] = ua.chrome

    # head["User-Agent"] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    # head['Upgrade-Insecure-Requests'] =1
    # head['Cookie'] = 'UM_distinctid=1763cf32cb110d-06a8906ad0eb4d-c791039-1fa400-1763cf32cb24dc; CNZZDATA950900=cnzz_eid%3D790364290-1607340338-%26ntime%3D1607428238; __cfduid=d646897a36daff025a3e893736bd21eed1608205360; 227c9_lastvisit=0%091608896266%09%2Fread.php%3Ftid%3D4248452'
    return head


def getProxy():
    # proxy = f'http://user-tasssa12:test123@gate.visitxiangtan.com:7000'
    # proxy = f'http://user-tasssa12:test123@gate.visitxiangtan.com:7000'
    # proxy = f'http://127.0.0.1:58591'
    # proxy = f'https://user-tasssa12:test1234@china-gate.visitxiangtan.com:8000'
    # proxy = f'http://35.220.154.111:16443'

    # proxy = 'https://tesaaa:test123@china-gate.visitxiangtan.com:8000'
    proxy = '127.0.0.1:58591'

    proxies = {
        'http': proxy,
        'https': proxy,
    }
    return proxies


def getURL(url, head, session, proxies):
    time.sleep(random.randint(1, 2))

    # print("当前请求的 url地址:{}".format(url))

    try:
        ##加上代理ip
        if proxies:
            # url = 'http://ipinfo.io/json'
            # url = 'http://youtube.com'
            response = session.get(url=url, headers=head, proxies=proxies, timeout=20)
            # response = session.get(url=url, headers=head, proxies=proxies, timeout=20, verify=False)
            # response = session.get(url=url, headers=head, proxies=proxies, timeout=10, verify=False)
        else:
            response = requests.get(url=url, headers=head, timeout=20)
        # response.encoding='gbk'

        if response.status_code != 200:
            print('详情页或者列表页状态不正常，地址为%s' % (url))
            return
        html = response.text
        # print(response.status_code)
        # print(response.text)
        return html
    except Exception as msg:
        print('异常图片---地址为%s, 异常内容: %s' % (url, msg))


def getLI(html):
    soup = BeautifulSoup(html, 'html.parser')
    allli = soup.find_all('tr', class_='tr3 t_one tac')
    return allli


def getDetailTitle(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h4', class_='f16')
    return title


def wuhuDIV(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_links = soup.find('div', class_='tpc_content do_not_catch')
    return all_links


def getimg(div, method2):
    img = re.findall(method2, str(div))
    return img


def savepic(sum, liNum, img, session, head, save_path, dirpath, proxies, page):
    try:

        current_thread_name = threading.current_thread().name
        # print("详情页-保存图片--主线程名为---%s" % current_thread_name)
        time.sleep(random.randint(1, 2))

        file_extension = img.split('.')[-1].lower()

        # print("文件扩展名:", file_extension)

        # head = getHead(head)
        if proxies:
            # wuhu = session.get(url=img, headers=head, timeout=20, proxies=proxies, verify=False)
            wuhu = session.get(url=img, headers=head, timeout=20, proxies=proxies)
        else:
            wuhu = session.get(url=img, headers=head, timeout=20)

        num = random.randint(1000000000, 9999999999)

        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        where = save_path % (sum, liNum, num) + "." + file_extension
        # print("图片访问状态 %d， 图片地址 %s， 保存地址：%s" % (wuhu.status_code, img, where))

        if wuhu.status_code != 200:
            print('状态不正确---当前第%d页---图片地址为%s' % (page + 1, img))
            return
        print('详情线程名字：%s, 当前第第%d页，  图片地址为：%s, 保存路径为：%s' % (current_thread_name, page + 1, img, where))
        f = open(where, 'wb')
        f.write(wuhu.content)
        f.close()
    except Exception:
        print('异常图片当前第%d页---图片地址为%s' % (page + 1, img))


def download_images(start, end, isguolv, isyuanchuang, isproxy, guolv, save_path):
    """
    多线程下载图片

    """
    current_thread_name = threading.current_thread().name
    print("当前线程名为---%s ---抓取第%s页 --  %s页的数据" % (current_thread_name, start, end))

    session = requests.session()
    c = requests.cookies.RequestsCookieJar()
    c.set('227c9_lastvisit', c9_lastvisit)
    session.cookies.update(c)

    if isproxy:
        proxies = getProxy()
        print("当前代理地址为：%s" % proxies)
    else:
        proxies = {}

    for i in range(start, end):
        if i == 0:
            index = "?fid=16"
            # "http://t66y.com/thread0806.php?fid=16"
        else:
            index = '?fid=16&search=&page=%s' % (i + 1)

        # 拼接后的详细地址
        url = baseurl + index

        firstUrl = baseurl + index

        page = '当前抓取第{}页的url地址为：{}'.format(i + 1, url)
        print(page)
        # print('当前抓取第%s页的url地址：%s' %(i+1,url))

        ##设置request头
        head = {"referer": "http://t66y.com/index.php"}
        ua = UserAgent()
        head["User-Agent"] = ua.random

        # 请求列表url地址
        html = getURL(url, head, session, proxies)

        main_logic(i, isguolv, isyuanchuang, proxies, session, guolv, head, html, firstUrl, save_path)


def main_logic(i, isguolv, isyuanchuang, proxies, session, guolv, head, html, firstUrl, save_path):
    current_thread_name = threading.current_thread().name

    # print('当前第%d页---isguolv:%s, guolv:%s' % (i + 1, isguolv, guolv))

    # 获取一级页面的所有li
    allli = getLI(html)
    ##图片张数定义
    m = 0
    ##tr 标签定义
    y = 0
    for item in allli:
        y += 1
        ##第一页前7条不抓（一般前面几条是发帖的公告和其他注意事项）
        if isguolv == 1 and i == 0 and y <= guolv:
            print('当前第%d页---isguolv:%s, guolv:%s, y:%s' % (i + 1, isguolv, guolv, y))
            continue
        print('当前第%d页---第%d条li' % (i + 1, y))

        ## 判断是否是[原创]
        if isyuanchuang == 1:
            if not re.findall(rex3, str(item)):
                continue

        if re.findall(rex1, str(item)):
            # print(item)
            url = base + re.findall(rex1, str(item))[0]
            # print('详情页地址为： %s' % url)

            title = re.findall(rex4, str(item))
            if title:
                title = re.findall(rex4, str(item))[0]
                # save_path = 'H:\\pa-pic\\caoliu\\'
                time2 = time.strftime('%Y-%m-%d', time.localtime())
                dirpath = save_path + time2
                dirpath = dirpath + '\\' + title
                path = dirpath + '\\caoliutv-%d(总)-%d(分)-%d(随机数)'
                print('当前第%d页---当前目录地址 %s' % (i + 1, dirpath))
                if not os.path.exists(dirpath):
                    os.makedirs(dirpath)
                print('当前第%d页---当前抓取的url二级页面地址：%s 标题为：%s' % (i + 1, url, title))
            else:
                continue
            # print(title)
            # exit()

            ##设置二级页面request头
            # head = {}
            head["referer"] = firstUrl
            # head = getHead(head)

            # 请求详情页的url地址
            print("当前第%d页---开始访问详情页+++++++++++++++++++++++++" % (i + 1))
            html = getURL(url, head, session, proxies)
            div = wuhuDIV(html)

            if re.findall(rex2, str(div)):

                imgUrlArr = getimg(div, rex2)
                # print(imgUrlArr)

                # 每个详情进行多线程下载
                with ThreadPoolExecutor(max_workers=5) as executor:
                    futures = []

                    for liNum, link in enumerate(imgUrlArr):
                        future = executor.submit(savepic, m, liNum + 1, link, session, head, path, dirpath, proxies, i)
                        futures.append(future)

                    # Wait for all image downloads to complete
                    for future in futures:
                        future.result()

                    current_thread_name = threading.current_thread().name
                    print("详情页---主线程名为---%s" % current_thread_name)

                # liNum = 0
                # for img in imgUrlArr:
                #     m += 1
                #     liNum += 1
                #     print('当前线程名为---%s---当前第%d页---下载中---标签地址为：%s,图片地址为：%s,总共%d张图片，当前地址第%d张' % (current_thread_name,i + 1, url, img, m, liNum))
                #
                #     # 下载当前图片
                #     savepic(m, liNum, img, session, head, path, dirpath, proxies, i)
                #
                #     time.sleep(2)


def mainThread(url_entry, output_text, page_entry, threadnum_entry, isguolv_entry, guolv_entry, isyuanchuang_entry,
               isproxy_entry, savepath_entry):
    guolv = 9
    print('开始爬虫草榴地址...')
    isguolv = int(isguolv_entry.get())
    guolv = int(guolv_entry.get())
    isyuanchuang = int(isyuanchuang_entry.get())
    isproxy = int(isproxy_entry.get())
    if not savepath_entry.get():
        print("保存目录为空")
        save_path = 'H:\\pa-pic\\caoliu\\'
    else:
        save_path = str(savepath_entry.get())
    num_threads = int(threadnum_entry.get())  # 开启几个线程
    total_pages = int(page_entry.get())  # 爬取总页数

    print("过滤数：%s" % guolv)
    # Calculate pages per thread
    pages_per_thread = total_pages // num_threads  # 计算每个线程爬取的页数

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []

        for i in range(num_threads):
            start_page = i * pages_per_thread
            end_page = (i + 1) * pages_per_thread
            if i == num_threads - 1:
                end_page = total_pages
            future = executor.submit(download_images, start_page, end_page, isguolv, isyuanchuang, isproxy, guolv, save_path)
            futures.append(future)

        # Wait for all threads to complete
        concurrent.futures.wait(futures)

        current_thread_name = threading.current_thread().name
        print("主线程名为---%s" % current_thread_name)


if __name__ == '__main__':
    # 当前文件夹目录
    current_folder = os.getcwd()
    # 创建 GUI 界面
    root = tk.Tk()
    root.title("草榴地址图片爬取")

    # 输入框--url
    url_label = tk.Label(root, text="url输入：", font=("黑体", 10, "bold"))
    url_label.pack()
    url_entry = tk.Entry(root, width=30)
    url_entry.pack()

    # 输入框--爬取页面
    page_label = tk.Label(root, text="爬取页面数(默认2)：", font=("黑体", 10, "bold"))
    page_label.pack()
    page_entry = tk.Entry(root, width=30)
    page_entry.insert(tk.END, 1)
    page_entry.pack()

    # 输入框--线程数
    threadnum_label = tk.Label(root, text="输入线程数：", font=("黑体", 10, "bold"))
    threadnum_label.pack()
    threadnum_entry = tk.Entry(root, width=30)
    threadnum_entry.insert(tk.END, 2)
    threadnum_entry.pack()

    # 输入框--保存位置
    savepath_label = tk.Label(root, text="输入保存目录：", font=("黑体", 10, "bold"))
    savepath_label.pack()
    savepath_entry = tk.Entry(root, width=30)
    savepath_entry.insert(tk.END, current_folder + "\\pa-pic\\")
    savepath_entry.pack()

    # 输入框--是否过滤
    isguolv_label = tk.Label(root, text="输入是否过滤(1或者0)：", font=("黑体", 10, "bold"))
    isguolv_label.pack()
    isguolv_entry = tk.Entry(root, width=30)
    isguolv_entry.insert(tk.END, 1)
    isguolv_entry.pack()

    # 输入框--过滤数
    guolv_label = tk.Label(root, text="输入过滤数(默认9)：", font=("黑体", 10, "bold"))
    guolv_label.pack()
    guolv_entry = tk.Entry(root, width=30)
    guolv_entry.insert(tk.END, 9)
    guolv_entry.pack()

    # 输入框--是否原创
    isyuanchuang_label = tk.Label(root, text="是否原创(1或者0)：", font=("黑体", 10, "bold"))
    isyuanchuang_label.pack()
    isyuanchuang_entry = tk.Entry(root, width=30)
    isyuanchuang_entry.insert(tk.END, 1)
    isyuanchuang_entry.pack()

    # 输入框--是否代理
    isproxy_label = tk.Label(root, text="输入是否代理(1或者0)：", font=("黑体", 10, "bold"))
    isproxy_label.pack()
    isproxy_entry = tk.Entry(root, width=30)
    isproxy_entry.insert(tk.END, 1)
    isproxy_entry.pack()

    # 输出文本框
    output_text = tk.Text(root, height=10, width=50)
    output_text.insert(tk.END, "开始爬虫中......\n")
    output_text.pack()

    # 开始按钮
    start_button = tk.Button(root, text="开始爬虫",
                             command=lambda: mainThread(url_entry, output_text, page_entry, threadnum_entry,
                                                        isguolv_entry, guolv_entry, isyuanchuang_entry, isproxy_entry,
                                                        savepath_entry))
    start_button.pack()

    # 运行 GUI 主循环
    root.mainloop()
