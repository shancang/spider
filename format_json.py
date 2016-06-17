# -*- coding: utf-8
import json,sys
#import chardet
def format_json(a):
    comm_dic={}
    veh_dic={}
    for com in json.loads(a)["result"]["specsList"]:
        keys=com["specid"]
        comm_dic[keys]={}

    json_data=json.loads(a)["result"]["paramtypeitems"]
    for item in json_data:
        base_name=item["name"]
        paramitems=item["paramitems"]  
        for base in paramitems :
            veh_name=base["name"]
            veh_list=base["valueitems"]
            for conf in veh_list:
                keys=conf["specid"]
                v_name=conf["value"]
                veh_dic[keys]={veh_name:v_name}
            for k,v in veh_dic.items():
                comm_dic[k].update(veh_dic[k])
    data=json.dumps(comm_dic,indent=2 ,encoding='utf-8', ensure_ascii=False)
    return data




