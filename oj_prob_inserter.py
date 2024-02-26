from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from Foundation import NSData
from AppKit import NSPasteboardTypePNG, NSPasteboardTypeTIFF, NSPasteboard
from pykeyboard import PyKeyboard
from pymouse import PyMouse
import time
from oj_auto_uploader.file_ranker import ranker

class problem_inserter:
    def __init__(self,fileroot,book) -> None:
        self.id_dict=['A']
        self.book=book
        self.fileroot=fileroot
        self.driver=webdriver.Chrome()
        self.driver.implicitly_wait(5)
        with open('total_ids.txt','r') as f:
            self.total_ids=int(f.read())
            
    def add_id(self,id):
        l=len(id)
        i=l-1
        while i>=0 and id[i]=='Z':
            i-=1
        if i<0:
            id='A'*(l+1)
        else:
            id=id[:i]+chr(ord(id[i])+1)+'A'*(l-i-1)
        return id
    
    def paste_image(self,filename,root):
        #将图片放入剪贴板
        pasteboard = NSPasteboard.generalPasteboard()
        file_path=self.fileroot+filename
        image_data = NSData.dataWithContentsOfFile_(file_path)
        format_type = NSPasteboardTypePNG
        pasteboard.clearContents()
        pasteboard.setData_forType_(image_data, format_type)

    def create_contest(self):
        files=self.fileroot
        self.paste_image('cover.png',files)
        driver=self.driver
        windows=driver.window_handles
        driver.switch_to.window(windows[-1])
        time.sleep(0.2)
        driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/ul/li[4]/div').click()
        time.sleep(0.2)
        driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/ul/li[4]/ul/li[2]').click()
        time.sleep(0.2)
        ele=driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/div/div/form/div/div[1]/div/div/div/input')
        ele.send_keys(self.book)
        time.sleep(0.2)
        ele=driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/div/div/form/div/div[2]/div/div/div/div[1]/div[4]')
        ele.send_keys(Keys.COMMAND,'v')
        time.sleep(0.2)
        #定位起始日期
        driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/div/div/form/div/div[3]/div/div/div/input').click()
        time.sleep(0.2)
        today=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        time.sleep(0.2)
        ele=driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[1]/span[1]/div/input')
        ele.send_keys(today.split()[0])
        time.sleep(0.2)
        ele=driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[1]/span[2]/div[1]/input')
        ele.send_keys(today.split()[1])
        time.sleep(0.2)
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/button[2]/span').click()
        time.sleep(0.2)
        #定位结束日期
        driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/div/div/form/div/div[4]/div/div/div/input').click()
        time.sleep(0.2)
        end_day=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()+3600*24*365))
        ele=driver.find_element_by_xpath('/html/body/div[3]/div[1]/div/div[1]/span[1]/div/input')
        ele.send_keys(end_day.split()[0])
        time.sleep(0.2)
        ele=driver.find_element_by_xpath('/html/body/div[3]/div[1]/div/div[1]/span[2]/div[1]/input')
        ele.send_keys(end_day.split()[1])
        time.sleep(0.2)
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/button[2]/span').click()
        time.sleep(0.2)
        #点击保存
        driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/div/div/button/span').click()
        time.sleep(0.2)
        
    def get_into_contest(self):
        driver=self.driver
        windows=driver.window_handles
        driver.switch_to.window(windows[-1])
        time.sleep(0.2)
        driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/ul/li[4]/div').click()
        time.sleep(0.2)
        driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/ul/li[4]/ul/li[1]').click()
        time.sleep(0.2)
        
    def get_filenames(self,start=None,start_id=None):
        tmp=ranker(self.fileroot)
        if start==None:
            for i in range(len(tmp.filenames)-1):
                self.id_dict.append(self.add_id(self.id_dict[-1]))
            return tmp.filenames
        start='/'.join(start.split('__'))+'.png'
        for i in range(len(tmp.filenames)-1):
            self.id_dict.append(self.add_id(self.id_dict[-1]))
        # self.id_dict=[start_id+'A']
        # for i in range(len(tmp.filenames)-tmp.filenames.index(start)):
        #     self.id_dict.append(start_id+self.add_id(self.id_dict[-1][len(start_id):]))
        return tmp.filenames[tmp.filenames.index(start)+1:]
        
    def run(self,start=None,start_id=None,total_ids=None):
        # 进入网站
        url = 'http://127.0.0.1/admin/'
        usrname='root'
        password='20020210xjk'
        testcase='~/Desktop/a.zip'
        driver=self.driver
        driver.get(url)
        driver.maximize_window()
        # 登录 
        ele=driver.find_element_by_xpath('//*[@id="app"]/form/div[1]/div/div/input')
        ele.send_keys(usrname)
        ele1=driver.find_element_by_xpath('//*[@id="app"]/form/div[2]/div/div/input')
        ele1.send_keys(password)
        # 点击Go(切换页面)
        ele2=driver.find_element_by_xpath('//*[@id="app"]/form/div[3]/div/button')
        ele2.click()   
        # 遍历所有的filename，插入进去 
        if start==None:
            self.create_contest()
        else:
            self.get_into_contest()  
            with open('total_ids.txt','w') as f:
                f.write(str(total_ids+1))
        first=1
        where=0
        filenames=self.get_filenames(start,start_id)
        pos=0
        self.id_dict.sort()
        if start!=None:
            where=self.id_dict.index(start_id)+1
        for filename in filenames:
            #复制图片
            self.paste_image(filename,self.fileroot)
            if first:
                first=0
                driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/div[1]/div/div[1]/div[4]/div[2]/table/tbody/tr[1]/td[8]/div/div/div[2]/button').click()
            time.sleep(1.5)
            driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/div[1]/div/div[2]/button[1]/span').click()
            '//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[1]/div[1]/div/div/div[1]/input'

            # 输入题目的id
            time.sleep(1.5)
            ele=driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[1]/div[1]/div/div/div[1]/input')
            time.sleep(0.2)
            ele.send_keys(self.id_dict[pos+where]+(' '*(3-len(self.id_dict[pos+where])))+'('+str(self.total_ids)+')')
            time.sleep(0.2)
            pos+=1
            self.total_ids+=1
            #输入题目的标题
            ele=driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[1]/div[2]/div/div/div[1]/input')
            time.sleep(0.2)
            ele.send_keys('__'.join(filename[:-4].split('/')))
            time.sleep(0.2)
            #点击上传图片，弹出系统选择图片的窗口
            ele=driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[2]/div/div/div/div/div[1]/div[4]')
            time.sleep(0.2)
            ele.send_keys(Keys.COMMAND,'v')
            time.sleep(0.2)

            #输入其他信息
            time.sleep(0.2)
            ele=driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[3]/div[1]/div/div/div/div[1]/div[4]')
            ele.send_keys("None")
            time.sleep(0.2)
            ele=driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[3]/div[2]/div/div/div/div[1]/div[4]')
            ele.send_keys("None")
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[5]/div[3]/div/div/button/span').click()
            time.sleep(0.2)
            ele=driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[5]/div[3]/div/div/div/div[1]/input')
            ele.send_keys('Math\n')
            time.sleep(0.2)
            ele=driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[6]/div/div/div/div/div/div[1]/div/div/div/textarea')
            ele.send_keys('None')
            time.sleep(0.2)
            ele=driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[6]/div/div/div/div/div/div[2]/div/div/div/textarea')
            ele.send_keys('None')
            time.sleep(0.2)

            #提交文件
            ele=driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/div/div/form/div[11]/div[2]/div/div/div/div/button/span').click()

            keyboard=PyKeyboard()
            m=PyMouse()
            time.sleep(1)
            keyboard.press_keys(['Command', 'Shift', 'G'])
            time.sleep(2)
            keyboard.type_string(testcase)
            time.sleep(2)
            keyboard.press_key('Return')
            time.sleep(1)
            keyboard.press_key('Return')
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/div/div/form/button/span').click()
        with open('total_ids.txt','w') as f:
            f.write(str(self.total_ids))
