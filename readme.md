# bilibili_spider

2020的B站用户+视频爬虫，包含代码详解，使用scrapy框架，爬取字段30+

## 项目环境

- python版本：3.7.4
- scrapy版本：1.6.0
- 数据库：MySQL  5.6
- 第三方库：fake_useragent 0.1.11；mysqlclient 1.3.14

##### 分析与可视化（暂定）：

- 数据分析：weka
- 数据可视化：pyechart、fineBI

***

### scrapy架构图：

<img src="resource\架构图.jpg" alt="架构图" style="zoom:50%;" />

### 模块简要介绍：

- **spider：**写爬虫的地方，请求并处理响应页面
- **item/item pipeline：**item用于暂存数据；item pipeline用于处理数据，如清洗不需要的数据、将数据存进数据库中等；
  - 若有不同种类的数据（如本项目中的视频数据和用户数据属于不同种类，需要分别存储），则需要使用多个item和item pipeline（在程序中体现为建立不同的类）
- **middleware：**可以简要理解为通过这个组件扩展/自定义scrapy的功能，如使用随机的user-agent和ip，修改downloader组件下载逻辑等；
- 其他模块：不需要编写代码，了解就好
  - downloader：负责下载spider传来的request请求页面，并将响应返回给spider。也就是说，**scrapy框架的请求和下载是分离的（这点与requests库有很大区别）**
  - scheduler：负责调度爬取页面的先后顺序
  - engine：负责各组件间的传输通讯

#### 框架简要逻辑（易懂向，不严谨）：

1. spider请求页面，安排到scheduler里，并逐一交给Downloader下载，Downloader再将响应页面返回给spider处理；
2. spider将处理后的数据（item）交给pipeline，之后pipeline会对数据进一步处理；若数据里有另外要请求的url，则再将其安排到scheduler里；
3. **只需要编写spider、item、pipeline模块，其他的已经在scrapy内部实现**，其他模块可以通过中间件（middleware）进行自定义配置

***

## 代码详解：

#### page_video.py







