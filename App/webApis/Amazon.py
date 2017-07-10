import urllib
import requests
import re
import sys
from bs4 import BeautifulSoup
class Item:
	pass
class Amazon:
	def __init__(self):
		pass
	def search(self,query,page=1):
		items = []
		start = 1 + ( (page-1) * 24)
		try:
			url = "https://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Delectronics&field-keywords="+urllib.parse.quote_plus(query)
#			print(url)
			response = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
			soup = BeautifulSoup(response.content,"lxml")
			title=""
			img=""
			for h in soup.select('li.celwidget'):
				for t in h.select('h2.s-access-title'):
					title=t.get_text()
				link=h.select('a')[0].get("href")
				if link[0]=='/':
					link=h.select('a')[1].get("href")
				il=h.find_all("img",{"class":"s-access-image"})
				img=il[0].get("src")
				list=h.find_all("span",{"class":"a-color-price"})
				price=int(re.sub("\..*","",re.sub(",", "",list[0].get_text())))
				item = Item()
				item.title = title
				item.img=img
				item.price = price
				item.link=link
				items.append(item)
		except:
			pass
#			print("Unexpected error:", sys.exc_info()[0])
		return items
"""a=Amazon()
g=a.search("redmi")
bi=0
for f in g:
	print(str(f.title)+" "+str(f.price))
	if f.price>bi:
		bi=f.price
print(bi)"""