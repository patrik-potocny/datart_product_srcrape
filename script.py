from bs4 import BeautifulSoup
import csv
import pandas
import requests
import config

def find_max_page_num(url):
    page_html = requests.get(url)
    soup = BeautifulSoup(page_html.content, 'html.parser')
    pagination = soup.find('div', class_ ='pagination')
    max_page_num = pagination.find_all('a')
    max_page_num = max_page_num[-2].text
    max_page_num = int(max_page_num)

    return max_page_num


def from_lists_to_excel():
    product_info_df = pandas.DataFrame({
        'Name': main_names,
        'Price': main_prices,
        'Link': main_links,
    })

    product_info_df.to_excel('product_info.xlsx')


def from_lists_to_csv():
    product_info_df = pandas.DataFrame({
        'Name': main_names,
        'Price': main_prices,
        'Link': main_links,
    })

    product_info_df.to_csv('product_info.csv')


main_names = []
main_prices = []
main_links = []


main_url = config.main_url

page_html = requests.get(main_url)
soup = BeautifulSoup(page_html.content, 'html.parser')
max_page_num_url = main_url.replace('Page=', 'Page=48')
format_url = max_page_num_url.replace('Pos=0', 'Pos={}')


pos = -48
for num in range(find_max_page_num(max_page_num_url)):
    pos += 48
    final_url = format_url.format(pos)

    page_html = requests.get(final_url)
    soup = BeautifulSoup(page_html.content, 'html.parser')

    product_list = soup.find('div', id="products-list")
    products = product_list.find_all('div', class_ = 'col-item col-ltr count-0')

    names = [product.find('h3').a['title'] for product in products]
    links = ['https://www.datart.sk' + str(product.find('h3').a['href']) for product in products]
    prices = []

    for product in products:
        price_div = product.find('div', class_ = 'price')
        price = price_div.find('span', class_ = 'tooltip').text
        prices.append(price)

    main_names.extend(names)
    main_prices.extend(prices)
    main_links.extend(links)


from_lists_to_excel()
print('Url succsessfully scraped.')
