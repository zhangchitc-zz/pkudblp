from lxml import etree
from scrape import PaperFetcher

f = open ('filtered_dblp.xml', 'r')
s = f.read ()
f.close ()

r = etree.fromstring (s)

count = 0
start = 280

pf = PaperFetcher ()

for article in r.xpath ('article'):
    count = count + 1

    if count < start:
        continue

    authors = ""
    for author in article.xpath ('author/text()'):
        author = author.encode ('utf-8').split (' ')
        authors = authors + ' ' + author[0]
        authors = authors + ' ' + author[-1]

    title = article.xpath ('title/text()')[0].encode ('utf-8')

    print '************************** Test number %d *****************************' % count
    print 'Test query AAAAAAAAAAAAAAAAAAA'
    print 'author = %s' % authors
    print 'title  = %s\n' % title
    print 'Test result from ACM ACM ACM ACM ACM ACM'
    p = pf.get_paper_from_acm (title, authors)
    if p:
        print p
        continue
   
    print 'Test result from MS MS MS MS MS MS MS MS'
    p = pf.get_paper_from_ms (title, authors)
    print p
    continue
   
    qtitle = etree.Element ('qtitle')
    qtitle.text = title
    qauthors = etree.Element ('qauthors')
    qauthors.text = authors
    article.append (qtitle)
    article.append (qauthors)

    p = pf.get_paper_from_acm (title, authors)
    if not p:
        p = pf.get_paper_from_ms (title, authors)

    if not p:
        continue

    rtitle = etree.Element ('rtitle')
    rtitle.text = p.title
    article.append (rtitle)

    for author in p.authors:
        rauthor = etree.Element ('rauthor')
        rauthor.text = str (author)
        article.append (rauthor)

    #print etree.tostring (article)
   
    if count > 0:
        break

print etree.tostring (r)
