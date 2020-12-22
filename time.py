import requests
import time

class timeTaobao(object):
    suTime = 'http://quan.suning.com/getSysTime.do'
    jdTime = 'https://a.jd.com//ajax/queryServerData.html'
    r1 = requests.get(url='http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp',
                      headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'})
    x = eval(r1.text)
    timeNum = int(x['data']['t'])

    def getTime():
        timeStamp = float(timeTaobao.timeNum / 1000)
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime
def c():
    r1 = requests.get(url='http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp',
                      headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'})
    x = eval(r1.text)
    timeNum = int(x['data']['t'])
    return timeNum;

def funcname(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


t = timeTaobao.getTime()
print(t)
# exit()
# if __name__ == '__main__':
#     while 1:
#
#         a = c()
#         b = funcname(a)
#         print(b)
#         time.sleep(1)
#


