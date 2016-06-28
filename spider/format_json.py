# -*- coding: utf-8
import json,sys,re
#import chardet
class FormatJson(object):
    def __init__(self):
        pass
    def format_json(slef,a,option):
    
        if option == "conf":
            par_type = "paramtypeitems"
            par = "paramitems"
        elif option == "option":
            par_type = "configtypeitems"
            par = "configitems"
    
        comm_dic={}
        veh_dic={}
        for com in json.loads(a)["result"]["specsList"]:
            keys=com["specid"]
            comm_dic[keys]={}
    
        json_data=json.loads(a)["result"][par_type]
        for item in json_data:
            base_name=item["name"]
            paramitems=item[par]  
            for base in paramitems :
                veh_name=base["name"]
                veh_list=base["valueitems"]
                for conf in veh_list:
                    keys=conf["specid"]
                    v_name=conf["value"]
                    if option == "option":
                        v_name=v_name.replace('&nbsp;','')
                        v_name=v_name.replace(u'●',u'有')
                        v_name=v_name.replace(u'-',u'无')
                    veh_dic[keys]={veh_name:v_name}
                for k,v in veh_dic.items():
                    comm_dic[k].update(veh_dic[k])
        #data=json.dumps(comm_dic,indent=2 ,encoding='utf-8', ensure_ascii=False)
        return comm_dic

    def json_plus(self,a,b):
        for k,v in a.items():
            b[k].update(a[k])
        data = json.dumps(b,indent=2 ,encoding='utf-8', ensure_ascii=False)

        return data





