import paramiko
import re,os
from time import sleep
import sys
import xlrd
import xlwt
from xlutils.copy import copy
import time

i=0
max_test=3

time=time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
print(time)
data=xlrd.open_workbook("D:/Study/python/data.xls",formatting_info=True)
#data1=xlrd.open_workbook("D:/Study/python/BttWallet.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)                 #List
password_List=table.col_values(1)           #List
#excel=copy(data1)
#行数
row=table.nrows

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('BttWallet')

tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'password')
tables.write(0, 2, 'Mnemonic')
tables.write(0, 3, 'PeerID')
tables.write(0, 4, 'PrivKey')
tables.write(0, 5, 'Score')
tables.write(0, 6, 'BttWalletBalance')
tables.write(0, 7, 'Storage_disk_available')
tables.write(0, 8, 'Online')
tables.write(0, 9, 'check')
tables.write(0, 10, 'uptime_score')
tables.write(0, 11, 'age_score')
tables.write(0, 12, 'version_score')
tables.write(0, 13, 'speed_score')

while row > i:
    count=0
    success=False

    while count < max_test and not success:
        try:
            username='root'
            port= 22
            ip=ip_List[i]
            password=password_List[i]
            print(ip)
            print(password)
            print('当前在第'+str(i+1)+'个')
            print('尝试第'+str(count+1)+'次登陆')
            client=paramiko.SSHClient()
            key=paramiko.AutoAddPolicy()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port, username=username, password=password,timeout=30)
            success = True
        except:
            if count == max_test-1:
                tables.write(i+1,0,ip_List[i])
                tables.write(i+1,1,password)
                tables.write(i+1,6,'loginfailed')
                excel.save('BttWallet.xls')
                count=0
                i=i+1
                print('连接失败，开始下一个')
            else:
                print('登陆失败，尝试重新登陆')
                count +=1

    if success:
        print("连接成功")

        flag=False
        command='apt -y install net-tools'
        stdin , stdout, stderr=client.exec_command(command)
        sleep(1)
        command='netstat -ntulp |grep 4001'
        print(command)
        stdin , stdout, stderr=client.exec_command(command)
        result=stdout.readlines()
        #print(result)
        for data in result:
            if data.find('btfs')!=-1:
                flag=True
        if flag:
            com='cat .btfs/config'
            command=(com)
            stdin, stdout, stderr = client.exec_command(command)
            results = stdout.readlines()
            find=False
            find1=False
            find2=False
            for data in results:
                pat="\"Mnemonic\": (?:'|\").*(?:'|\")"
                if re.search(pat , data)!=None:
                    Mnemonic = re.search(pat , data).group()
                    Mnemonic = Mnemonic[13:len(Mnemonic)-1]
                    print(Mnemonic)
            for data in results:
                pat="\"PeerID\": (?:'|\").*(?:'|\")"
                if re.search(pat , data)!=None:
                    PeerID=re.search(pat , data).group()
                    PeerID = PeerID[11:len(PeerID)-1]
                    print(PeerID)
            for data in results:
                pat="\"PrivKey\": (?:'|\").*(?:'|\")"
                if re.search(pat , data)!=None:
                    PrivKey=re.search(pat , data).group()
                    PrivKey =PrivKey[12:len(PrivKey)-1]
                    print(PrivKey)
            tables.write(i+1, 2, Mnemonic)
            tables.write(i+1, 3, PeerID)
            tables.write(i+1, 4, PrivKey)
            Mnemonic=''
            PeerID=''
            PrivKey=''

            command='btfs/bin/btfs storage stats info'
            stdin , stdout, stderr=client.exec_command(command)
            result=stdout.readlines()
            #print(result)
            for data in result:
                pat='"score":[0-9]+([.]{1}[0-9]+){0,1}'
                Score=re.search(pat,data)
                if Score!=None:
                    Score=Score.group(0)
                pat1='"storage_disk_available":[0-9]+([.]{1}[0-9]+){0,1}'
                Storage_disk_available=re.search(pat1,data)
                if Storage_disk_available!=None:
                    Storage_disk_available=Storage_disk_available.group(0)
                pat2='"online":(\w+),'
                Online=re.search(pat2,data)
                if Online!=None:
                    Online=Online.group(0)
                pat3='"uptime_score":(\w+)'
                Uptime_score=re.search(pat3,data)
                if Uptime_score!=None:
                    Uptime_score=re.search(pat3,data).group(0)
                pat4='"age_score":(\w+)'
                Age_score=re.search(pat4,data)
                if Age_score!=None:
                    Age_score=re.search(pat4,data).group(0)
                pat5='"version_score":(\w+)'
                Version_score=re.search(pat5,data)
                if Version_score!=None:
                    Version_score=re.search(pat5,data).group(0)
                pat6='"speed_score":(\w+)'
                Speed_score=re.search(pat6,data)
                if Speed_score!=None:
                    Speed_score=re.search(pat6,data).group(0)
            command='btfs/bin/btfs wallet balance'
            stdin , stdout, stderr=client.exec_command(command)
            result=stdout.readlines()
            for data in result:
                pat='"BttWalletBalance":[0-9]+([.]{1}[0-9]+){0,1}'
                BttWalletBalance=re.search(pat,data)
                if BttWalletBalance!=None:
                    BttWalletBalance=BttWalletBalance.group(0)
            print(Score[:])
            print(BttWalletBalance[:])
            print(Storage_disk_available[:])
            print(Online[:-1])
            print(Uptime_score[:])
            print(Age_score[:])
            print(Version_score[:])
            print(Speed_score[:])
            tables.write(i+1,5,Score[8:])
            tables.write(i+1,6,BttWalletBalance[19:])
            tables.write(i+1,7,Storage_disk_available[25:])
            tables.write(i+1,8,Online[9:-1])
            tables.write(i+1,10, Uptime_score[15:])
            tables.write(i+1,11, Age_score[12:])
            tables.write(i+1,12, Version_score[16:])
            tables.write(i+1,13, Speed_score[14:])
            Score=''
            BttWalletBalance=''
            Storage_disk_available=''
            Online=''
            Uptime_score=''
            Age_score=''
            Version_score=''
            Speed_score=''
        client.close()
        # 8 19 25
        tables.write(i+1,0,ip)
        tables.write(i+1,1,password)
        if not flag:
            tables.write(i+1,9,'runfailed')
        print("完成")
        mingzi=time+".xls"
        print(mingzi)
        excel.save(mingzi)
        count=0
        i=i+1
    else:
        print("连接失败")
