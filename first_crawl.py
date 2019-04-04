#! /usr/bin/python3
# _*_ coding:utf-8 _*_
'''
    time：2019.3.20
    author:zyj
    name:尝试写第一个爬虫
'''
import os
import requests
from bs4 import BeautifulSoup

# 选取爬取范围
def next_page():
    begin = int(input("请输入起始页:"))
    end = int(input("请输入结束页:"))
    page = 'https://www.286zh.com/pic/html28/'
    for n in range(begin,end+1):
        if n == 1:
            page_n = page
        else:
            page_n = page + 'index_' + str(n) + '.html'
        pic_one(page_n)

def pic_one(page_n):
    # 第一页图片的url
    url1 = 'https://www.286zh.com/pic/html28/'
    # 获取响应
    res1 = requests.get(page_n)
    # 指定编码格式
    res1.encoding = 'utf-8'
    html1 = res1.text
    # 解析html
    soup = BeautifulSoup(html1,'lxml')
    # 找出所有包含了图片地址的a标签
    a_tag = soup.find_all('a',class_='video-pic loading')
    # 对a标签进行遍历，取出href，并构成一组图片的完整的url
    for href in a_tag:
        href_art = href['href']
        url2 = url1 + href_art.split('/')[3]
        pic_one_first(url2)

# 获取第一页第一组图片url
def pic_one_first(url2):
    res2 = requests.get(url2)
    res2.encoding = 'utf-8'
    html2 = res2.text
    soup2 = BeautifulSoup(html2,'lxml')
    pic_div = soup2.find('div',class_='details-content text-justify')
    for pic_jpg in  pic_div.find_all('img'):
        img_src = pic_jpg.get('src')
        save_pic(img_src)

# 保存图片到本地
def save_pic(img_jpg):
    path = os.getcwd() + '/first_crawl_pictures'
    if not os.path.exists(path):
        os.makedirs(path)
    res3 = requests.get(img_jpg)
    res3.encoding = 'utf-8'
    html3 = res3.content
    file = path + '/' + img_jpg[-15:]
    with open(file,'wb') as p:
        p.write(html3)

next_page()
print('抓取完成')
