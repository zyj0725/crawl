#! /usr/bin/python3
# _*_ coding:gbk _*_
'''
    target:��ȡ51��վ�Ϸ����������ְλ��Ϣ
    author:zyj
    time:2019.3.26
'''

import os
import time
import requests
from pandas import DataFrame
from lxml import etree
from scrapy.selector import Selector

# �õ�ÿһҳ��url
def crawl_url(url):
	res = requests.get(url)
	res.encoding = 'gbk'
	html = res.text
	# ��htmlԴ���ȡÿһҳ�����湤����url
	e_html = etree.HTML(html)
	x_html = e_html.xpath('//*[@id="resultList"]/div/p/span/a/@href')
	for job_url in x_html:
		first_job(job_url)

# ��ȡ�������湤���ľ�����Ϣ
def first_job(job_url):
	res = requests.get(job_url)
	res.encoding = 'gbk'
	html = res.text
	e_html = etree.HTML(html)
	job_name = e_html.xpath('//div[@class="cn"]/h1/text()')[0].strip()    # ְλ����
	post_mesgs = e_html.xpath('//p[@class="msg ltype"]//text()')    # ������Ϣ
	l_mesg =[]
	for mesg in post_mesgs:
		mes = mesg.strip()
		l_mesg.append(mes)
	mesgs = ''.join(l_mesg)
	company_name = e_html.xpath('//a[@class="catn"]/text()')[0].strip()   # ��˾����
	if e_html.xpath('//div[@class="cn"]/strong/text()'):
		salary = e_html.xpath('//div[@class="cn"]/strong/text()')   # н��
	else:
		salary =['��']
	if e_html.xpath('//span[@class="sp4"]//text()'):
		welfare = ','.join(e_html.xpath('//span[@class="sp4"]//text()'))    # ��������
	else:
		welfare = '��'
	if e_html.xpath('//div[@class="tCompany_main"]/div[3]'):
		addr = e_html.xpath('//div[@class="bmsg inbox"]/p/text()')[1].strip()   # �ϰ��ַ
	else:
		addr = '��'
	occ_info = ','.join(e_html.xpath('//div[@class="bmsg job_msg inbox"]/p//text()'))  # ְλ��Ϣ
	data = {
		'ְλ����':[job_name],'��˾����':[company_name],'н��':salary,
		'����':[welfare],'������Ϣ':[mesgs],'�ϰ��ַ':[addr]
	}

	save_job(data)

# ��csv��ʽ����ְλ��Ϣ
def save_job(data):
	job = DataFrame(data)
	job_csv = job.to_csv('crawler_51job.csv',mode='a',encoding='gbk',index=False,header=False)

# ȷ������ȡ��Χ
def job_url():
	baseurl = 'https://search.51job.com/list/040000,000000,0000,00,9,99,%25E7%2588%25AC%25E8%2599%25AB,2,'
	start = int(input("������һ������:"))
	end = int(input("������һ������:"))
	for num in range(start,end+1):
		# ƴ��url
		url = baseurl + str(num) + '.html'
		print('������ȡ�� %d ҳ' % num)
		time.sleep(0.5)
		crawl_url(url)
		print('��%dҳ��ȡ���' % num)

job_url()
print("��ȡ����")