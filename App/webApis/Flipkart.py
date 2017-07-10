from urllib.request import urlopen
import requests
import urllib
import re
from bs4 import BeautifulSoup
class Item:
	pass
class Flipkart:
	def __init__(self):
		pass
	def search(self,query,page=1):
		items = []
		try:
			url = requests.get("https://www.flipkart.com/search?q="+urllib.parse.quote_plus(query)+"&otracker=start&as-show=on&as=off")
			soup = BeautifulSoup(url.text,"lxml")
			products = soup.find_all("div",{"class":"col _2-gKeQ"})
			if len(products)!=0:
				for p in products:
					if(len(p.find_all("div",{"class":"row"}))==0):
						continue
					rl=p.find_all("div",{"class":"row"})[0]
					r=rl.select("div div")[0]
					title=r.get_text()
					price1=p.find_all("div",{"class":"row"})[0].select("div")[6].select("div")[2].get_text()
					price=int(re.sub("[^0-9].*","",re.sub(",","",price1[1:])))
					link="https://www.flipkart.com"+p.find_all("a")[0].get("href")
					item = Item()
					item.title = title
					item.price = price
					item.link=link
					items.append(item)
			else:
				products = soup.find_all("div",{"class":"MP_3W3"})
				#print(len(products))
				for p in products:
					a=p.find_all("a")
					link=a[0].get("href")
					title=a[1].get_text()
					price=0
					if len(re.sub("[^0-9]","",a[2].get_text()))!=0:
						price=int(re.sub("[^0-9].*","",re.sub(",","",a[2].get_text()[1:])))
					item = Item()
					item.title = title
					item.price = price
					item.link=link
					items.append(item)
		except:
			pass
		return items
#f=Flipkart()
#a=f.search("redmi")
#for b in a:
#	print(b.title)