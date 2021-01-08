import paramiko
import os
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
command='cat /proc/net/dev | awk \'{i++; if(i>2){print $1}}\' | sed \'s/^[\t]*//g\' | sed \'s/[:]*$//g\''
net=os.popen(command).readlines()
n=0
for i in net:
    i=i.replace('\n','')
    net[n]=i
    n+=1
net.remove('lo')
netname=net[0][0:-1]
netname=netname+'1'
print(netname)

#检查是否添加配置文件
command='cat /etc/network/interfaces'
result=os.popen(command).readlines()
result=''.join(result)
for i in lis:
    print(i)
    if i in result:
        print('exist')
        continue
    command='sed -i \'$a iface '+netname+' inet static\' /etc/network/interfaces'
    print(command)
    result=os.popen(command)
    command='sed -i \'$a \ \ \ \ \ \ \ \ address '+i+'/29\'  /etc/network/interfaces'
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
    sleep(1)
    count+=1
