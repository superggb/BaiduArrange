# coding=utf-8

from bs4 import BeautifulSoup

import requests
import sys

baiduUrl = "http://www.baidu.com"
# 取出一个网页的html的方法封装
def get_html(url):
    f = requests.get(url)
    # print f.content
    f.encoding = 'gbk2312'
    soup = BeautifulSoup(f.content, "lxml")
    return soup


## 该函数用于处理用户自定义参数，第一个参数为搜索目标，第二个参数为搜索页码
def argument_deal():
    arg = [0,0,0]
    if len(sys.argv) == 2:
        arg[0] = 1
        arg[1] = sys.argv[1].decode('gbk') #命令行如果有中文参数，需要按gbk解码，不然会显示乱码
    elif len(sys.argv) == 3:
        arg[0] = 2
        arg[1] = sys.argv[1].decode('gbk')
        #第二个参数要判断使其位于1到9之间
        if int(sys.argv[2])>1 and int(sys.argv[2])<10:
            arg[2] = sys.argv[2]
        else:
            arg[2] = 1
    return arg

def main():
    fo = open("result.txt", "w+")
    pages = 4  # pages表示总共搜索几页内容
    target = "720全景"
    arg = argument_deal()
    #print arg
    if arg[0] == 1:
        target = arg[1]
    elif arg[0] == 2:
        target = arg[1]
        pages = int(arg[2])+1 #注意这里要把参数中的字符串转换为数字，否则会造成后面死循环
    arrange = 1 #初始化排名
    times = 1
    soup = get_html(baiduUrl+"/s?ie=UTF-8&wd="+target)
    # 获取单个搜索标签内容和链接
    print "please waiting...."
    while(times < pages):
        print "page %d finished"%times
        fo.write("page %d content:"%times+"\n")
        for k in soup.find_all('div', class_='result c-container '):
          for j in k.find_all('h3'):
              #此处获得为整个h3标签，需要去掉href之前的无用css代码
              j = str(j)
              cut = j.find("href")
              fo.write("%d: "%arrange + j[cut:]+"\n")
              arrange = arrange+1
        ## 获取当前页面下一页对应的url去除其中的第一个“amp;”以此获得跳转下一页的链接(amp为url中的空格转码出来的多余字符，在笔记本中会显示，但在程序字符串处理过程中并不会出现，所以不用做处理)
        next = soup.find_all("a", class_='n')
        for item in next:
            nextUrl= item.get("href")
        #  print nextUrl
        nextPage = baiduUrl+nextUrl
        soup = get_html(nextPage)
        times = times+1
    fo.close()
    print "finished"



if __name__=='__main__':
       main()


