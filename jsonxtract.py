#  read the JSON data from that URL using urllib and then parse and extract the comment counts from the JSON data, compute the sum of the numbers in the file and enter the sum below

import urllib.request, urllib.parse, urllib.error
import json, ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Import JSON from URL
url = input('Enter location: ')
print('Retrieving ', url)
uh = urllib.request.urlopen(url)
data = uh.read()
print('Retrieved',len(data),'characters')

js = json.loads(data)
comments = js.get("comments") # Go in one level
count = []
for person in comments:
    #create list for each k,v pair
    count.append(person.get("count"))

print('Count: ', len(count))
print('Sum: ', sum(count))
