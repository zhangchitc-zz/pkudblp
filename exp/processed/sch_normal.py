import re, sys


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
tot = 0
known = 0

for line in f.readlines ():
    name = line.split ('\t')[0]
    freq = line.split ('\t')[1].strip ()

    tot = tot + int (freq)
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

    if not ans.startswith ('*'):
        known = known + int (freq)

    print name + '\t\t\t' + ans + '\t\t\t' + freq

sys.stderr.write (str (known * 1.0 / tot) + '\n')
#print sch_table



