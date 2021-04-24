# Amazon price tracker

import requests
from bs4 import BeautifulSoup
import smtplib
import time

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:84.0) Gecko/20100101 Firefox/84.0'}

amazon_items = []
notif_prices = []


def send_email(itemLink, min, adress):
    # setting the connection
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('automaticmail05@gmail.com', '')

    # email Content
    subject = 'Price felling down'
    body = 'Hello, The price of the Amazon item ' + itemLink + ' is now less than ' + str(min) + ' euros.' + '\nGo check it out.'

    # sending the email
    email = f'Subject:{subject}\n\n{body}'
    server.sendmail('automaticmail05.gmail.com', adress, email)
    print('Email Sent !')
    server.quit()



def Track_price(itemLink, min, adress):
    page = requests.get(itemLink, headers = headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    price = soup.find(id = 'priceblock_ourprice').get_text()

    price = int(price[:-5])

    if price < min:
        send_email(itemLink, min, adress)

def get_item():
    item = input('Paste the amazon link here :')
    amazon_items.append(item)

def get_min_price():
    min = float(input("What price you want to get notification for ? "))
    notif_prices.append(min)

def get_links():
    add = True
    while add:
        get_item()
        get_min_price()
        choice = input("Do you want to add another item ? [y/n]")
        if choice == 'N' or choice == 'n':
            add = False
    print('The items are registered, you will receive an email if the prices drops down.')



email_adress = input('Type your email adress : ')
get_links()
n = len(amazon_items)
# main loop
while True:
    for i in range(n):
        Track_price(amazon_items[i], notif_prices[i], email_adress)

    time.sleep(1200*12)
