import csv
import urllib2
from django.template.defaultfilters import safe
from django.utils.encoding import smart_str
import json
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def getting_Hotel_Links():
    final_Array = []
    for i in range(16):
        urlString = 'https://www.visitberlin.de/en/hotels-in-berlin/hotel-guide?keys=&cat=All&stars=All&page=' + smart_str(
            i)
        html_page = urllib2.urlopen(urlString)
        soup = BeautifulSoup(html_page)
        for ul in soup.findAll('ul', {'class': 'l-list'}):
            for li in ul.findAll('li', {'class': 'l-list__item'}):
                for article in li.findAll('article'):
                    for div in article.findAll('div', {'class': 'teaser-search__content'}):
                        for innerDiv in div.findAll('div', {'class': 'teaser-search__booking-header'}):
                            for header in innerDiv.findAll('h3'):
                                for link in header.findAll('a'):
                                    temp = []
                                    print smart_str(link.text)
                                    # print smart_str('https://www.visitberlin.de'+link.get('href'))
                                    temp.append(smart_str(link.text))
                                    temp.append(smart_str('https://www.visitberlin.de' + link.get('href')))
                                final_Array.append(temp)
        return final_Array


def getting_Further_Details(final_Array):
    final_Details = []
    for i in final_Array:
        urlString = i[1]
        print urlString
        html_page = urllib2.urlopen(urlString)
        soup = BeautifulSoup(html_page)
        for div in soup.findAll('div', {'class': 'map-single__address'}):
            for inner_Div in div.findAll('div', {'class': 'address'}):
                temp = []
                temp.append(i[0])
                for p in inner_Div.findAll('p'):
                    dump = []
                    for span in p.findAll('span'):
                        dump.append(smart_str(span.text).replace('\n', '').replace('  ', ''))
                    if len(dump) == 5:
                        # temp.append(','.join(dump))
                        temp.append(smart_str(dump[0]) + smart_str(dump[1]))
                        temp.append(smart_str(dump[3]))
                        temp.append(smart_str(dump[4]))
                        temp.append(smart_str(dump[2]))
                    elif len(dump) == 2:
                        email = smart_str(dump[1])
                        phone = smart_str(dump[0])
                        email = email.replace('E-Mail: ', '')
                        phone = phone.replace('Tel.: ', '')
                        temp.append(phone[5:])
                        temp.append(email[7:])
                    elif len(dump) == 1:
                        if len(dump[0]) != 0:
                            print i
                            phone = smart_str(dump[0]).replace('Tel.: ', '')
                            temp.append(phone[5:])
                final_Details.append(temp)
    return final_Details


final_Array = getting_Hotel_Links()
final_Details = getting_Further_Details(final_Array)

for i in final_Details:
    print i
print len(final_Details)

outfile = open('Hotels_Data_Sample.csv', 'w')
writer = csv.writer(outfile)
writer.writerow(['Hotel_Name', 'Street', 'City', 'Country', 'Zip_Code', 'Phone_Number', 'Email'])
for row in final_Details:
    writer.writerow(row)
outfile.close()
