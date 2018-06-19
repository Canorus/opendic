 #!/usr/local/bin/python3.6
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import re
import os
import time
import csv

# set current path to basename
#basename = os.getcwd()
# This, unfortunately, didn't work when run by launchctl
# so manually setting path
basename = '/Users/Canor/scripts/opendic'

def getdata(url, t):
    # setting chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(basename+'/chromedriver', chrome_options=options)
    driver.get(url)
    time.sleep(10) # wait 10s for page to fully load
    driver.implicitly_wait(10)
    # select new_words or hot_words
    if t == 'hot':
        param = 'publicity_words'
    elif t == 'new':
        param = 'search_words'
    driver.execute_script('NaverDictUser.showRegisterListByType(\''+param+'\');');
    driver.implicitly_wait(10)
    time.sleep(10)
    html = driver.page_source

    soup = bs(html,'html.parser')

    # pull out ul list
    param_html = str(soup.select('ul#'+param))[1:-1] # remove [ and ] in first and last character from list
    soup = bs(param_html,'html.parser') # parse t.html file with bs and removed whitespaces

    entrys = soup.select('p.usen_entry > span.word_wrap > a') # it's a list, remember
    means = soup.select('p.usen_mean > a')
    uploaders = soup.select('span.usen_from')
    updates = soup.select('span.usen_date')
    url = []
    for i in entrys:
        ibs = bs(str(i),'html.parser')
        url.append(ibs.find('a',attrs={'href':re.compile("^https://")}).get('href')) # url extracted
    def textify(listt):
        for k in range(len(listt)):
            soupi = bs(str(listt[k]),'html.parser')
            listt[k] = soupi.get_text()
    textify(entrys)
    textify(means)
    textify(uploaders)
    textify(updates)
    updata = []
    for l in range(len(entrys)):
        updata.append([])
        updata[-1].append(str(entrys[l]).strip())
        updata[-1].append(str(means[l]).strip())
        updata[-1].append(str(uploaders[l]).strip())
        updata[-1].append(str(updates[l]).strip())
        updata[-1].append(str(url[l]).strip())
    # read from csv
    # count numbers of line in opendic_param.csv file and if line_number is 0 skip the function
    file = open('opendic_'+t+'.csv','r')
    linenum = sum(1 for row in file)
    file.close()
    def addtocsv(d):
        # function to append data to csv
        fi = open('opendic_'+t+'.csv','a')
        wr = csv.writer(fi)
        wr.writerow(d)
        fi.close()
    def comp():
        # function to compare retreived data and previous data
        prev = []
        try:
            csv_read = open('opendic_'+t+'.csv','r')
        except:
            os.system('touch opendic_'+t+'.csv')
            csv_read = open('opendic_'+t+'.csv','r')
        rdr = csv.reader(csv_read)
        for line in rdr:
            prev.append(line) # store previous data to prev list as double list
        csv_read.close()
        # extract head
        prev_head = []
        for i in range(len(prev)):
            prev_head.append(prev[i][0])
        # comparison and append to list
        for i in range(len(updata)):
            if updata[i][0] not in prev_head:
                prev.append(updata[i]) # add updata :double list: to prev :double list: if head of updata element is not in prev_head
                prev_head.append(updata[i][0])
                addtocsv(updata[i])
    if linenum == 0:
        for u in updata:
            addtocsv(u)
    else:
        comp()

getdata('https://open.dict.naver.com/participation/word_list.dict#common/register/zh/ko/','hot')
getdata('https://open.dict.naver.com/participation/word_list.dict#common/register/zh/ko/','new')