from requests import get
from lxml.html import fromstring
import csv

def crawl_gintarine():

    response = get ("https://www.gintarine.lt/asmens-higiena-3")
    response.raise_for_status ()

    tree = fromstring (response.content)

    products = tree.xpath ("//div[contains(@class, 'product-item')]")

    result = []
    for product in products:
        title = product.xpath (".//input[@name='productName']/@value")
        price = product.xpath (".//input[@name='productPrice']/@value")

        if title and price:
            result.append ({
                "title": title[0].strip (),
                "price": price[0].strip ()
            })
    return result

def save_as_csv(data, filename="output.csv"):

    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    return filename

if __name__ == "__main__":
    products = crawl_gintarine ()
    csv_file = save_as_csv (products)
    print (f"Produktai išsaugoti faile: {csv_file}")