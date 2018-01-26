from bs4 import BeautifulSoup
import requests
import foocopy as foo
import xlsxwriter


lines = tuple(open("top100.menu", 'r'))
menu_dict = {}
for line in lines:
	menu_item = line.replace("\n","").split(",")
	print menu_item[1]
	r = requests.get(menu_item[1])
	data = r.text
	soup = BeautifulSoup(data, "html.parser")
	link_arr = []
	for link in soup.find_all("a", { "class" : "bl_12" }):
		if not ("javascript" in link['href']):
			link_arr.append("http://www.moneycontrol.com/" + link['href'])
	link_arr.pop(0)
	menu_dict[menu_item[0]] = link_arr

print "extract sentiment"

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('topStocks.xlsx')
for menu in menu_dict:
	worksheet = workbook.add_worksheet(menu)
	# Start from the first cell. Rows and columns are zero indexed.
	worksheet.write(0,0,"STOCK")
	worksheet.write(0,1,"LAST PRICE")
	worksheet.write(0,2,"52 WRK LOW")
	worksheet.write(0,3,"52 WRK HIGH")
	worksheet.write(0,4,"LOW LIMIT ")
	worksheet.write(0,5,"HIGH LIMIT")
	worksheet.write(0,6,"SENTIMENT")
	worksheet.write(0,7,"BUYQT")
	worksheet.write(0,8,"SELLQT")
	worksheet.write(0,9,"SECTOR")
	worksheet.write(0,10, "MARKET CAP (RS CR)")
	worksheet.write(0,11, "P/E")
	worksheet.write(0,12, "BOOK VALUE (RS)")
	worksheet.write(0,13, "DIV (%)")
	worksheet.write(0,14, "MARKET LOT")
	worksheet.write(0,15, "INDUSTRY P/E")
	worksheet.write(0,16, "EPS (TTM)")
	worksheet.write(0,17, "P/C")
	worksheet.write(0,18, "PRICE/BOOK")
	worksheet.write(0,19, "DIV YIELD.(%)")
	worksheet.write(0,20, "FACE VALUE (RS)")
	worksheet.write(0,21, "DELIVERABLES (%)")
	row = 1
	print menu
	for link in menu_dict[menu]:
		try:
			dic_stock_details = foo.get_stock_details(link)
			worksheet.write(row,0, dic_stock_details["stock_name"])
			worksheet.write(row,1, dic_stock_details["last_price"])
			worksheet.write(row,2, dic_stock_details["_52low"])
			worksheet.write(row,3, dic_stock_details["_52high"])
			worksheet.write(row,4, dic_stock_details["low_price_limit"])
			worksheet.write(row,5, dic_stock_details["high_price_limit"]	)
			worksheet.write(row,6, dic_stock_details["sentiment"])
			worksheet.write(row,7, dic_stock_details["buy_qt"])
			worksheet.write(row,8, dic_stock_details["sell_qt"])
			worksheet.write(row,9, dic_stock_details["sector"])
			worksheet.write(row,10, dic_stock_details["MARKET CAP (Rs Cr)"])
			worksheet.write(row,11, dic_stock_details["P/E"])
			worksheet.write(row,12, dic_stock_details["BOOK VALUE (Rs)"])
			worksheet.write(row,13, dic_stock_details["DIV (%)"])
			worksheet.write(row,14, dic_stock_details["Market Lot"])
			worksheet.write(row,15, dic_stock_details["INDUSTRY P/E"])
			worksheet.write(row,16, dic_stock_details["EPS (TTM)"])
			worksheet.write(row,17, dic_stock_details["P/C"])
			worksheet.write(row,18, dic_stock_details["PRICE/BOOK"])
			worksheet.write(row,19, dic_stock_details["DIV YIELD.(%)"])
			worksheet.write(row,20, dic_stock_details["FACE VALUE (Rs)"])
			worksheet.write(row,21, dic_stock_details["DELIVERABLES (%)"])
			row = row + 1
		except:
			print("Error : "+ link)
workbook.close()

