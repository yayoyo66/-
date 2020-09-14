# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import requests
import time
import random
import re


def get_result(ybcode,page=1): #数据的请求
    referer = "https://data.cnki.net/yearbook/Single/" +ybcode
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    data = {'ybcode': ybcode, 'entrycode': '', 'page': page, 'pagerow': '20'}
    headers = {
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Cookie': cookie,
'Origin': "https//data.cnki.net",
'Referer': referer,
'User-Agent': user_agent,
    }
    url = "https://data.cnki.net/Yearbook/PartialGetCatalogResult"
    params = urllib.parse.urlencode(data).encode(encoding='utf-8')
    req = urllib.request.Request(url, params, headers)
    r = urllib.request.urlopen(req)
    res = str(r.read(),'utf-8')
    return res

def get_pageno(ybcode): #获取总页数
    soup = BeautifulSoup(get_result(ybcode), 'lxml')
    pages=int(soup.select('.s_p_listl')[0].get_text().split("共")[2].split('页')[0])
    print('总共'+str(pages)+'页')
    return pages


def dataclear(data): #数据的清理，除去文本中所有的\n和\r
    data=re.sub('\n+',' ',data)
    data = re.sub('\r+', ' ', data)
    data=re.sub(' +',' ',data)
    return data


def filedata(ybcode): #下载知网的统计年鉴之类的所有excel表
    pageno=get_pageno(ybcode)
    for i in range(1,pageno+1,1):
        print ('########################################当前第'+str(i)+'页###################################')
        soup=BeautifulSoup(get_result(ybcode,i),'lxml')
        for j in soup.select('tr'):
            s=BeautifulSoup(str(j),'lxml')
            if len(s.select('img[src="/resources/design/images/nS_down2.png"]'))==0:
                pass
            else:
                try:
                    if len(BeautifulSoup(str(j), 'lxml').select('td:nth-of-type(3) > a'))>=2:
                        title= str(BeautifulSoup(str(j), 'lxml').select('td:nth-of-type(1) > a')[0].get_text())
                        url= 'https://data.cnki.net'+BeautifulSoup(str(j), 'lxml').select('td:nth-of-type(3) > a')[1].get('href')
                        title=dataclear(title) #若不清洗数据，则文件名中会包含\n等特殊字符，导致文件下载错误
                        referer = "https://data.cnki.net/yearbook/Single/" +ybcode
                        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
                        header = {
'Cookie': cookie,
'Host': "data.cnki.net",
'Referer': referer,
'User-Agent': user_agent,
'Connection': 'keep-alive',
'Accept': "text/html, application/xhtml+xml, application/xml;q = 0.9, image/avif, image/webp, image/apng, */*;q = 0.8, application/signed-exchange;v = b3;q = 0.9",
 }
                        filedown(title,url,header)
                        print(title)
                except Exception as e:
                    print ('error:-------------------'+str(e))
                    pass

def filedown(title,url,header): #文件下载函数
    try:
        print("正在下载"+title)
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url,headers=header,verify=False)
        with open(title + ".xls", "wb") as code:
            code.write(r.content)
        print(title+"下载完成")
    except Exception as e:
        print(e)
        pass
    x = random.randint(3,4)
    time.sleep(x)

#自行添加cookie
cookie = ''
#更改此项可下载其他年鉴
ybcode = 'N2019110002'
filedata(ybcode)

#N2019110002 2019年
#N2018110025 2018年
#<a href="/Yearbook/Single/N2018050234">2017年</a>
#<a href="/Yearbook/Single/N2017060038">2016年</a>
#<a href="/Yearbook/Single/N2016030128">2015年</a>
#<a href="/Yearbook/Single/N2015040001">2014年</a>
#<a href="/Yearbook/Single/N2014050073">2013年</a>
#<a href="/Yearbook/Single/N2013040146">2012年</a>
#<a href="/Yearbook/Single/N2012020070">2011年</a>
#<a href="/Yearbook/Single/N2011040042">2010年</a>
#<a href="/Yearbook/Single/N2010042092">2009年</a>
#<a href="/Yearbook/Single/N2009060160">2008年</a>
#<a href="/Yearbook/Single/N2008060073" class="current">2007年</a>
#<a href="/Yearbook/Single/N2008060072">2006年</a>
#<a href="/Yearbook/Single/N2006090503">2005年</a>
#<a href="/Yearbook/Single/N2005110391">2004年</a>
#<a href="/Yearbook/Single/N2005110393">2003年</a>
#<a href="/Yearbook/Single/N2005110392">2002年</a>
#<a href="/Yearbook/Single/N2006010420">2001年</a>
#<a href="/Yearbook/Single/N2006010421">2000年</a>
#<a href="/Yearbook/Single/N2005110394">1999年</a>
#<a href="/Yearbook/Single/N2005110395">1998年</a>
#<a href="/Yearbook/Single/N2005110396">1997年</a>
#<a href="/Yearbook/Single/N2005110397">1996年</a>
#<a href="/Yearbook/Single/N2005110398">1995年</a>
#<a href="/Yearbook/Single/N2005110399">1993-1994年</a>
#<a href="/Yearbook/Single/N2005110400">1992年</a>
#<a href="/Yearbook/Single/N2005110401">1991年</a>
#<a href="/Yearbook/Single/N2005120801">1990年</a>
#<a href="/Yearbook/Single/N2006020063">1989年</a>
#<a href="/Yearbook/Single/N2006010585">1988年</a>
#<a href="/Yearbook/Single/N2006020064">1987年</a>
#<a href="/Yearbook/Single/N2006010586">1986年</a>
#<a href="/Yearbook/Single/N2006010587">1985年</a>