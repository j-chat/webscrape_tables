
""" A simple script to webscrape Splunk CIM Reference tables. 

Notes: 
User will be prompted for user and password for proxy. 
If there are multiple tables on the webpage, it will scrape the second table. 

Original code: https://srome.github.io/Parsing-HTML-Tables-in-Python-with-BeautifulSoup-and-pandas/

Args:
	user: user will be prompted to type username
	password: user will be prompted to type password
    proxy_url (str): url of proxy and port number
	datamodel (str): name of the CIM data model (default is Web)
    url (str): url containing the table (default is a link to Splunk's CIM documentation)
	table_num (int): specify the (first, second, etc) table to scrape (default is 1)

Returns:
An .xlsx file of the scraped table
"""

import requests
import getpass
import pandas as pd
from bs4 import BeautifulSoup

# inputs for proxy (optional).
user= getpass.getuser()
password= getpass.getpass()
proxy_url=""
method= 'http'

# inputs for request
datamodel = "Web"
url = "https://docs.splunk.com/Documentation/CIM/4.14.0/User/" + datamodel

proxy = {
'http' : str(method) + '://' + str(user) + ':' + str(password) + '@' + str(proxy_url),
'https' : str(method) + '://' + str(user) + '·' + str(password) + '@' + str(proxy_url)
}

# GET request
response = requests.get(url, proxies=proxy)
print "Connection Established"
# Parse the HTML as a string
soup = BeautifulSoup(response.text, 'lxml' )
# get the second table on the page
table_num = 1
table = soup.find_all('table')[table_num]
print "Grabbed the second table on the page"

# initializations
n_columns = 0
n_rows = 0
column_names = []

# Find number of rows and columns
# we also find the column titles 
print "Get column names"
for row in table.find_all('tr'):
# Determine the number of rows in the table
    td_tags = row.find_all('td')
	if len(td_tags) > 0:
	    n_rows+=l
		if n_columns = 0:
		    # Set the number of colunns for our table
		    n_columns = len(td_tags)
			
	# Handle column names if we find them
    th_tags = row.find_all('th') 
    if len(th_tags) > 0 and len(column_names) == 0:
        for th in th_tags:
            column_names.append(th.get_text())
			
# Safeguard on Column Titles
if len(column_names) > 0 and len(column_names) != n_columns:
    raise Exception("Column titles do not match the number of columns")
	
# making the dataframe
columns = column_names if len(column_names) > 0 else range(0,n_columns)
df = pd.DataFrame(columns = columns, index= range(0,n_rows))
print "Storing Table into a Dataframe"
row_marker = 0
for row in table.find_all('tr'):
    column_marker = 0
    columns = row.find_all('td')
    for column in columns:
        df.iat[row_marker,column_marker] = column.get_text()
        column_marker += 1
        if len(columns) > 0:
            row_marker += 1
	   
# Convert to float if possible
for col in df:
    try:
        df[col] = df[col].astype(float)
    except ValueError:
        pass

# store dataframe to file
print "Dataframe stored to file"
df.to_excel(datamodel + 'Fields.xslx', index=False)  
#df.to_csv(datamodel + 'Fields.xslx', index=False) 
	   