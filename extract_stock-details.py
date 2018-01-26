from bs4 import BeautifulSoup
import requests
import sys
from datetime import datetime


def get_stock_details(stock_url):
	dic_stock_details = {}
	r  = requests.get(stock_url)
	data = r.text
	soup = BeautifulSoup(data, "html.parser")

	stock_name = soup.find("h1", {"class":"b_42"}).text.replace(";","")
	dic_stock_details["stock_name"] = stock_name

	last_price = soup.find("span", {"id":"Bse_Prc_tick"}).text
	dic_stock_details["last_price"] = last_price

	_52low = soup.find("span", {"id":"b_52low"}).text
	dic_stock_details["_52low"] = _52low

	_52high = soup.find("span", {"id":"b_52high"}).text
	dic_stock_details["_52high"] = _52high

	low_price_limit = soup.find("span", {"id":"b_low_price_limit"}).text
	dic_stock_details["low_price_limit"] = low_price_limit

	high_price_limit = soup.find("span", {"id":"b_high_price_limit"}).text
	dic_stock_details["high_price_limit"] = high_price_limit


	sentiment = "-"
	for link in soup.find_all("div", { "class" : "senti_gry" }):
		sentiment = link.text.replace('\n', ' ').replace('\r', '')
		if("100%" in sentiment and "BUY" in sentiment):
			sentiment = "BUY"
		elif("100%" in sentiment and "SELL" in sentiment):
			sentiment = "SELL"
		else:
			sentiment = "-"
	dic_stock_details["sentiment"] = sentiment

	buy_qt = soup.find("p", {"id":"b_total_buy_qty"}).text.replace(" K", "")
	dic_stock_details["buy_qt"] = buy_qt

	sell_qt = soup.find("p", {"id":"b_total_sell_qty"}).text.replace(" K", "")
	dic_stock_details["sell_qt"] = sell_qt

	market_details = soup.find("div", {"id":"mktdet_1"})
	tab = market_details.find_all("div", { "class":"FL" ,"style":"width:210px; padding-right:10px"})
	tab_left = tab[0]
	tab_right = tab[1]
	details = tab_left.find_all("div",{"class":"PA7 brdb"})
	for div in details:
		name = div.find("div", {"class":"FL gL_10 UC"}).text
		name = " ".join(name.split())
		val = div.find("div", {"class":"FR gD_12"}).text
		val = " ".join(val.split())
		dic_stock_details[name] = val

	details = tab_right.find_all("div",{"class":"PA7 brdb"})
	for div in details:
		name = div.find("div", {"class":"FL gL_10 UC"}).text
		name = " ".join(name.split())
		if (name == "DELIVERABLES (%)"):
			val = div.find("a", {"class":"bl_12"}).text
		else:
			val = div.find("div", {"class":"FR gD_12"}).text
			val = " ".join(val.split())
		dic_stock_details[name] = val

	sector_div = soup.find("div",{"class":"PB10"})
	sector = sector_div.find("a",{"class":"gry10"}).text
	dic_stock_details["sector"] = sector

	return dic_stock_details


if __name__ == '__main__':
	startTime = datetime.now()
	input_file_name = sys.argv[1]
	output_file_name = sys.argv[2]
	lines = tuple(open(input_file_name, 'r'))
	f = open(output_file_name, "wa")
	f.write("sep=;\n")
	f.write("STOCK;LAST PRICE;52 WRK LOW;52 WRK HIGH;SENTIMENT;BUYQT;SELLQT;SECTOR;MARKET CAP (RS CR);P/E;BOOK VALUE (RS);DIV (%);MARKET LOT;INDUSTRY P/E;EPS (TTM);P/C;PRICE/BOOK;DIV YIELD.(%);FACE VALUE (RS);DELIVERABLES (%)\n")
	for url in lines:
		url = url.replace('\n', ' ').replace('\r', '')
		print(url)
		try:
			dic_stock_details = get_stock_details(url)
			text = ""
			text += dic_stock_details["stock_name"]
			text += ";"
			text += dic_stock_details["last_price"]
			text += ";"
			text += dic_stock_details["_52low"]
			text += ";"
			text += dic_stock_details["_52high"]
			text += ";"			
			text += dic_stock_details["sentiment"]
			text += ";"
			text += dic_stock_details["buy_qt"]
			text += ";"
			text += dic_stock_details["sell_qt"]
			text += ";"
			text += dic_stock_details["sector"]
			text += ";"
			text += dic_stock_details["MARKET CAP (Rs Cr)"]
			text += ";"
			text += dic_stock_details["P/E"]
			text += ";"
			text += dic_stock_details["BOOK VALUE (Rs)"]
			text += ";"
			text += dic_stock_details["DIV (%)"]
			text += ";"
			text += dic_stock_details["Market Lot"]
			text += ";"
			text += dic_stock_details["INDUSTRY P/E"]
			text += ";"
			text += dic_stock_details["EPS (TTM)"]
			text += ";"
			text += dic_stock_details["P/C"]
			text += ";"
			text += dic_stock_details["PRICE/BOOK"]
			text += ";"
			text += dic_stock_details["DIV YIELD.(%)"]
			text += ";"
			text += dic_stock_details["FACE VALUE (Rs)"]
			text += ";"
			text += dic_stock_details["DELIVERABLES (%)"]
			text += "\n"
			f.write(text)
		except:
			print("Error : "+ url)
	print datetime.now() - startTime