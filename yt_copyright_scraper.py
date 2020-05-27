#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 1 2020
yt_copyright_scraper.py

YouTube content id claims populate information in the video's description.
This script pulls that info from the first song claimed in a YouTube video.
Run this with a list of YouTube urls named "youtube_urls.txt" in the same directory as this script the csv will export

anthony2owaru@gmail.com
"""


import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime
from random import randint
from time import sleep #useage: `sleep(randint(10,100))`

"""STEP 1
this function exports a dictionary where each key has a sequence value of equal lengths """
def dict_to_csv(mdict):
    out_path = str(os.getcwd())+"/"+str(datetime.now())+"_yt_proj_output.csv"
    zd = zip(*mdict.values())
    with open(out_path, 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(mdict.keys())
        writer.writerows(zd)
    print("exported to {}".format(out_path))

"""STEP 2
this needs to be a pipline but for now using a .txt file """

file_path = 'youtube_urls.txt'
with open(file_path) as f:
    youtube_url_list = [line.rstrip() for line in f]


"""STEP 3
Loop through above url pipeline, create a list of soups"""
soup_list=[]
counter=0
#print(youtube_url_list) #for debugging
for url in youtube_url_list:
    soup_list.append(BeautifulSoup(requests.get(url).text, 'html')) #decoupling response as its own variable instead of in one step broke the indexing in the soup_list loop @step4
    counter+=1
    sleep(randint(0,3))
    print(round((counter/len(youtube_url_list))*100,2),"%")

"""
For debugging:
h4_list = soup.findAll('h4',{'class':'title'}).text #this gets the list of header columns from the YT video description
content_items = soup.findAll('ul',{'class':'content watch-info-tag-list'}) #returns a list of soup exports that we can parse again
"""

"""STEP 4
We construct a dict with empty lists as values, Each key should represent a column from h4_list in the above debugging section
Then we loop through the soup list filling in all of the information from each YT vid"""
h4_dict={'Category':[],'Song':[],'Artist':[],'Album':[],'Claimant':[],'URL':[]}

#print(soup.findAll('ul',{'class':'content watch-info-tag-list'})[0].text)
for soup in soup_list:
    if len(soup.findAll('ul',{'class':'content watch-info-tag-list'})) != 5: #this condition ensures there is a copyright claim, solely going off whether there are 5 elements might not stand every situation
        h4_dict['Category'].append(None)
        h4_dict['Song'].append(None)
        h4_dict['Artist'].append(None)
        h4_dict['Album'].append(None)
        h4_dict['Claimant'].append('No Copyright Claim')
        h4_dict['URL'].append(soup.find("meta", property="og:url")) #fix this so it's just the text down the line
    else:
        h4_dict['Category'].append(soup.findAll('ul',{'class':'content watch-info-tag-list'})[0].text)
        h4_dict['Song'].append(soup.findAll('ul',{'class':'content watch-info-tag-list'})[1].text)
        h4_dict['Artist'].append(soup.findAll('ul',{'class':'content watch-info-tag-list'})[2].text)
        h4_dict['Album'].append(soup.findAll('ul',{'class':'content watch-info-tag-list'})[3].text)
        h4_dict['Claimant'].append(soup.findAll('ul',{'class':'content watch-info-tag-list'})[4].text)
        h4_dict['URL'].append(soup.find("meta", property="og:url")) #fix this so it's just the text down the line

"""STEP 5
export the csv
"""
dict_to_csv(h4_dict)
