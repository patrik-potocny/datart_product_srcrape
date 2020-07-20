from bs4 import BeautifulSoup
import csv
import pandas
import requests

def find_max_page_num(url):
    html = requests.get(url)
    html_soup = BeautifulSoup(html.content, 'html.parser')
    pagination = html_soup.find('div', class_ ='pagination')
    max_page_num = pagination.find_all('a')
    max_page_num = max_page_num[-2].text
    max_page_num = int(max_page_num)

    return max_page_num


def from_lists_to_excel(file_name):
    product_info_df = pandas.DataFrame({
        'Name': main_names,
        'Price': main_prices,
        'Link': main_links,
    })

    product_info_df.to_excel('scrape_results//'+file_name+'.xlsx')


def from_lists_to_csv(file_name):
    product_info_df = pandas.DataFrame({
        'Name': main_names,
        'Price': main_prices,
        'Link': main_links,
    })

    product_info_df.to_csv('scrape_results//'+file_name+'.csv')


def get_user_input():
    global main_url
    global file_format
    global file_name
    print('Go to datart.sk and select any category of products select whatever sorting you want and copy link here.')
    main_url = input('Enter url, make sure it has https:// at start: ')

    answer_is_correct = False
    while answer_is_correct == False:
        print('Do you want to save to: \na) csv\nb) xlsx')
        file_format = input('Choose by typing in a or b : ')
        if file_format == 'a' or file_format == 'b':
            answer_is_correct = True
        else:
            print('CHOOSE option a or b')
    file_name = input('Name of the output file: ')


main_names = []
main_prices = []
main_links = []


get_user_input()


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


if file_format == 'a':
    from_lists_to_csv(file_name)

elif file_format == 'b':
    from_lists_to_excel(file_name)

print('Url succsessfully scraped.Results are in scrape_results folder.')
