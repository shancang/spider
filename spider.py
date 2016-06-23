# -*- coding: utf-8
import Queue
import cookielib
import threading
import urllib2
import urllib
import re
import time
import sys
import os
import json
from bs4 import BeautifulSoup
from daemonize import Daemonize
import format_json
import chardet
import logging
from db import ConnectDB
db=ConnectDB()
log_dir="/tmp/spider.log"
log_conf=logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%F %H:%M:%S',
                filename='%s' % log_dir,
                filemode='w')
logger=logging.getLogger(__name__)
url="http://www.autohome.com.cn/"
cookie_jar = cookielib.LWPCookieJar()
cookie = urllib2.HTTPCookieProcessor(cookie_jar)
opener = urllib2.build_opener(cookie)
user_agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"

class GetObj(object):
    def __init__(self,url):
        self.url=url
        self.send_headers={'User-Agent':user_agent}

    def getcodeing(self,obj):
        if obj:
            coding=chardet.detect(obj)["encoding"]
            return coding

    def gethtml(self):
        request = urllib2.Request(self.url,headers=self.send_headers)
        try:
            soures_home = opener.open(request,timeout=300).read()
        except urllib2.URLError,e:
            logging.warning(e)
            return None
        except urllib2.HTTPError,e:
            logging.warning(e)
            return None
        return soures_home
    def getconf(self):
        #根据html结果获取配置项的json，并且格式化
        html=self.gethtml()
        coding=self.getcodeing(html)
        if html is not None:
            conf_html=html.decode(coding,"ignore").encode('utf-8')
            w=re.compile(r'(var config =) ({.*})')
            conf_josn=re.search(w,conf_html)
            #print conf_josn
            if hasattr(conf_josn,'group'):
                conf_josn = conf_josn.group(2)
                conf=format_json.format_json(conf_josn)
                return conf
            else:
                return None
        return None

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
        href=item.a.get("href")
        url1[name]=href
    return url1
    #print "%s : %s" % (name,href)
#停售处理函数        
logging.info("start spider.....")
url_1=GetFirstType(url)
for type_name,url2 in url_1.items():
    def thrad(type_name,url2):
        logging.info("name：%s url: %s" % (type_name,url2))
        url2=url2.encode("utf-8")
        obj = GetObj(url2)
        html=obj.gethtml()
        coding=obj.getcodeing(html)
        soup=BeautifulSoup(html,'html5lib',from_encoding=coding)
    
        if type_name == u"电动车":
            logging.info(u"%s pass..." % type_name )
        else:
            #print "----------------------------------------------"
            #print type_name
            #print "----------------------------------------------"
            logging.info("start %s...." % type_name)
            content=soup.find("div",attrs={"class":["tab-content-item","current"]})
            soup=BeautifulSoup(str(content),'html5lib')
    
            #获取二级名称
            name=soup.find_all('div',attrs={"class":"h3-tit"})
            ul=soup.find_all('ul',attrs={"class":"rank-list-ul"})
            for (name_type_2,ul_tag) in zip(name,ul):
                
                firm_name=name_type_2.text
                logging.info("start %s...." % firm_name )
                logging.debug(ul_tag)
                #获取第三级
                soup=BeautifulSoup(str(ul_tag),'html5lib')
                w=re.compile(r's\d+')
                litag=soup.find_all('li',id=w)
                for item in litag:
                    name_type_3=item.h4.text
                    href=item.h4.a.get("href")
                    price=item.div.text
                    url_id=href.split("/")[3]
                    #print "●●%s %s %s" % (name_type_3,price,url_id)
                    #拼接在售车辆的配置页面URL
                    sale_conf_url="http://car.autohome.com.cn/config/series/%s.html" % url_id
                    #拼接停售车辆的配置页面URL
                    stop_sale_conf_url="http://www.autohome.com.cn/%s/sale.html" % url_id
                    url_dic={"sale_conf_url":sale_conf_url,"stop_sale_conf_url":stop_sale_conf_url}
                    #threads=[]
                    for (url_name,sale_url) in url_dic.items():
                        #在售
                        if url_name == "sale_conf_url":
                            #print sale_url
                            #def get_josn():
                            log_mess="在售:%s %s %s %s %s" % (type_name,firm_name,name_type_3,price,url_id)
                            obj=GetObj(sale_url)
                            conf=obj.getconf()
                            if conf:
                                #print conf
                                logging.info(log_mess)
                                conf=json.loads(conf)

                                for (k,v) in conf.items():
                                    v=json.dumps(v,encoding='utf-8', ensure_ascii=False)
                                    status="在售"
                                    db=ConnectDB()
                                    db.insert(table_name="json_data", 
                                                spaceid=k,
                                                status=status ,
                                                type_name=type_name,
                                                manufacturer=firm_name,
                                                name=name_type_3,
                                                price=price,
                                                json_text=v,
                                                Url=sale_conf_url)
                                    db.dbclose()
                            else:
                                mess= u"没有找到相关配置"
                                logging.info("%s %s" % (log_mess,mess))
                                #print mess
                            #t=threading.Thread(target=get_josn)
                            #threads.append(t)
                        else:
                            #停售
                            #def get_stop_conf():
                            obj=GetObj(sale_url)
                            html=obj.gethtml()
                            coding=obj.getcodeing(html)
                            soup=BeautifulSoup(html,'html5lib',from_encoding=coding)
                            filter_html=soup.find_all('div',attrs={"class":"models_nav"})
                            log_mess="停售:%s %s %s %s %s" % (type_name,firm_name,name_type_3,price,url_id)
                            if filter_html:
                                for item in filter_html:
                                    href=item.find('a',text='参数配置').get("href")
                                    stop_sale_conf_url_1=url+href
                                    obj=GetObj(stop_sale_conf_url_1)
                                    conf=obj.getconf()
                                    if conf:
                                        #print conf
                                        logging.info("%s %s" % (log_mess,href))
                                        #print u"在售品牌中的停售车辆"
                                        conf=json.loads(conf)
                                        for (k,v) in conf.items():
                                            #print k,json.dumps(v,encoding='utf-8', ensure_ascii=False)
                                            #db.insert(table_name=json, spaceid=k, json_data=v)
                                            v=json.dumps(v,encoding='utf-8', ensure_ascii=False)
                                            status="停售"
                                            db=ConnectDB()
                                            db.insert(table_name="json_data", 
                                                spaceid=k,
                                                status=status ,
                                                type_name=type_name,
                                                manufacturer=firm_name,
                                                name=name_type_3,
                                                price=price,
                                                json_text=v,
                                                Url=stop_sale_conf_url_1 )
                                            db.dbclose()
                                            
                                        
                                    else:
                                        mess= u"没有找到相关配置"
                                        logging.info("%s %s" % (log_mess,href))
                                        #print mess
                            else:
                                mess= u"没有找到相关配置"
                                logging.info("%s %s" % (log_mess,mess))
    threads=[]                       
    t=threading.Thread(target=thrad,args=(type_name,url2))
    threads.append(t)
    #启动线程，并控制线程在50以内
    for t in threads:
        t.start()
        while True:
            if(len(threading.enumerate()) < 12):
                break
