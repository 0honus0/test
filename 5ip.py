'''
Author: your name
Date: 2021-01-08 14:58:17
LastEditTime: 2021-01-08 20:27:23
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \python\project\new\5ip.py
'''
import paramiko
import os,re
from time import sleep

#获取5ip
command='curl ifconfig.me'
ip=os.popen(command).readlines()
ip=ip[0].split('.')
lis=[]
lis.append(ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(int(ip[3])+1))
lis.append(ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(int(ip[3])+2))
lis.append(ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(int(ip[3])+3))
lis.append(ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(int(ip[3])+4))
lis.append(ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(int(ip[3])))
print(lis)

def GetIP(number,lis):
    if number<=25:
        ip=lis[0]
    elif number<=50:
        ip=lis[1]
    elif number<=75:
        ip=lis[2]
    elif number<=100:
        ip=lis[3]
    else:
        ip=lis[4]
    return ip


#获取网卡名称
command='cat /etc/network/interfaces'
net=os.popen(command).readlines()
net=''.join(net)
net=net[20:-1]
pat='iface [\s\S]*? inet static'
result=re.search(pat,net).group()
net=result.replace('iface ','').replace(' inet','').replace(' static','')
print(net)

#检查是否添加配置文件
for i in lis:
    command='ip address add '+i+'/29 dev '+str(net)
    print(command)
    result=os.popen(command)

#修改配置文件
command='ls -a'
res=os.popen(command).readlines()
oldport=4001
maxnumber=0
for data in res:
    geshu=data.find('btfs')
    shu=data.replace('.btfs','').replace('btfs','').replace('\n','')
    if geshu!=-1:
        if shu=='':
            shu=0
        else:
            shu=int(shu)
        if (shu > maxnumber):
            maxnumber=shu
print(maxnumber)

suc=False
try:
    username='root'
    port= 22
    ip='127.0.0.1'
    password='Berserker20!SHABIXIANYU!!'
    client=paramiko.SSHClient()
    key=paramiko.AutoAddPolicy()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port, username=username, password=password,timeout=30)
except:
    print('con fail')

count=1
while count<=maxnumber:
    chan = client.invoke_shell()
    chan.send('cd /root\n')
    sleep(1)
    command='export BTFS_PATH=/root/.btfs'+str(count)+'\n'
    print(command)
    chan.send(command)
    sleep(2)
    command='export PATH=${PATH}:${HOME}/btfs'+str(count)+'/bin\n'
    print(command)
    chan.send(command)
    sleep(2)
    ip=GetIP(count,lis)
    port=oldport+count
    print('begin...')
    print(ip)
    print(port)
    command="btfs config --json Addresses.Swarm '[\"/ip4/"+str(ip)+"/tcp/"+str(port)+"\""+",\"/ip4/"+str(ip)+"/udp/"+str(port)+"/quic\"]'"+"\n"
    print(command)
    chan.send(command)
    sleep(3)
    count+=1
