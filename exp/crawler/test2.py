from lxml import etree
from scrape2 import PaperFetcher

f = open ('filtered_dblp.xml', 'r')
s = f.read ()
f.close ()

r = etree.fromstring (s)

count = 0
start = 29677
end = 30000

pf = PaperFetcher ()

f = open ('out2.xml', 'w')

for article in r.xpath ('*'):
    count = count + 1

    if count < start:
        continue

    authors = ""
    for author in article.xpath ('author/text()'):
        author = author.encode ('utf-8').split (' ')
        authors = authors + ' ' + author[0]

    title = article.xpath ('title/text()')[0].encode ('utf-8')

    print '************************** Test number %d *****************************' % count
    print 'Test query AAAAAAAAAAAAAAAAAAA'
    print 'author = %s' % authors
    print 'title  = %s\n' % title
    print 'Test result from ACM ACM ACM ACM ACM ACM'
    #p = pf.get_paper_from_acm (title, authors)
    #if p:
    #    print p
    #    continue
   
    #print 'Test result from MS MS MS MS MS MS MS MS'
    #p = pf.get_paper_from_ms (title, authors)
    #print p
    #continue
   
    qtitle = etree.Element ('qtitle')
    qtitle.text = title.decode ('iso-8859-1')
    qauthors = etree.Element ('qauthors')
    qauthors.text = authors.decode ('iso-8859-1')
    article.append (qtitle)
    article.append (qauthors)
    
    p = None

    i = 0
    while (i < 3):
        try:
            p = pf.get_paper_from_acm (title, authors)
        except Exception as e:
            p = None
            print e
            print "ACM failed %d time" % i
        else:
            break
        i = i + 1

    i = 0;
    while (i < 3 and not p):
        try:
            p = pf.get_paper_from_ms (title, authors)
        except Exception as e:
            p = None
            print e
            print "MS failed %d time" % i
        else:
            break
        i = i + 1


    if not p:
        continue

    print p
    
    rtitle = etree.Element ('rtitle')
    rtitle.text = p.title
    article.append (rtitle)

    for author in p.authors:
        rauthor = etree.Element ('rauthor')
        s = '%s (%s)' % (author.name, author.affn)
        s = s.encode ('utf-8')
        
        rauthor.text = s.decode ('iso-8859-1')
        article.append (rauthor)

    f.write (etree.tostring (article, pretty_print = True))
    #print etree.tostring (article)
   
    if count >= end:
        break

f.close ()
