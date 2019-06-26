
# from selenium import webdriver
# import xlwt
import os
import urllib
import urllib.request

from selenium import webdriver
from bs4 import BeautifulSoup
import time

global nextFlag
url= 'http://jp.qsbdc.com/jpword/index.php'
urlBase='http://jp.qsbdc.com/jpword/'
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
        'Host': 'movie.douban.com'
    }




def getBookID(url,driver):
    driver.get(url)
    time.sleep(10)  # 留出加载时间
    soup = BeautifulSoup(driver.page_source, "html.parser")
    result = soup.find('div', class_=['index_r f_r r_bian']).find_all('a')
    return result

def getLessonList(url,driver):

    result=[]
    lessonName=[]
    driver.get(url)
    loop=1
    while (loop):
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        resultTemp = soup.find_all('a', string='列表学习')
        lessonNameTemp=soup.find_all('strong')
        lessonNameTemp.pop(0)
        result.extend(resultTemp)
        lessonName.extend(lessonNameTemp)

        nextFlag = soup.find_all('span', style='color:grey;')
        print(nextFlag)
        print(len(nextFlag))

        str = ''
        for k in nextFlag:
            str = str + k.get_text()
        if (len(nextFlag)):

            if('下一页' in str):
                loop = 0
                print('none')
                break
            else:
                driver.find_element_by_partial_link_text('下一页').click()
            # for next in nextFlag:
            #     if ('下一页' in next.string):
            #         print('meiyouzhaodao')
            #         loop = 0
            #         break
            # print('下一页可用')
            # driver.find_element_by_partial_link_text('下一页').click()

            # if('下一页' in nextFlag[0].get_text()):
            #     loop = 0
            #     break
            # elif('下一页' in nextFlag[1].get_text()):
            #     loop = 0
            #     break
            # else:
            #     driver.find_element_by_partial_link_text('下一页').click()

        else:
            # print('下一页')
            driver.find_element_by_partial_link_text('下一页').click()

    return result,lessonName

def getLessonWord(url,driver):
    Japanese=[]
    kana=[]
    Chinese=[]
    # driver.get(urlBase + urlLesson + urlPage + str(page))
    loop=1
    driver.get(url)
    while (loop):
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        par = soup.find('div', class_=['index_r f_r r_bian']).find_all('a')  # for test

        JapaneseTemp = soup.find_all('span', class_='hidden_1_1')

        kanaTemp = soup.find_all('span', class_='hidden_2_1')
        ChineseTemp = soup.find_all('span', class_='hidden_3_1')
        Japanese.extend(JapaneseTemp)
        kana.extend(kanaTemp)
        Chinese.extend(ChineseTemp)
        for k in Japanese:
            print(k.string)

        # for p in par:
        #     print(p.string)

        # nextPage=soup.find_all('a',value='下一页')
        # print(nextPage)
        nextFlag = soup.find_all('span', style='color:grey;')  #根据灰色元素提取翻页信息，该信息属性为不可用
        print(nextFlag)
        str=''
        for k in nextFlag:
            str=str+k.get_text()  #翻页信息文本全都提出，
        if (len(nextFlag)):  #判断翻页是否有不可点击元素，有：break 没有：点击下一页

            # print(nextFlag.get_text())
            if ('下一页' in str): #判断下一页是否在不可点击范围，是，break，否，点击翻页
                loop = 0
                print('none')
                break
            else:
                driver.find_element_by_partial_link_text('下一页').click()

        else:
            # print('下一页')
            driver.find_element_by_partial_link_text('下一页').click()
    return Japanese,kana,Chinese


def mkdir(folderName):
    basePath=os.path.abspath(os.path.join(os.getcwd(), ".."))
    fullPath=basePath+'/'+folderName
    # print(fullPath)
    isExists = os.path.exists(basePath+'/' + folderName)
    if not isExists:
        os.makedirs(fullPath)
        print('创建成功')
        return True
    else:
        print('文件夹已存在')
        return False

def saveImg(url,path):
    imgurl = 'https://imgsa.baidu.com/forum/w%3D580/sign=d2876e86afc27d1ea5263bcc2bd4adaf/077f9e2f0708283819880036b399a9014c08f10f.jpg'
    req = urllib.request.Request(url, None)
    response = urllib.request.urlopen(req,timeout=5)

    image = response.read()

    f = open(path+ '.jpg', 'wb')
    f.write(image)
    f.close()

if __name__=="__main__":
    baseUrl='https://manhua.fzdm.com/7/'
    basePath = os.path.abspath(os.path.join(os.getcwd(), ".."))
    # # url='http://jp.qsbdc.com/jpword/word_list.php?lesson_id=401'
    #
    # # bookIDList=[]
    # url='https://manhua.fzdm.com/7/'
    driver = webdriver.Chrome()
    driver.get(baseUrl)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    index=soup.find(id="content").find_all('a')

    index.pop(0)
    index.pop(0)
    index.pop(0)
    index.pop(0)
    index.pop(0)
    index.pop(0)
    index.pop(0)
    index.pop(0)
    index.pop(0)

    # print(index)
    # print(index.find_all('a'))
    # print(index)
    # i.get_text()
    for i in index:
        print(i['href'])
        print(i.get_text())
        driver.get(baseUrl+i['href'])
        fullPath=basePath+'/BLEACH/'+ i.get_text()
        print(fullPath)
        mkdir('/BLEACH/'+ i.get_text())
        loop=1
        i=0
        while(loop):
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # print(i.get_text())
            time.sleep(10)
            result = soup.find(id='mhimg0').find_all('img')
            imgurl = result[0]['src']   #img  url
            print(imgurl)
            saveImg(imgurl,fullPath+'/'+str(i))
            i= i+ 1
            next=soup.find_all(' 最后一页了 ')
            if(len(next)):
                loop=0
                break
            else:
                driver.find_element_by_partial_link_text('下一页').click()

    # driver.get('https://manhua.fzdm.com/7/686/index_4.html')
    # time.sleep(10)
    # soup = BeautifulSoup(driver.page_source, "html.parser")
    #
    # imgurl=soup.find(id='mhimg0').find_all('img')
    # # print(imgurl.find('scr'))
    # print(imgurl[0]['src'])
    # url=imgurl[0]['src']
    driver.quit()



