#importing necessary libraries
import requests, csv
from bs4 import BeautifulSoup

# paste the url you want to extract the data
URL = "http://www.values.com/inspirational-quotes"
#Sending the request to the URL to get the response
r = requests.get(URL)
#check the status code of the url. It should be 200
#print(r.status_code)

soup = BeautifulSoup(r.content, 'html5lib')

#create a list to store quotes
quotes = [] 
table = soup.find('div', attrs = {'id' : 'all_quotes'})

for row in table.findAll('div'):
    quote = {}
    quote['theme'] = row.h5.text
    quote['url'] = row.a['href']
    quote['img'] = row.img['src']
    quote['lines'] = row.img['alt'].split("#<")[0]
    quotes.append(quote)
#print(quotes)

filename = 'inspirational_quotes.csv'
with open(filename, 'wb') as f:
    w = csv.DictWriter(f,['theme', 'url', 'img', 'lines'])
    w.writeheader()
    for quote in quotes:
        w.writerow(quote)
