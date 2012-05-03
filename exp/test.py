from lxml import etree
from scrape import PaperFetcher

f = open ('filtered_dblp.xml', 'r')
s = f.read ()
f.close ()

r = etree.fromstring (s)

count = 0

pf = PaperFetcher ()

for article in r.xpath ('article'):
    count = count + 1

    authors = ' '.join (article.xpath ('author/text()')).encode ('utf-8')
    title = article.xpath ('title/text()')[0].encode ('utf-8')

    print '************************** Test number %d *****************************' % count
    print 'Test query AAAAAAAAAAAAAAAAAAA'
    print 'author = %s' % authors
    print 'title  = %s\n' % title
    print 'Test result from ACM ACM ACM ACM ACM ACM'
    print pf.get_paper_from_acm (title, authors)
    print 'Test result from MS MS MS MS MS MS MS MS'
    print pf.get_paper_from_ms (title, authors)

    if count > 20:
        break


