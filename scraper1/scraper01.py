import httpx # alternative to requests (httpx has async capabilities)
from selectolax.parser import HTMLParser # HTML parser (more modern than beautifulsoup, but is CSS selcetor only)

books_title_and_price = [] # list of dictionaries for saving data

def parser(page):
    print('scraping page number:', page)
    # url to scrape
    url = f'https://books.toscrape.com/catalogue/page-{page}.html' 
    # result of searching 'my user agent' on google
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' }

    # GET request to URL with the headers 
    response = httpx.get(url, headers=headers) #print(response.text)  #.status_code; .text -> HTML
    # HTML parser to create html variable to query for data
    return (HTMLParser(response.text), response.status_code)  # to print the first CSS selector specified:    print(html.css_first('title').text())

def save_info(html):
    # find all elements that match the selector: 
    # select 'ol' element with 'row' class with all 'li' descentend from it
    books = html.css('ol.row li') # <ol class="row"> contains a list <li> of items
    #print('all books:', books) # print the list of books: [<Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>, <Node li>]

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


# main function
def main():
    for page in range(1,4):
        (html, status_code) = parser(page)
        if status_code == 404: # stop pagination
            print(f'page {page} status code: {status_code}')
            break
        save_info(html)
  
    print('all info:', books_title_and_price)


if __name__ == "__main__":
    main()