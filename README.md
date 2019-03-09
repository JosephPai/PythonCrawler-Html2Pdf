# Python爬虫：抓取廖雪峰老师的Python教程保存为PDF电子书

### Update 2019.03

项目作为博客写在了CSDN上，有不少朋友提示我有 `Index out of range` 错误。

经过检查，应该是网站加强了反爬虫防护措施。

主要进行了三点更新
>* headers模拟浏览器：如果不加的话，服务器会自动识别为bot，返回503

>* 动态ip代理支持：首先爬取部分公开的代理池，从代理池中随机抽取一个设置为当前代理，直至status_code返回200

>* 休眠策略，根据需要自行更改。

如果不加动态代理的话，用自己的网络运行程序，过一会儿程序就会报错，然后你会惊喜的发现自己的浏览器好像也无法访问该网站了。不过也不用担心，这只是暂时的，IP封锁一小段时间就会被解除。

加入IP代理后，目前仍旧不是特别稳定，因为抓取的代理池中，有一些无效的或被网站封锁的，所以可能有时会出现不断重复设置代理的情况。

一个暂时的解决办法在代码的121行，如果你的程序从某一页开始挂掉了，例如50页，这个时候你的本地保存了前50页的HTML文件，你可以从51页开始继续完成剩余的任务。

-----


### 环境
python3.6


### 准备工具
爬虫依旧采用requests+BeautifulSoup组合，reuqests 用于网络请求，beautifusoup 用于操作 html 数据。
此外，涉及到把 html 文件转为 pdf，我们采用 wkhtmltopdf ，它可以用适用于多平台的 html 到 pdf 的转换，
pdfkit 是 wkhtmltopdf 的Python封装包。首先安装好下面的依赖包

```python
pip install requests
pip install beautifulsoup4
pip install pdfkit
```
pdfkit使用参考：[pdfkit文档](https://pypi.python.org/pypi/pdfkit/0.4.1)

### 安装 wkhtmltopdf
Windows平台直接在 [http://wkhtmltopdf.org/downloads.html](http://wkhtmltopdf.org/downloads.html) 下载稳定版的 wkhtmltopdf 进行安装，
安装完成之后把该程序的执行路径加入到系统环境 $PATH 变量中，
否则 pdfkit 找不到 wkhtmltopdf 就出现错误 “No wkhtmltopdf executable found”。

在运行程序过程中可能会出现no such file or directory:b'' 
这种错误在python中出现时，意味着有.exe文件需要被调用，而该.exe文件没有被安装或者在控制面板的环境变量中没有添加该.exe的路径。
请再三确认是否已经将wkhtmltopdf安装的bin文件夹路径添加到path中
如果仍旧无法解决问题，程序中需添加代码
```python
config=pdfkit.configuration(wkhtmltopdf=r"D:\software\wkhtmltopdf\bin\wkhtmltopdf.exe")
pdfkit.from_file(htmls, self.name + ".pdf", options=options,configuration=config)
```
即手动导入.exe文件路径


### 运行
```python
python LiaoPythonCrawler.py
```

### 效果图
![image](https://raw.githubusercontent.com/JosephPai/PythonCrawler-Html2Pdf/master/asserts/01.jpg)
![image](https://raw.githubusercontent.com/JosephPai/PythonCrawler-Html2Pdf/master/asserts/02.jpg)


### 参考链接
  https://github.com/lzjun567/crawler_html2pdf/tree/master/pdf
  特此感谢
