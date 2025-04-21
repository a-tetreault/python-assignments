import urllib.request
import xml.etree.ElementTree as ET
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter location: ')
print('Retrieving ', url)
uh = urllib.request.urlopen(url)
data = uh.read()
print('Retrieved',len(data),'characters')

xml = ET.fromstring(data)
counts = xml.findall('.//count')
print('Count:', len(counts))
nums = list()
for result in counts:
    nums.append(int(result.text))
print('Sum:', sum(nums))
