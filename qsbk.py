import re,requests

'''
url='https://www.qiushibaike.com/8hr/page/2/?s=5001810'
headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"}
r = requests.get(url, headers=headers)
content=r.text
pattern = re.compile(r'<div.*?author clearfix">.*?<h2>(.*?)</h2>.*?<div.*?'+
                         'content">.*?<span>(.*?)</span>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
iterms=re.findall(pattern,content)
for item in iterms:
    hasimage = re.search('<div class="thumb">.*?<image>.*?/>', item[2])
    if not hasimage:
        print(item[0],'\n',item[1],'\n',item[3])
'''
class qsbk:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent}
        # 存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        # 存放程序是否继续运行的变量
        self.enable = False
    def getpage(self,pageindex):
        if pageindex==1:
            url='https://www.qiushibaike.com'
        else:
            url='https://www.qiushibaike.com/8hr/page/'+str(pageindex)+'?s=5002023'
        content = requests.get(url, headers=self.headers).text
        return content
    def getpageiterms(self,pageindex):
        pagecode=self.getpage(pageindex)
        if not pagecode:
            print('頁面加載失敗...')
        pattern = re.compile(r'<div.*?author clearfix">.*?<h2>(.*?)</h2>.*?<div.*?' +
                             'content">.*?<span>(.*?)</span>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)
        iterms = re.findall(pattern, pagecode)
        pageStories = []
        for item in iterms:
            hasimage = re.search('<div class="thumb">.*?<img.*?/>', item[2],re.S)
            if not hasimage:
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR, "\n", item[1])
                # item[0]是一个段子的发布者，item[1]是内容,item[3]是点赞数
                pageStories.append([item[0].strip(), text.strip(), item[3].strip()])
        return pageStories

    # 加载并提取页面的内容，加入到列表中
    def loadpage(self):
        # 如果当前未看的页数少于2页，则加载新一页
        if self.enable == True:
            if len(self.stories) < 2:
                # 获取新一页
                pageStories = self.getpageiterms(self.pageIndex)
                # 将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    # 获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex += 1
                    # 调用该方法，每次敲回车打印输出一个段子

    def getOneStory(self, pageStories, page):
        # 遍历一页的段子
        for story in pageStories:
            # 等待用户输入
            inpu = input()
            # 每当输入回车一次，判断一下是否要加载新页面
            self.loadpage()
            # 如果输入Q则程序结束
            if inpu == "Q":
                self.enable = False
                return
            print(u"第%d页\t发布人:%s\t赞:%s\n%s" % (page, story[0],story[2], story[1]))
    #开始方法
    def start(self):
        print(u"正在读取糗事百科,按回车查看新段子，Q退出")
        #使变量为True，程序可以正常运行
        self.enable = True
        #先加载一页内容
        self.loadpage()
        #局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                #从全局list中获取一页的段子
                pageStories = self.stories[0]
                #当前读到的页数加一
                nowPage += 1
                #将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                #输出该页的段子
                self.getOneStory(pageStories,nowPage)
spider=qsbk()
spider.start()
