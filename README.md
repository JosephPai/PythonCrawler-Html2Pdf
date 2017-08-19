# Python爬虫：抓取廖雪峰老师的Python教程保存为PDF电子书

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
python crawler.py
```

### 效果图
