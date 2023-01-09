from fake_useragent import UserAgent
import requests

def main():
    head = {}
    ua = UserAgent()
    head["User-Agent"] = ua.random
    url = 'http://ipinfo.io/json'

    url = 'http://youtube.com'
    # proxy = f'http://user-tasssa12:test123@china-gate.visitxiangtan.com:8000'
    # proxy = f'https://user-tasssa12-country-us:test123@china-gate.visitxiangtan.com:8000'
    proxy = f'https://user-tasssa12:test123@china-gate.visitxiangtan.com:8000'

    proxies = {
        'http': proxy,
        'https': proxy,
    }
    response = requests.get(url=url, headers=head, proxies=proxies, timeout=20, verify=False)
    print(response.text)

if __name__ == '__main__':
    main()