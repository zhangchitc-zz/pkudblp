from lxml import etree

f = open ('all.xml', 'r')
xml = f.read ()
f.close ()

root = etree.fromstring (xml)
c = 0

f = open ('data1_validurl.txt', 'r')
urls = f.readlines ()
f.close ()

print "<dblp>"

for article in root.xpath ('*'):
    title = article.xpath ('title/text ()')[0]
    if len (article.xpath ('url/text()')) == 0:
        c = c + 1
    else:
        url = article.xpath ('url/text()')[0]
        url = url.split ('#')[0] + '\n'
        if url in urls:
            print etree.tostring (article, pretty_print = True)
  
print "</dblp>"
