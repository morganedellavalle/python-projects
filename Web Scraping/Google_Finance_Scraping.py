# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 17:45:23 2017

@author: modellav
"""

#The goal of this project is to scrape data from Google Finance
#To determine the top gainers and top losers of the market, with corresponding % change

#IMPORT PACKAGES
import urllib.request as ul
from bs4 import BeautifulSoup 
import re
import datetime


#OPEN URL
url = "http://www.google.com/finance"
url_response=ul.urlopen(url,timeout=5)

#CREATE SOUP AND FIND SECTOR TABLE
finance_soup = BeautifulSoup(url_response, "lxml") 
sector_table = finance_soup.find('div', class_ = 'id-secperf sfe-section-major')

#USE REG. EX. TO FIND OUT WHICH SECTOR MOVED THE MOST AND EXTRACT ITS NAME, THE PCT CHANGE AND LINK TO NEXT PAGE
regex_change = re.compile('[+-](.\...)%')
regex_link = re.compile('href=\"(.+)\">')
regex_name = re.compile('>(.+)<')
maxchange = 0

for row in sector_table.find_all('tr'):
    changerow = str(row.find('span', class_='chg'))
    changevalue = regex_change.findall(changerow)
    if changevalue:
        change = float(changevalue[0])
        if change > maxchange:
            maxchange = change
            biggest_mover = regex_name.findall(str(row.a))
            nextpage_link = regex_link.findall(str(row.a))

#OPEN NEXT PAGE (SECTOR URL) AND EXTRACT TOP MOVERS TABLE
url2 = "http://www.google.com" + nextpage_link[0]
url_response2=ul.urlopen(url2,timeout=5)
sector_soup = BeautifulSoup(url_response2, "lxml")

top_movers = sector_soup.find('table', class_ = "topmovers")

#SINCE THEY ARE ORDERED IT IS EASY TO FIND TOP GAINER AND TOP LOSER
mover_rows = top_movers.find_all('tr')
top_gainer = mover_rows[1]
top_loser = mover_rows[7]

#USE REGEX TO FIND TOP GAINER/LOSER NAMES AND CORRESPONDING PCT CHANGE
regex_change2 = re.compile('<span class="chg">\((.+\...%)\)')
regex_change3 = re.compile('<span class="chr">\(\-(.+\...%)\)')

topgainer_name = regex_name.findall(str(top_gainer.a))
toploser_name = regex_name.findall(str(top_loser.a))
topgainer_gain = regex_change2.findall(str(top_gainer))
toploser_loss = regex_change3.findall(str(top_loser))

#find today's date
today = datetime.date.today()

#PRINT FINAL RECAP STATEMENT
print('The sector that has moved the most today, '+ today + " is " + biggest_mover[0] + ' +'+str(maxchange)+'%. '+topgainer_name[0] + ' gained the most ('+topgainer_gain[0]+') while ' + toploser_name[0]+ ', the biggest loser, lost '+ toploser_loss[0]+'.')