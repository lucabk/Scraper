# alternative to requests (httpx has async capabilities)
import httpx
# HTML parser (more modern than beautifulsoup, but is CSS selcetor only)
from selectolax.parser import HTMLParser

# url to scrape
url = 'https://books.toscrape.com/' 
# result of searching 'my user agent' on google
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' }

# GET request to URL with the headers 
response = httpx.get(url, headers=headers) #print(response.text)  #.status_code; .text -> HTML
# HTML parser to create html variable to query for data
html = HTMLParser(response.text)  # to print the first CSS selector specified:    print(html.css_first('title').text())

# find all elements that match the selector: 
# select 'ol' element with 'row' class with all 'li' descentend from it
books = html.css('ol.row li') # <ol class="row"> contains a list <li> of items
print('all books:', books) # print the list of books: [<Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>]

# list of dictionaries for saving data
books_title_and_price = []

for book in books:
    # book's title: <h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the ...</a></h3>
    a_tag = book.css_first('h3 a')  # find the <h3><a> element
    
    # book's price: <p class="price_color">£51.77</p>
    price_tag = book.css_first('p.price_color')

    if a_tag and price_tag:
        # extract title attribute and price
        title = a_tag.attributes.get('title')
        price = price_tag.text()
        # push to list
        books_title_and_price.append({ 'title':title, 'price':price})
    
print(books_title_and_price)