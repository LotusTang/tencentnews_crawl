# 爬取腾讯新闻信息
***
前言:

　　一般的网站来说，数据要么是在服务端渲染好成为html页面直接返回到浏览器，要么是使用Ajax请求或者js文件里包含所需要的数据，而腾讯新闻则是三种方式
都使用到了，这点确实让人头痛不已。

　　本来我一开始是想要使用Scrapy+Splash去完成这个爬取任务，但是发现Splash渲染后依旧有部分数据无法爬取到，故而最后我选择直接使用requests的方式去编写整个程序。如果腾讯新闻修改了数据的返回形式那么这个代码就失效了，到时候需要根据它修改的新的方式去编写代码。

　　这个代码编写完成的日期为**2019/3/13**，所以请根据自身情况谨慎参考。

　　这个project编写的时候[腾讯首页](https://news.qq.com/)的界面如下图：(查看日期为 2019-3-13)
    
![](https://github.com/cheng-github/tencentnews_crawl/raw/master/show_pictures/腾讯首页.PNG)


开发环境: win10 python3.7 
***
## 分析腾讯新闻网页数据请求构成

在这篇文章内我们主要抓取的是下面三个模块的内容:
1. 今日要闻

2. 热点精选

3. 热门资讯

### 今日要闻

　　打开view page source,显然今日要闻的数据不存在于网站站点源码里，没关系，我们打开F12，切换到Network这个tab下面，若没有内容可以按F5刷新以后再查看。 如果要一个一个文件去翻今日要闻的内容不免过于繁琐，我们可以随意点击其一个标题的链接，然后将该标题的链接后面一串数字记录下来。在调试模式下进行搜索，很快我们可以定位到我们需要寻找的文件。如下图所示:

![](https://github.com/cheng-github/tencentnews_crawl/raw/master/show_pictures/今日要闻3.PNG)

![](https://github.com/cheng-github/tencentnews_crawl/raw/master/show_pictures/今日要闻4.PNG)
  
![](https://github.com/cheng-github/tencentnews_crawl/raw/master/show_pictures/今日要闻5.PNG)

　　在这里我们还可以预览里面的内容:
  
![](https://github.com/cheng-github/tencentnews_crawl/raw/master/show_pictures/今日要闻6.PNG)

这里的get请求的两个参数callback以及pull_urls都是固定值，只需要获取到然后自行解析即可。

### 热点精选

　　热点精选包括两种形式的链接，一种是专题，另外一种是包含新闻内容的普通链接。我们先看热点精选的数据来源请求，同样的方式，我们可以找到对应的内容。
  
![](https://github.com/cheng-github/tencentnews_crawl/raw/master/show_pictures/热点精选.PNG)
  
![](https://github.com/cheng-github/tencentnews_crawl/raw/master/show_pictures/热点精选2.PNG)
  
　　在这个url里面我们可以看到有下面几种参数，
- cid
- ext
- token
- page
- expIds
- callback

　　cid为108表示这是热点精选的请求，ext没有任何值表示，token表示一次会话的值，如果是第一页的数据，expIds的值为空，如果不是第一页，下一页的话它的值是前一页文章内容的id之和，用|隔开。
  
　　每次拼凑下一个请求的expIds,如此传递请求，每次最多提交十个请求，十个请求之后就无法请求更多的数据了。在浏览器中也是如此，下拉十次之后也无法加载更多的数据了。如此我们可以抓取到所有热点精选的链接数据。对于这些链接数据，这里我们分开讨论这两种情况:
   
1.1 普通新闻内容
　　
  普通新闻内容主要分为四种形式的链接，前缀都是news.qq.com，后缀格式如下:

- omn + 日期 + newsid 
- cmsn + 日期 + newsid
- omn + 日期 + newsid + .html
- cmsn + 日期 + newsid + .html

　　对于非html结尾的页面，同样的道理我们依旧可以找到对应的数据请求地址，对于html页面的页面，我们可以使用beautifulsoup对其进行解析。

1.2 专题内容

　　如果链接为专题，我们也可以找到对应的专题下的所有数据来源，
  
![](https://github.com/cheng-github/tencentnews_crawl/raw/master/show_pictures/专题1.PNG)
    
  　　里面的文章id的值存在于节点，object►ext_data►content►0►desc►sectionData►
   
![](https://github.com/cheng-github/tencentnews_crawl/raw/master/show_pictures/专题2.PNG)
  
 　　之后我们可以根据这里所有的文章id，去获取所有的文章内容，因为在专题下，所有文章链接都只有两种形式:
   
   - cmsn + newsid
   - omn + newsid
   
   　　且请求数据的方式也都一样，唯一的可变参数就只有标识文章的id字段，这里就不再赘述。解析请求内容写入数据库即可。
     
### 热门资讯

　　热门资讯部分的参数如下。
  
- cid
- ext
- token
- page
- expIds
- callback

　　cid为4表示为热门资讯，page经过我的测试可以取值从0-599，也就是最多600条请求，expIds为空，callback为固定值__jp3。其内容的获取与热点精选类似，这里也不再赘述。
  
  
## 抓取结果展示

![](https://github.com/cheng-github/tencentnews_crawl/raw/master/show_pictures/数据库1.PNG)

![](https://github.com/cheng-github/tencentnews_crawl/raw/master/show_pictures/数据库2.PNG)

　　数据库表结构建立都存放在sql目录下，需要可以自取。

## 如何运行

　　直接run tencentnews_crawl目录下的CrawlTencentNewsJSFileData.py入口即可,文件中也提供了将其生成windows服务的CrawlTencentNewsService.py文件，目前已捕获已知的异常，如有其它情况可以自行修改。



