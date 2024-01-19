import os
import sys
from PIL import Image

class ranker:
    def __init__(self,fileroot) -> None:
        self.fileroot=fileroot
        #进入所有的二级目录，按照文件名排序好的文件，从1开始编号
        #只需要遍历二级目录，如果一级目录中有文件，不用管
        #打印所有二级文件夹,排除不是文件夹的部分
        sub_root=[]
        for i in os.listdir(fileroot):
            if os.path.isdir(fileroot+i):
                sub_root.append(i)
        sub_root.sort(key=lambda x:int(x.split('.')[0]))
        #遍历每一个二级文件夹，将文件名改为编号

        for i in sub_root:
            #进入二级文件夹
            for root,dirs,files in os.walk(fileroot+i):
                if(files[0][0].isalpha()):
                    files.sort()
                else:
                    for x in files:
                        try:
                            y=int(x.split('.')[0])
                        except:
                            files.remove(x)
                    files.sort(key=lambda x:int(x.split('.')[0]))
                #每一个文件的名字改为编号
                total_ids=1
                for i in range(len(files)):
                    #要确保这个文件是.png文件
                    if files[i].split('.')[-1]=='png':
                        os.rename(root+'/'+files[i],root+'/'+str(total_ids)+'.png')
                        total_ids+=1

        #返回一个filenames列表，是所有的“二级目录名/文件名”，当然，文件得是.png文件
        self.filenames=[]
        for i in sub_root:
            for root,dirs,files in os.walk(fileroot+'/'+i):
                for x in files:
                        try:
                            y=int(x.split('.')[0])
                        except:
                            files.remove(x)
                files.sort(key=lambda x:int(x.split('.')[0]))
                for j in files:
                    if j.split('.')[-1]=='png':
                        self.filenames.append(i+'/'+j)
                        Ima=Image.open(fileroot+'/'+i+'/'+j)
                        
        print("ranker "+fileroot+" Done!")
