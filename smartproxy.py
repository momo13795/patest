from fake_useragent import UserAgent
import requests

def main():
    head = {}
    ua = UserAgent()
    head["User-Agent"] = ua.random
    url = 'http://ipinfo.io/json'
    url = 'https://t66y.com/thread0806.php?fid=16&search'

    # url = 'http://youtube.com'
    # proxy = f'http://user-tasssa12:test123@china-gate.visitxiangtan.com:8000'
    # proxy = f'https://user-tasssa12-country-us:test123@china-gate.visitxiangtan.com:8000'
    # proxy = 'https://tesaaa:test123@china-gate.visitxiangtan.com:8000'
    # proxy = 'http://35.220.154.111:16443'

    # proxies = {
    #     'http': proxy,
    #     'https': proxy,
    # }
    # response = requests.get(url=url, headers=head, proxies=proxies, timeout=20, verify=False)
    # print(response.text)

    proxy = {"http": "35.220.154.111:16443",  "https": "35.220.154.111:16443"}
    proxy = {"http": "101.251.204.174:8080",  "https": "101.251.204.174:8080"}
    proxy = {"http": "127.0.0.1:58591",  "https": "127.0.0.1:58591"}
    response = requests.get('https://t66y.com/htm_data/2302/16/5559032.html', proxies=proxy)
    # response = requests.get('https://www.baidu.com', proxies=proxy)
    print(response.text)


if __name__ == '__main__':
    main()