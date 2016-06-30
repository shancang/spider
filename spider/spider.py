# -*- coding: utf-8
import threading
import re
import time
import sys
import json
from bs4 import BeautifulSoup
from getobj import GetObj
from db import ConnectDB
from daemonize import Daemonize
from common import *
db=ConnectDB()


url="http://www.autohome.com.cn/"

#获取费第一级分类URL
def GetFirstType(url):
    obj =  GetObj(url)
    html = obj.gethtml()
    coding = obj.getcodeing(html)
    soup = BeautifulSoup(html,"html5lib",from_encoding=coding)
    m=re.compile(r"navcar")
    content=soup.find_all("li",attrs={"class":m})
    url1={}
    for item in content:
        name=item.a.text
        if name == u"电动车":
            continue
        href=item.a.get("href")
        url1[name]=href
    return url1
    #print "%s : %s" % (name,href)

#数据入库函数
def SaveData(table_name="",brand="",series="",conf="",status="",URL_="",index=""):
    conf=json.loads(conf)
    for (k,v) in conf.items():
        spaceid = k
        models = v[u"车型名称"]
        if models == '-':
            continue
        mth=re.compile(r'(.*)(20\d\d)(.*)')
        y=re.search(mth,models)
        if y:
            year = int(y.group(2))
        else:
            year = 0
        guide_price =v[u"厂商指导价(元)"]
        #f=re.compile(r'(\d+.\d+)')
        #p=re.search(f,guide_price)
        #guide_price=p.group()
        emission_standard=v[u"环保标准"]
        structure=v[u"车身结构"]
        level=v[u"级别"]
        manufacturer=v[u"厂商"]
        json_text=json.dumps(v,encoding='utf-8', ensure_ascii=False)
        db=ConnectDB()
        n = db.select(table_name="spider_json",field="spaceid",value=spaceid)
        if n != 0:
            logger.info("spaceid: %s exists " %  spaceid )
            continue
        db.insert(table_name=table_name, 
                    spaceid=spaceid,
                    brand=brand,
                    series=series,
                    models=models,
                    guide_price=guide_price,
                    level=level,
                    emission_standard=emission_standard,
                    structure=structure,
                    status=status ,
                    manufacturer=manufacturer,
                    year=year,
                    index=index,
                    json_text=json_text,
                    URL_=URL_)
        db.dbclose()

    
#线程函数
def thrad(type_name,url2):
    logger.info("name：%s url: %s" % (type_name,url2))
    url2=url2.encode("utf-8")
    obj = GetObj(url2)
    html=obj.gethtml()
    coding=obj.getcodeing(html)
    soup=BeautifulSoup(html,'html5lib',from_encoding=coding)
    

    #print "----------------------------------------------"
    #print type_name
    #print "----------------------------------------------"
    logger.info("start %s...." % type_name)
    content=soup.find("div",attrs={"class":["tab-content-item","current"]})
    soup=BeautifulSoup(str(content),'html5lib')
    index = soup.find_all('span',attrs={'class':"font-letter"})
    box =  soup.find_all('div',attrs={'class':["uibox-con", "rank-list","rank-list-pic"]})
    for (index,box) in zip(index,box):
    #for item in box:
        #获取字母分割的DIV 同时获取字母索引
        index = index.text.strip()
        brand_soup  = BeautifulSoup(str(box),'html5lib')
        brand_html=brand_soup.find_all('dl')
        for brand_item in brand_html:
            #品牌名称
            brand  = brand_item.dt.text.strip()
            series_html = brand_item.dd
            series_soup=BeautifulSoup(str(series_html),'html5lib')
            manufacturer_name=series_soup.find_all('div',attrs={"class":"h3-tit"})
            ul=series_soup.find_all('ul',attrs={"class":"rank-list-ul"})
            for (manufacturer,ul_tag) in zip(manufacturer_name,ul):
                #获取厂商名称
                manufacturer=manufacturer.text
                logger.info("start %s...." % manufacturer )
                logger.debug(ul_tag)
                soup=BeautifulSoup(str(ul_tag),'html5lib')
                w=re.compile(r's\d+')
                litag=soup.find_all('li',id=w)
                for item in litag:
                    #获取车系名称
                    series=item.h4.text
                    db=ConnectDB()
                    n=db.select(table_name="spider_json",field="series",value=series)
                    db.dbclose()
                    if n != 0:
                        logger.info("%s %s %s exists " % (type_name,brand, series) )
                        continue
                    href=item.h4.a.get("href")
                    price=item.div.text
                    url_id=href.split("/")[3]
                    #print "●●%s %s %s" % (series,price,url_id)
                    #拼接在售车辆的配置页面URL
                    sale_conf_url="http://car.autohome.com.cn/config/series/%s.html" % url_id
                    #拼接停售车辆的配置页面URL
                    stop_sale_conf_url="http://www.autohome.com.cn/%s/sale.html" % url_id
                    url_dic={"sale_conf_url":sale_conf_url,"stop_sale_conf_url":stop_sale_conf_url}
                    #threads=[]
                    for (url_name,sale_url) in url_dic.items():
                        #在售
                        if url_name == "sale_conf_url":
                            status=u"在售"
                            #print sale_url
                            #def get_josn():
                            log_mess="%s:%s %s %s %s %s %s %s" % (status,type_name,index,brand,manufacturer,series,price,url_id)
                            obj=GetObj(sale_url)
                            conf=obj.getconf()
                            if conf:
                                #print conf
                                logger.info(log_mess)
                                SaveData(table_name="spider_json",
                                    brand=brand,
                                    series=series,
                                    conf=conf,
                                    status=status,
                                    index=index,
                                    URL_=sale_conf_url)
                                
                            else:
                                mess= u"没有找到相关配置"
                                logger.info("%s %s" % (log_mess,mess))
                                #print mess
                        else:
                
                            #停售
                            #def get_stop_conf():
                            status=u"停售"
                            obj=GetObj(sale_url)
                            html=obj.gethtml()
                            coding=obj.getcodeing(html)
                            soup=BeautifulSoup(html,'html5lib',from_encoding=coding)
                            filter_html=soup.find_all('div',attrs={"class":"models_nav"})
                            log_mess="%s:%s %s %s %s %s %s %s" % (status,type_name,index,brand,manufacturer,series,price,url_id)
                            if filter_html:
                                for item in filter_html:
                                    href=item.find('a',text=u'参数配置').get("href")
                                    stop_sale_conf_url_1=url+href
                                    obj=GetObj(stop_sale_conf_url_1)
                                    conf=obj.getconf()
                                    if conf:
                                        #print conf
                                        logger.info("%s %s" % (log_mess,href))
                                        SaveData(table_name="spider_json",
                                            brand=brand,
                                            series=series,
                                            conf=conf,
                                            status=status,
                                            index=index,
                                            URL_=stop_sale_conf_url_1)
                                        #print u"在售品牌中的停售车辆"
                
                                    else:
                                        mess= u"没有找到相关配置"
                                        logger.info("%s %s %s" % (log_mess,mess,href))
                                        #print mess
                            else:
                                mess= u"没有找到相关配置"
                                logger.info("%s %s" % (log_mess,mess))

def main():
    logger.info("start spider.....")
    url_1=GetFirstType(url)
    for type_name,url2 in url_1.items():                     
        t=threading.Thread(target=thrad,args=(type_name,url2))
        t.start()
        while True:
            if(len(threading.enumerate()) < THARED_NUMBER + 1 ):
                break

daemon = Daemonize(app="app", pid=PID_FILE, action=main, keep_fds=keep_fds,logger=logger)
daemon.start()
