from bs4 import BeautifulSoup
import urllib2
import csv
import dbconfig as cfg
origPage = 'http://steamsales.rhekua.com/'
page = urllib2.urlopen(origPage)
file = "C:\\Python27\\demo.html"
import sys
import re 
import MySQLdb as mdb
reload(sys)
sys.setdefaultencoding('UTF8')

def pullGames():
 soup = BeautifulSoup (page, 'html.parser')
 #(page, 'html.parser')

 #Let's pull prices
 names = []
 pricing = []
 discounts = []
 discountPct = []
 #Push items to array for saving
 for name in soup.find_all('div', attrs={'class': 'tab_row'}):
  names.append(name.h4.text)
 for price in soup.find_all('div', attrs={'class': 'discount_original_price'}):
  pricing.append(price.text)
 for discount in soup.find_all('div', attrs={'class': 'discount_final_price'}):
  discounts.append(discount.text)
 for percent in soup.find_all('div', attrs={'class': 'discount_pct'}):
  discountPct.append(percent.text)


 con = mdb.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['passwd'], cfg.mysql['db']);
 cur = con.cursor()
 con.set_character_set('utf8')
 cur.execute('SET NAMES utf8;')
 cur.execute('SET CHARACTER SET utf8;')
 cur.execute('SET character_set_connection=utf8;')


 for i in range(len(names)):
  sql = 'INSERT INTO game_pricing(game_name, original_price, discount_price) \
         VALUES("%s", "%s", "%s")' % \
         (names[i],pricing[i],discounts[i])
 #print sql
  cur.execute(sql)      
  con.commit()

def checkDb():
 con = mdb.connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['passwd'], cfg.mysql['db']);
 cur = con.cursor()
 con.set_character_set('utf8')
 cur.execute('SET NAMES utf8;')
 cur.execute('SET CHARACTER SET utf8;')
 cur.execute('SET character_set_connection=utf8;')
 sql = 'SELECT game_name, original_price, discount_price FROM game_pricing'
 cur.execute(sql)
 results = cur.fetchall()
 for row in results:
  game_name = row[0]
  original_price = row[1]
  discount_price = row[2]
  print "game_name=%s, original_price=%s, discount_price=%s" % \
         (game_name, original_price, discount_price)
#For testing
checkDb()
#sql = "SELECT VERSION()"

##WORKING ----


##
## #Save to CSV
##ofile = open('output2.csv','wb')
##fieldname = ['name', 'discountPrice', 'originalPrice', 'percentOff']
##writer = csv.DictWriter(ofile, fieldnames = fieldname)
##writer.writeheader()
##for i in range(len(names)):
## writer.writerow({'name': names[i], 'discountPrice':pricing[i], 'originalPrice': discounts[i], 'percentOff': discountPct[i].strip('\n\r\t')})
##ofile.close()