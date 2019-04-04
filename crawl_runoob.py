#! /usr/bin/python3
# _*_ coding:utf-8 _*_
"""
    爬取www.runoob.com的python3教程
    time:2019.3.22
    author:zyj
"""
import os
import requests
from bs4 import BeautifulSoup

def all_pages_url(url):
    # first_url = 'http://www.runoob.com/python3/'
    res = requests.get(url)
    res.encoding = 'utf-8'
    html = res.text
    soup = BeautifulSoup(html, 'lxml')
    this_url = soup.find('link', rel='canonical').get('href')
    page_one_url(this_url)

# 获得第一页的内容包括图片地址和文字地址
def page_one_url(url):
    # 发出请求并获得响应
    res = requests.get(url)
    # 指定编码方式
    res.encoding = 'utf-8'
    html = res.text
    # 用lxml解析得到的响应回来的html
    soup = BeautifulSoup(html, 'lxml')
    # 获得文字内容的地址并调用保存文字的函数
    text_url = soup.find(class_='article-intro')
    save_text(text_url)
    # 获得图片的地址并调用保存图片的函数
    pic_url = soup.find('div', class_='article')
    save_pic(pic_url)
    page_next_url(html)

# 将文本内容保存到本地
def save_text(text_url):
    text = text_url.text
    with open('菜鸟教程.txt', 'a', encoding='utf-8') as t:
        t.write(text)

# 将图片保存到本地
def save_pic(pic_url):
    path = os.getcwd() + '/runoob_photos'
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        n = 1
        for pic in pic_url.find_all('img'):
            file = 'http:'+pic.get('src')
            file2 = requests.get(file).content
            filename = path+'/'+file[-8:]
            with open(filename, 'wb') as p:
                print("开始爬取第%d张" % n)
                p.write(file2)
                print("第%d张爬取完成" % n)
                n += 1
    except:
        pass

# 获取下一个url
def page_next_url(next_html):
    while True:
        next_soup = BeautifulSoup(next_html,'lxml')
        a_href = next_soup.find('a',rel='next').get('href')
        all_pages_url(a_href)
        if a_href == 'http://www.runoob.com/python3/python3-examples.html':
            all_pages_url(a_href)
            break


all_pages_url('http://www.runoob.com/python3/')
print("爬取完成")

