from urllib.request import urlopen
import requests
import urllib
import sys
from bs4 import BeautifulSoup
class Item:
	pass
class Croma:
	def __init__(self):
		pass
	def search(self,query,page=1):
		items = []
		try:
			url = requests.get("https://www.croma.com/search?q="+urllib.parse.quote_plus(query)+"%3Arelevance%3AskuStockFlag%3Atrue&show=All")
			#url = requests.get("https://www.croma.com/search/?text="+urllib.parse.quote_plus(query))
			soup = BeautifulSoup(url.text,"lxml")
			products = soup.find_all("div",{"class":"gBox"})
			for product in products:
				p=product.find_all("div",{"class":"thumb"})[0];
				title = p.find_all("h2")[0].find_all("a")[0].get("title")
				price=p.find_all("h3")[0].get_text()
				img=p.find_all("a",{"class":"productMainLink"})[0].find_all("img")[0].get("src")
				link=p.find_all("a",{"class":"productMainLink"})[0].get("href")
				item = Item()
				item.title = title
				item.price = price
				item.img=img
				item.link=link
				items.append(item)
		except:
#			print("Unexpected error:", sys.exc_info()[0])
			pass
		return items
"""a=Croma()
g=a.search("nokia")
for f in g:
	print(str(f.title)+" "+str(f.price))"""