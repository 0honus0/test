import os
from time import sleep

lis=0
maxnumber=0
res=os.popen('ls')
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
print(maxnumber)

os.system('wget https://raw.githubusercontent.com/0honus0/test/main/screen.py')
while(lis<=maxnumber):
    print('第',lis,'个')
    sleep(2)
    if lis==0:
        com='sed -i s/change_this_number/0/g /root/screen.py'
    else:
        com='sed -i s/lis='+str(lis-1)+'/lis='+str(lis)+'/g /root/screen.py'
    print(com)
    os.system(com)
    if lis==0:
        com='screen -S btfs'
    else:
        com='screen -S btfs'+str(lis)
    print(com)
    com='python3 /root/screen.py'
    lis+=1
    print('wait')
    sleep(20)

    #sleep(1200)
