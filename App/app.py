from flask import Flask, render_template,request,redirect, url_for
from webApis import Croma,Amazon,Flipkart
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse,parse_qsl
app = Flask(__name__)
class witem:
	def __init__(self):
		self.price=0
		self.title=""
		self.link=""
		self.img=""
		self.alink=""

class Product:
	def __init__(self):
		self.amazonItem=witem()
		self.cromaItem=witem()
		self.flipkartItem=witem()

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/view/<link>/<source>')
def view(link,source):
	if source=="c":
		link=re.sub('@','/',link)
		link="https://www.croma.com/"+link
		#return(link)
		response = requests.get(link, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
		soup = BeautifulSoup(response.text,"lxml")
		name=soup.find_all("div",{"class":"productDescriptionCss"})[0].get_text()
		contents=soup.find_all("div",{"class": "pContentTab"})
		tech=contents[2]
		td=tech.find_all("td")
		data={}
		i=0
		while i<len(td):
			data[td[i].get_text()]=td[i+1].get_text()
			i=i+2
		hyp=soup.find_all("div",{"class":"productImage"})[0].find_all("img")[0]
		img="https://www.croma.com"+hyp.get("src")
		price=0
		for r in soup.select("div.cta table tbody tr td h2"):
			price=int(re.sub("[^0-9]","",r.get_text()))
#		print(soup.prettify())
		#soup = BeautifulSoup(response.content,"lxml")
		return(render_template("view.html",name=name,data=data,link=link,imag=img,price=price))
	elif source=="a":
		data={}
		img=""
		prce=0
		name=""
		link=re.sub('@','/',link)
		link=re.sub("\$","?",link)
		link=link.replace("http://www.amazon.in/","")
		link=link.replace("https://www.amazon.in/","")
		link="http://www.amazon.in/"+link
		query_dict=dict(parse_qsl(urlparse(link)[4]))
		c=0
		p=0
		while(c<6):
			if link[p]=='/':
				c=c+1
			if c==6:
				break
			p=p+1
		link=link[:p]+"?_encoding="+query_dict['ie']+"&keywords="+query_dict['keywords']+"&qid="+query_dict['qid']+"&ref_=sr_"+(re.sub('-','_',query_dict['sr']))+"&s="+query_dict['s']+"&sr="+query_dict['sr']
		#return link
		response = requests.get(link, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
		return(render_template("view.html",name=name,data=data,link=link,imag=img,price=price))
		#return response.content
	elif source=="f":
		data={}
		link=re.sub('@','/',link)
		link=re.sub("\$","?",link)
		link=link.replace("https://www.flipkart.com","")
		link="https://www.flipkart.com"+link
		#return(link)
		response = requests.get(link, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
		soup=BeautifulSoup(response.text,"lxml")
		h1=soup.find_all("h1",{"class":"_3eAQiD"})[0]
		name=h1.get_text()
		divtext=soup.find_all("div",{"class":"_1vC4OE _37U4_g"})[0].get_text()
		price=int(re.sub("[^0-9]","",divtext))
		img=soup.find_all("img",{"class":"sfescn"})[0]
		imag=img.get("src")
		lis=soup.find_all("div",{"class":"_2MCvv7"})[0].find_all("li")
		i=0
		while i<len(lis):
			key=lis[i].get_text()
			value=lis[i+1].get_text()
			key=key.replace(value,"")
			data[key]=value
			i=i+2
		return(render_template("view.html",name=name,data=data,link=link,imag=imag,price=price))
#	return "View "+link

@app.route('/find', methods = ['POST', 'GET'])
def find():
	try:
#	if True:
		if request.method == 'POST':
			mob = request.form['item']
			if mob=="":
				return redirect(url_for('index'))
			c = Croma.Croma()
			cr = c.search(mob)
			a = Amazon.Amazon()
			ar = a.search(mob)
			ar= ar[:len(ar)-3]
			f=Flipkart.Flipkart()
			fr=f.search(mob)
			fr= fr[:len(fr)-1]
			products=[]
			for i in cr:
				product=Product()
				product.cromaItem.price=i.price
				product.cromaItem.title=i.title
				product.cromaItem.img="https://www.croma.com"+i.img
				product.cromaItem.link="https://www.croma.com"+i.link
				product.cromaItem.alink=re.sub("/", "@", product.cromaItem.link[22:])
				products.append(product)
			for i in ar:
				flag=0
				for j in products:
					if j.cromaItem.title==i.title:
						j.amazonItem.title=i.title
						j.amazonItem.price=i.price
						j.amazonItem.img=i.img
						j.amazonItem.link=i.link
						j.amazonItem.alink=re.sub("/", "@", j.amazonItem.link[22:])
						j.amazonItem.alink=re.sub("\?","$",j.amazonItem.alink)
						flag=1
						break
				if flag==0:
					product=Product()
					product.amazonItem.price=i.price
					product.amazonItem.title=i.title
					product.amazonItem.img=i.img
					product.amazonItem.link=i.link
					product.amazonItem.alink=re.sub("/", "@", product.amazonItem.link[22:])
					product.amazonItem.alink=re.sub("\?","$",product.amazonItem.alink)
					products.append(product)
			for i in fr:
				flag=0
				for j in products:
					if j.cromaItem.title==i.title or j.amazonItem.title==i.title:
						j.flipkartItem.title=i.title
						j.flipkartItemItem.price=i.price
						j.flipkartItem.link=i.link
						j.flipkartItem.alink=re.sub("/", "@", j.flipkartItem.link)
						j.flipkartItem.alink=re.sub("\?","$",j.flipkartItem.alink)
						flag=1
						break
				if flag==0:
					product=Product()
					product.flipkartItem.price=i.price
					product.flipkartItem.title=i.title
					#product.flipkartItem.img=i.img
					product.flipkartItem.link=i.link
					j.flipkartItem.alink=re.sub("/", "@", j.flipkartItem.link)
					j.flipkartItem.alink=re.sub("\?","$",j.flipkartItem.alink)
					products.append(product)
			return render_template("results.html",query=mob,products=products)
#			,amazon=ar,croma=cr,query=mob)
		else:
			return render_template("results.html")
#	else:
#		pass
	except:
		return(render_template("results.html"))

if __name__ == '__main__':
   app.run(debug = True)