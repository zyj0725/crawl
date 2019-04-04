#! /usr/bin/python3
# _*_ coding:gbk _*_
'''
    target:爬取51网站上发布的爬虫的职位信息
    author:zyj
    time:2019.3.26
'''

import os
import time
import requests
from pandas import DataFrame
from lxml import etree
from scrapy.selector import Selector

# 得到每一页的url
def crawl_url(url):
	res = requests.get(url)
	res.encoding = 'gbk'
	html = res.text
	# 从html源码获取每一页中爬虫工作的url
	e_html = etree.HTML(html)
	x_html = e_html.xpath('//*[@id="resultList"]/div/p/span/a/@href')
	for job_url in x_html:
		first_job(job_url)

# 获取所有爬虫工作的具体信息
def first_job(job_url):
	res = requests.get(job_url)
	res.encoding = 'gbk'
	html = res.text
	e_html = etree.HTML(html)
	job_name = e_html.xpath('//div[@class="cn"]/h1/text()')[0].strip()    # 职位名称
	post_mesgs = e_html.xpath('//p[@class="msg ltype"]//text()')    # 发布信息
	l_mesg =[]
	for mesg in post_mesgs:
		mes = mesg.strip()
		l_mesg.append(mes)
	mesgs = ''.join(l_mesg)
	company_name = e_html.xpath('//a[@class="catn"]/text()')[0].strip()   # 公司名称
	if e_html.xpath('//div[@class="cn"]/strong/text()'):
		salary = e_html.xpath('//div[@class="cn"]/strong/text()')   # 薪资
	else:
		salary =['无']
	if e_html.xpath('//span[@class="sp4"]//text()'):
		welfare = ','.join(e_html.xpath('//span[@class="sp4"]//text()'))    # 福利待遇
	else:
		welfare = '无'
	if e_html.xpath('//div[@class="tCompany_main"]/div[3]'):
		addr = e_html.xpath('//div[@class="bmsg inbox"]/p/text()')[1].strip()   # 上班地址
	else:
		addr = '无'
	occ_info = ','.join(e_html.xpath('//div[@class="bmsg job_msg inbox"]/p//text()'))  # 职位信息
	data = {
		'职位名称':[job_name],'公司名称':[company_name],'薪资':salary,
		'福利':[welfare],'发布信息':[mesgs],'上班地址':[addr]
	}

	save_job(data)

# 以csv格式保存职位信息
def save_job(data):
	job = DataFrame(data)
	job_csv = job.to_csv('crawler_51job.csv',mode='a',encoding='gbk',index=False,header=False)

# 确定好爬取范围
def job_url():
	baseurl = 'https://search.51job.com/list/040000,000000,0000,00,9,99,%25E7%2588%25AC%25E8%2599%25AB,2,'
	start = int(input("请输入一个整数:"))
	end = int(input("请输入一个整数:"))
	for num in range(start,end+1):
		# 拼接url
		url = baseurl + str(num) + '.html'
		print('正在爬取第 %d 页' % num)
		time.sleep(0.5)
		crawl_url(url)
		print('第%d页爬取完成' % num)

job_url()
print("爬取结束")