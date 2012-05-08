from lxml import etree
import re

f = open ('result1.xml', 'r')
xml = f.read ()
f.close ()

root = etree.fromstring (xml)
c = 0

#f = open ('data1_validurl.txt', 'r')
#urls = f.readlines ()
#f.close ()

print "<dblp>"

for article in root.xpath ('*'):
    if len (article.xpath ('author/text ()')) == 0:
        c = c + 1
        continue
    
    p = re.compile (r'(?P<name>.*)\((?P<uname>.*)\).*\((?P<affn>.*)\)')
    rauthors = article.xpath ('rauthor')
    for rauthor in rauthors:
        m = p.search (rauthor.text)
        if m:
            rauthor.text = m.group ('name') + '(' + m.group ('affn') + ')'
    
    print etree.tostring (article, pretty_print = True)

print "</dblp>"
