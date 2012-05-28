from lxml import etree
import re

f = open ('result2.xml', 'r')
xml = f.read ()
f.close ()

root = etree.fromstring (xml)
c = 0

#f = open ('data1_validurl.txt', 'r')
#urls = f.readlines ()
#f.close ()

print '<?xml version="1.0" encoding="ISO-8859-1"?>'
print '<!DOCTYPE dblp SYSTEM "dblp.dtd">'
print "<dblp>"


for article in root.xpath ('*'):
    paper = etree.Element ('paper')
    paper.set ('mdate', article.xpath ('@mdate')[0])
    paper.set ('key', article.xpath ('@key')[0])

    for node in article.xpath ('title'):
        paper.append (node)
    
    for node in article.xpath ('author'):
        paper.append (node)

    for node in article.xpath ('year'):
        paper.append (node)

    for node in article.xpath ('url'):
        paper.append (node)

    for node in article.xpath ('pages'):
        paper.append (node)

    for node in article.xpath ('qtitle'):
        paper.append (node)

    for node in article.xpath ('qauthors'):
        paper.append (node)

    for node in article.xpath ('rtitle'):
        paper.append (node)

    for node in article.xpath ('rauthor'):
        paper.append (node)


    print etree.tostring (paper, pretty_print = True)

print "</dblp>"
