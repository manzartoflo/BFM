#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 16:40:19 2019

@author: manzar
"""

import requests
from selenium import webdriver
wb = webdriver.FirefoxProfile()
wb.set_preference("javascript.enabled", True)
driver = webdriver.Firefox(wb)
from bs4 import BeautifulSoup
from urllib.parse import urljoin
alpha = [chr(i) for i in range(97, 97+26)]
hyperLiks = []
for link in alpha:
    url = "http://www.bfm.org.uk/consumers/directory/alphaindex/" + link + '.html'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")
    links = soup.findAll('p', {'class': 'pos-links'})
    for link in links:
        hyperLiks.append(urljoin(url, link.a.attrs['href']))
other_url = "http://www.bfm.org.uk/consumers/directory/alphaindex/other.html"
req = requests.get(other_url)
soup = BeautifulSoup(req.text, "lxml")
links = soup.findAll('p', {'class': 'pos-links'})
for link in links:
    hyperLiks.append(urljoin(url, link.a.attrs['href']))
    
file = open('assignment.csv', 'w')
header = 'Company Name, Telephone, Fax, Email, Website\n'
file.write(header)
    
for link in hyperLiks:
    driver.get(link)
    html = driver.execute_script('return document.documentElement.outerHTML')
    soup = BeautifulSoup(html, "lxml")
    name = soup.findAll('h1', {'class': 'pos-title'})[0].text
    about = soup.findAll('div', {'class': 'pos-contact'})
    li = about[0].findAll('li')
    try:
        tel = li[0].contents[2]
        fax = li[1].contents[2]
        email = li[2].contents[2].a.attrs['href'].split('mailto:')[1]
        web = li[3].contents[2].attrs['href']
    except:
        try:
            tel = li[0].contents[2]
            email = li[1].contents[2].a.attrs['href'].split('mailto:')[1]
            web = li[2].contents[2].attrs['href']
            fax = 'NaN'
        except:
            try:
                tel = li[0].contents[2]
                fax = li[1].contents[2]
                email = 'NaN'
                web = li[2].contents[2].attrs['href']
            except:
                try:
                    tel = li[0].contents[2]
                    fax = 'NaN'
                    email = 'NaN'
                    web = li[1].contents[2].attrs['href']
                except:
                    try:
                        tel = li[0].contents[2]
                        fax = li[1].contents[2]
                        email = li[2].contents[2].a.attrs['href'].split('mailto:')[1]
                        web = 'NaN'
                    except:
                         tel = li[0].contents[2]
                         fax = 'NaN'
                         email = li[1].contents[2].a.attrs['href'].split('mailto:')[1]
                         web = 'NaN'
                         
    tel = str(tel)
    fax = str(fax)
    email = str(email)
    web = str(web)
    print(name, tel, fax, email, web)
    file.write(name.replace(',', '') + ', ' + tel.replace(',', ' | ') + ',' + fax.replace(',', ' | ') + ', ' + email.replace(',', ' | ') + ',' + web.replace(',', ' | ') + '\n')
file.close()
    
    
        