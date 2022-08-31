import glob
import os
import uuid

path = './databases/illust/*'
i=0
flist = glob.glob(path)
 
# ファイル名を一括で変更する
for file in flist:
    if i!=1:
        print('変更前')
        print(file)
        uuid_txt=uuid.uuid4()
        root_ext_pair = os.path.splitext(file)
        print(root_ext_pair)
        # ('./dir/subdir/filename', '.ext')
        os.rename(file, './databases/illust/' +str(uuid_txt)+root_ext_pair[1])
        print('変更後')
        print('./databases/illust/' +str(uuid_txt)+root_ext_pair[1])
    #i=1

 
list = glob.glob(path)
#print(list)