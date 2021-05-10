import requests
import json
from time import sleep

API='HND7EMJMNQJHYXXUAJSDSIZMMF7BZWPA273Q'
ip_List=['45.77.212.108']

instances_url='https://api.vultr.com/v2/instances'

headers={
    'Authorization': 'Bearer '+str(API)
}
res=requests.get(instances_url,headers=headers)
all_instances=json.loads(res.text)
for instances in all_instances['instances']:
    ip=instances['main_ip']
    id=instances['id']
    if ip not in ip_List:
        delete_url='https://api.vultr.com/v2/instances/'
        delete_url=delete_url+id
        res=requests.delete(url=delete_url,headers=headers)
        if str(res.status_code)!='204':
            print(ip+' 删除失败')
        print()
        sleep(4)
    else:
        print(ip)


