import xlrd
import os
import xlwt

xls_file=[]

files=os.listdir()
for file in files:
    if 'xls' in file and file!='compare.xls':
        xls_file.append(file)

all_list=[]
for file in xls_file:
    data=xlrd.open_workbook("./"+file,formatting_info=True)
    table=data.sheets()[0]
    PeerID_List=table.col_values(4)[1:]
    for peerid in PeerID_List:
        all_list.append((file,peerid))
    del data

count={}
for id in all_list:
    if count.get(id[1])==None:
        count[id[1]]=(0,[])
    tmp_num=count[id[1]][0]+1
    tmp=count[id[1]][1][:]
    tmp.append(id[0])
    count[id[1]]=(tmp_num,tmp)
items=list(count.items())
res_list=[]
for item in items:
    if item[1][0]>=2:
        id=item[0]
        table=item[1][1]
        table.sort()
        res_list.append((id,table))
print('重复个数为:'+str(len(res_list)))

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0, 0, 'PeerID')
tables.write(0, 1, 'time')

op=1
for res in res_list:
    tables.write(op,0,res[0])
    tables.write(op,1,' '.join(res[1]))
    op+=1
excel.save('compare.xls')

command="sed -i 's/# swap-endpoint: http:\/\/localhost:8545/swap-endpoint: https:\/\/goerli.infura.io\/v3\/cd8135ee2e07404ab7fd85b862c01f59/' /etc/bee/bee.yaml"

