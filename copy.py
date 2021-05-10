import os

def copy(path):
    command='copy getbalance121.py '+path+'\\getbalance121.py'
    print(command)
    os.system(command)

# files=os.walk()
# for file in files:
#     if os.path.isdir(file):
#         copy(file)

import os
for root, dirs, files in os.walk(".", topdown=False):
    for name in dirs:
        file=os.path.join(root, name)
        copy(file)