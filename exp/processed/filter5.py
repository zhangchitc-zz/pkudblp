import re, sys
from lxml import etree


allowed = {}
f = open ('pages.txt', 'r')
for line in f.readlines ():
    tmp = []
    tokens = line.strip ().split ('\t')
    prefix = len ('http://www.informatik.uni-trier.de/~ley/')
    url = tokens[0][prefix:]
    for i in range (1, len (tokens), 2):
        tmp.append ((int (tokens[i]), int(tokens[i + 1])))
    allowed[url] = tmp

f.close ()


f = open ('result4.xml', 'r')
xml = f.read ()
f.close ()

root = etree.fromstring (xml)

print '<?xml version="1.0" encoding="ISO-8859-1"?>'
print '<!DOCTYPE dblp SYSTEM "dblp.dtd">'
print "<dblp>"

count = 0

out = ''

for paper in root.xpath ('paper'):
    url = paper.xpath ('url/text()')[0]
    url = url.split ('#')[0]
    page = paper.xpath ('pages/text()')
    if page and allowed.has_key (url):
        if page[0].find ('-') == -1:
            count = count + 1
            out = out + etree.tostring (paper) + '\n'
            continue
        if page[0].split('-')[0] and page[0].split ('-')[1]:
            s = int (page[0].split ('-')[0])
            t = int (page[0].split ('-')[1])
            flag = 0
            for span in allowed[url]:
                if span[0] <= s and t <= span[1]:
                    flag = 1
            if flag == 0:
                count = count + 1
                out = out + etree.tostring (paper) + '\n'
                continue

    print etree.tostring (paper, pretty_print = True)

print "</dblp>"

f = open ('filtered_paper.xml', 'w')
f.write ('total %d paper filtered!\n' % count)
f.write (out)
f.close ()
