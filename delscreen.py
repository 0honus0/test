import os
from time import sleep
import time

def gettime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

while(True):
    command='free -m'
    res=os.popen(command).readlines()[2].split()
    print('swap占用:'+str(res[2])+'/'+str(res[1]))
    if int(res[2])>1024:
        print(gettime())
        print('开始删除screen。。。')
        command='ls /root'
        res=os.popen(command).readlines()
        maxnumber=0
        for data in res:
            geshu=data.find('btfs')
            shu=data.replace('btfs','').replace('\n','')
            if geshu!=-1:
                if shu=='':
                    shu=0
                else:
                    shu=int(shu)
                if shu > maxnumber:
                    maxnumber=shu
        command='screen -S run -X quit'
        os.popen(command)
        command='screen -S btfs -X quit'
        os.popen(command)
        for i in range(1,maxnumber+1):
            command='screen -S btfs'+str(i)+'  -X quit'
            os.popen(command)
        print('删除完成。。。')
        print('开始重启btfs。。。')
        command='rm -rf screen.py'
        os.system(command)
        command='rm -rf auto.py'
        os.system(command)
        command='wget https://raw.githubusercontent.com/0honus0/test/main/auto.py'
        os.system(command)
        os.system('screen -dmS run python3 /root/auto.py')
        print('后台重启中。。。')
        count=3600
        while count>0:
            sleep(1)
            count=count-1
            print('\r' + 'sleep中:'+str(3600-count)+'/'+str(3600), end='', flush=True)
    else:
        print(gettime())
        print("正常")
        count=3600
        while count>0:
            sleep(1)
            count=count-1
            print('\r' + 'sleep中:'+str(3600-count)+'/'+str(3600), end='', flush=True)

