import os
from time import sleep

lis=0
if lis==0:
    os.environ['BTFS_PATH'] = '/root/.btfs'
else:
    com='/root/.btfs'+str(lis)
    print(com)
    os.environ['BTFS_PATH'] = com
if lis==0:
    os.environ['PATH'] = '${PATH}:${HOME}/btfs/bin'
else:
    com='${PATH}:${HOME}/btfs'+str(lis)+'/bin'
    print(com)
    os.environ['PATH'] = com
os.environ['http_proxy']='http://honus:honushonus@18.188.199.125:9999'
os.environ['https_proxy']='http://honus:honushonus@18.188.199.125:9999'
if lis==0:
    com='btfs/bin/btfs daemon'
else:
    com='btfs'+str(lis)+'/bin/btfs daemon'
print(com)
os.system(com)
