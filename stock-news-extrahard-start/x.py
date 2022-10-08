import xml.etree.ElementTree

def remove_tags(text):
    return ''.join(xml.etree.ElementTree.fromstring(text).itertext())



import re
# as per recommendation from @freylis, compile once only
CLEANR = re.compile('<.*?>')

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

print(cleanhtml('''
<ol><li>Elon Musk responds to Tesla's ESG boot amid calls for a buyback (NASDAQ:TSLA)  Seeking Alpha
</li><li>Why Tesla was kicked out of the S&P 500's ESG index  CNBC
</li><li>Cathie Wood has a simple response to Tesla getting booted out of an S&P 500 ESG …
'''))