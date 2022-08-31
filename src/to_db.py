import os
import csv

def all_illust_db_write():
    #画像読み込み
    dataset_path = "./databases/illust/"
    i=0
    iamge_lsit=[]
    for file in os.listdir(dataset_path):        
        filepath=dataset_path+"/"+file
        if os.path.splitext(os.path.basename(filepath))[1] == "":
            continue
        iamge_lsit.append((os.path.splitext(os.path.basename(filepath))[0],os.path.splitext(os.path.basename(filepath))[1][1:]))

    with open('./databases/illust.csv') as f:
        reader = csv.reader(f)
        l = [row for row in reader]

    for i in iamge_lsit:
        l.append([i[0],"",i[1],"","","","",""])

    output=l
    with open('./databases/illust.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(output)