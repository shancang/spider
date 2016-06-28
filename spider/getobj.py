# -*- coding: utf-8
import cookielib
import urllib2
import urllib
import re
import chardet
from format_json import FormatJson

class GetObj(object):

    def __init__(self,url):
        cookie_jar = cookielib.LWPCookieJar()
        cookie = urllib2.HTTPCookieProcessor(cookie_jar)
        self.opener = urllib2.build_opener(cookie)
        user_agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
        self.url=url
        self.send_headers={'User-Agent':user_agent}

    def getcodeing(self,obj):
        if obj:
            coding=chardet.detect(obj)["encoding"]
            return coding

    def gethtml(self):
        request = urllib2.Request(self.url,headers=self.send_headers)
        try:
            soures_home = self.opener.open(request).read()
        except urllib2.URLError,e:
            return None
        except urllib2.HTTPError,e:
            return None
        return soures_home
    def getconf(self):
        #根据html结果获取配置项的json，并且格式化
        html=self.gethtml()
        coding=self.getcodeing(html)
        if html is not None:
            html=html.decode(coding,"ignore").encode('utf-8')
            c=re.compile(r'(var config =) ({.*})')
            o=re.compile(r'(var option =) ({.*})')
            conf_josn   =   re.search(c,html)
            option_josn =   re.search(o,html)
            #print conf_josn
            if hasattr(conf_josn,'group') and hasattr(option_josn,'group'):
                conf_josn = conf_josn.group(2)
                option_josn = option_josn.group(2)
                json=FormatJson()
                conf_json=json.format_json(conf_josn,"conf")
                option_josn=json.format_json(option_josn,"option")
                config = json.json_plus(conf_json,option_josn)
                return config
            else:
                return None
        return None


