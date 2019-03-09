# coding=utf-8
import logging
import os
import re
import time
from urllib.parse import urlparse  # py3
import pdfkit
import requests
import random
from bs4 import BeautifulSoup

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""

class Crawler(object):
    """
    爬虫基类，所有爬虫都应该继承此类
    """
    name = None

    def __init__(self, name, start_url):
        """
        初始化
        :param name: 将要被保存为PDF的文件名称
        :param start_url: 爬虫入口URL
        """
        self.name = name
        self.start_url = start_url
        self.domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(self.start_url))
        self.headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent':'Mozilla/5.0 (Linux; U; Android 6.0; zh-CN; MZ-m2 note Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 MZBrowser/6.5.506 UWS/2.10.1.22 Mobile Safari/537.36'
        }

    @staticmethod
    def request(url, **kwargs):
        """
        网络请求,返回response对象
        :return:
        """
        response = requests.get(url, **kwargs)
        return response

    def parse_menu(self, response):
        """
        从response中解析出所有目录的URL链接
        """
        raise NotImplementedError

    def parse_body(self, response):
        """
        解析正文,由子类实现
        :param response: 爬虫返回的response对象
        :return: 返回经过处理的html正文文本
        """
        raise NotImplementedError

    def get_ip_list(self):
        print("正在获取代理列表...")
        url = 'http://www.xicidaili.com/nn/8'
        html = requests.get(url=url, headers=self.headers).text
        soup = BeautifulSoup(html, 'lxml')
        ips = soup.find(id='ip_list').find_all('tr')
        ip_list = []
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            ip_list.append(tds[1].text + ':' + tds[2].text)
        print("代理列表抓取成功.")
        return ip_list

    def get_random_ip(self,ip_list):
        print("正在设置随机代理...")
        proxy_list = []
        for ip in ip_list:
            proxy_list.append('http://' + ip)
        random.shuffle(proxy_list)
        proxy_ip = random.choice(proxy_list)
        proxies = {'http': proxy_ip}
        print("代理设置成功.")
        return proxies

    def run(self, start_index):
        start = time.time()
        print("Start!")
        iplist = self.get_ip_list()
        proxies = self.get_random_ip(iplist)
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
        htmls = []
        menu_page = self.request(self.start_url, headers=self.headers, proxies=proxies)
        while menu_page.status_code != 200:
            proxies = self.get_random_ip(iplist)  # 更换代理
            menu_page = self.request(self.start_url, headers=self.headers, proxies=proxies)
        for index, url in enumerate(self.parse_menu(menu_page)):
            if index < start_index:  # 程序挂掉之后重新跑
                continue
            body_page = self.request(url, headers=self.headers, proxies=proxies)
            while body_page.status_code != 200:
                proxies = self.get_random_ip(iplist)  # 更换代理
                body_page = self.request(url, headers=self.headers, proxies=proxies)
            html = self.parse_body(body_page)
            f_name = ".".join([str(index), "html"])
            with open(f_name, 'wb') as f:
                if (index + 1) % 10 == 0:
                    time.sleep(5)   # 防止被封，更换代理的同时可以设置一定时间休眠，双保险
                    proxies = self.get_random_ip(iplist)    # 更换代理
                print("正在爬取第 %d 页......" % index)
                f.write(html)
            htmls.append(f_name)

        print("HTML文件下载完成，开始转换PDF")
        pdfkit.from_file(input=htmls, output_path=self.name + ".pdf", options=options)
        print("PDF转换完成，开始清除无用HTML文件")
        for html in htmls:
            os.remove(html)
        total_time = time.time() - start
        print(u"完成！总共耗时：%f 秒" % total_time)


class LiaoxuefengPythonCrawler(Crawler):
    """
    廖雪峰Python3教程
    """
    def parse_menu(self, response):
        bsObj = BeautifulSoup(response.content, "html.parser")
        menu_tag = bsObj.find_all(class_="uk-nav uk-nav-side")[1]
        for li in menu_tag.find_all(class_="x-wiki-index-item"):
            # url = li.a.get("href")
            url = li.get('href')
            # print(li.get('href'))
            # print('')
            if not url.startswith("http"):
                url = "".join([self.domain, url])  # 补全为全路径
            yield url

    def parse_body(self, response):
        try:
            bsObj = BeautifulSoup(response.content, 'html.parser')
            body = bsObj.find_all(class_="x-wiki-content")[0]

            # 加入标题, 居中显示
            title = bsObj.find('h4').get_text()
            center_tag = bsObj.new_tag("center")
            title_tag = bsObj.new_tag('h1')
            title_tag.string = title
            center_tag.insert(1, title_tag)
            body.insert(1, center_tag)

            html = str(body)
            # body中的img标签的src相对路径的改成绝对路径
            pattern = "(<img .*?src=\")(.*?)(\")"

            def func(m):
                if not m.group(2).startswith("http"):
                    rtn = "".join([m.group(1), self.domain, m.group(2), m.group(3)])
                    return rtn
                else:
                    return "".join([m.group(1), m.group(2), m.group(3)])

            html = re.compile(pattern).sub(func, html)
            html = html_template.format(content=html)
            html = html.encode("utf-8")
            return html
        except Exception as e:
            logging.error("解析错误", exc_info=True)


if __name__ == '__main__':
    start_url = "https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000"
    crawler = LiaoxuefengPythonCrawler("廖雪峰Python教程", start_url)
    crawler.run(0)
