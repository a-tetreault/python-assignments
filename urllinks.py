# The program will use urllib to read the HTML from the data files below,
# extract the href= vaues from the anchor tags, scan for a tag that is in a
# particular position relative to the first name in the list, follow that link
# and repeat the process a number of times and report the last name you find.

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter - ')
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')
# Retrieve all of the anchor tags
tags = soup('a')
names = list()
for tag in tags:
    href = tag.get('href', None)
    if href is not None:
        names.append(href)


link_pos = int(input("Link Position: ")) - 1
iterations = int(input("Repeat how many times?"))
print('Retrieving: ', url)
for i in range(iterations):
    url = names[link_pos]
    print('Retrieving: ', url)
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('a')
    names = []
    for tag in tags:
        href = tag.get('href', None)
        if href is not None:
            names.append(href)
