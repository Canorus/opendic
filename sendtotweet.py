#!/usr/local/bin/python3.6
import csv
from twitter import *
import random
import os

# base = os.getcwd()
# this os.getcwd method didn't work when run by launchctl
# manually setting path
base = '/Users/Canor/scripts/opendic'
print(base)
h = open(base+'/opendic_hot.csv','r')
n = open(base+'/opendic_new.csv', 'r')
rdrh = csv.reader(h)
rdrn = csv.reader(n)

words = []

for line in rdrh:
    words.append(line)
for line in rdrn:
    words.append(line)

word = words[random.randrange(len(words))] # is list

#print(word)

keyw = word[0]
meaning = word[1]
uploader = word[2]
update = word[3]
url = word[4]
print('keyword: '+keyw)
print('meaning: '+meaning)
print('uploader: '+uploader)
print('update: '+update)
print('url: '+url)

t = Twitter(auth=OAuth('your_token_here','your_token_secret_here','your_consumer_key_here','your_consumer_secret_here'))
t.statuses.update(status='키워드: '+keyw+'\n의미: '+meaning+'\n업로더: '+uploader+'\n업로드일: '+update+'\n링크: '+url+'\n#오늘의_듕귁어_자동봇', in_reply_to_status_id=1009005619175518208)
