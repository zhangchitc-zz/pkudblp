import re, sys
from lxml import etree

def normalize (s):
    s = s.lower ()
    s = s.replace ('univ.', 'university')
    s = s.replace (',', ' ')
    s = s.replace ('.', ' ')
    s = s.replace ('-', ' ')
    s = s.replace ('&', ' ')
    s = s.replace ('of', ' ')
    s = s.replace ('and', ' ')
    s = s.replace ('at', ' ')
    s = s.replace ('the', ' ')
    while (s.find ('  ') != -1):
        s = s.replace ('  ', ' ')
    return s.strip ()

sch_table = []
f = open ('top_schools.txt', 'r')
for line in f.readlines ():
    p = re.compile (r'(?P<name>.*)\((?P<affn>.*)\)')
    m = p.search (line)
    affn = ''
    if m:
        name = m.group ('name')
        affn = m.group ('affn')
    else:
        name = line

    name = name.strip ()
    sch_table.append ((normalize (name), name))
    #print normalize (name), name
    if affn:
        sch_table.append ((normalize (affn), name))
        #print normalize (affn), name

f.close ()

f = open ('affiliations.txt', 'r')

normal = {}

for line in f.readlines ():
    name = line.split ('\t')[0]
    freq = line.split ('\t')[1].strip ()

    norm = normalize (name)
    ans = ' '
    for a, b in sch_table:
        if norm.find (a) != -1:
            if len (a) < 5:
                p = re.compile (r'\b' + a + r'\b')
                if not p.search (norm):
                    continue
            if ans.startswith ('*') or len (b) > len (ans):
                ans = b

    normal[name] = ans


f = open ('result3.xml', 'r')
xml = f.read ()
f.close ()

root = etree.fromstring (xml)

print "<dblp>"

for paper in root.xpath ('paper'):
    p = re.compile (r'(?P<name>.*)\((?P<affn>.*)\)')
    rauthors = paper.xpath ('rauthor')
    for rauthor in rauthors:
        m = p.search (rauthor.text)
        name = m.group ('name') 
        affn = unicode (m.group ('affn')).encode ('latin-1')

        ename = etree.Element("name")
        ename.text = name
        rauthor.text = ''
        rauthor.append (ename)

        ename = etree.Element ("affn")
        ename.text = normal[affn].decode ('latin-1')
        rauthor.append (ename)

        ename = etree.Element ("rawaffn")
        ename.text = m.group ('affn')
        rauthor.append (ename)
 

    print etree.tostring (paper, pretty_print = True)

print "</dblp>"
