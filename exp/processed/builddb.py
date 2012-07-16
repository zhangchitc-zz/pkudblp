# -*- coding: utf_8 -*-
from lxml import etree
import cStringIO
import sqlite3
import sys

con = sqlite3.connect ('test.db')
authorid = {}

def getaffnid (affn):
    affn = affn.strip ()

    cur = con.cursor ()
    cur.execute ("SELECT * FROM Affiliations WHERE title = ?", [affn])
    row = cur.fetchone ()

    return row[0]


def getauthorid (name, affn):
    name = name.strip ()
    affn = affn.strip ()
    
    if authorid.has_key ((name, affn)):
        return authorid[(name, affn)]

    affnid = getaffnid (affn)

    cur = con.cursor ()
    cur.execute ("INSERT INTO Authors (name, affnid) VALUES (?, ?)", (name, affnid))
    authorid[(name, affn)] = cur.lastrowid
    return cur.lastrowid


def fromLatinToUnicode (s):
    vf = cStringIO.StringIO ()
    vf.write (s.encode ('latin-1'))
    return vf.getvalue ().decode ('utf-8')
 

with con:

    cur = con.cursor ()
    cur.execute ('DROP TABLE IF EXISTS Papers')
    cur.execute ('''CREATE TABLE Papers (
        pid     INTEGER PRIMARY KEY AUTOINCREMENT,
        title   TEXT, 
        key     TEXT, 
        year    INTEGER, 
        url     TEXT
        )''')

    cur.execute ('DROP TABLE IF EXISTS Affiliations')
    cur.execute ('''CREATE TABLE Affiliations (
        sid     INTEGER PRIMARY KEY AUTOINCREMENT,
        title   TEXT,
        type    TEXT
        )''')

    cur.execute ('DROP TABLE IF EXISTS Authors')
    cur.execute ('''CREATE TABLE Authors (
        aid     INTEGER PRIMARY KEY AUTOINCREMENT,
        name    TEXT, 
        affnid  INTEGER,
        FOREIGN KEY (affnid) REFERENCES Affiliations (sid)
        )''')

    cur.execute ('DROP TABLE IF EXISTS Copyrights')
    cur.execute ('''CREATE TABLE Copyrights (
        pid     INTEGER,
        pubtype INTEGER,
        pubid   INTEGER,
        aid     INTEGER,
        rank    INTEGER,
        score   REAL, 
        FOREIGN KEY (pid) REFERENCES Papers (pid),
        FOREIGN KEY (aid) REFERENCES Authors (aid)
        )''')
    
    cur.execute ('DROP TABLE IF EXISTS Conferences')
    cur.execute ('''CREATE TABLE Conferences (
        cid     INTEGER PRIMARY KEY AUTOINCREMENT,
        abbr    TEXT,
        area    INTEGER,
        title   TEXT
        )''')

    cur.execute ('DROP TABLE IF EXISTS Journals')
    cur.execute ('''CREATE TABLE Journals (
        jid     INTEGER PRIMARY KEY AUTOINCREMENT,
        abbr    TEXT,
        area    INTEGER,
        title   TEXT
        )''')

    f = open ('data_conf.txt', 'r')
    for line in f.readlines ():
        abbr = line.split ('\t')[0].strip ()
        area = line.split ('\t')[2].strip ()
        area = int (area)
        title = line.split ('\t')[3].strip ()
        cur.execute ("INSERT INTO Conferences (abbr, area, title) VALUES(?, ?, ?)", (abbr, area, title))
    f.close ()


    f = open ('data_journal.txt', 'r')
    for line in f.readlines ():
        abbr = line.split ('\t')[0].strip ()
        area = line.split ('\t')[2].strip ()
        area = int (area)
        title = line.split ('\t')[3].strip ()
        cur.execute ("INSERT INTO Journals (abbr, area, title) VALUES(?, ?, ?)", (abbr, area, title))
    f.close ()


    # Add a empty affiliation
    cur.execute ("INSERT INTO Affiliations (title, type) VALUES ('', '')")

    # Add affliation record
    f = open ('data_affiliations.txt', 'r')
    for line in f.readlines ():
        #line = line.decode ('utf-8')
        name = line.split ('\t')[0].strip ()
        Type = line.split ('\t')[1].strip ()
        if name.find ('(') != -1:
            name = name[:name.find ('(')].strip ()

        name = name.decode ('utf-8')
        Type = Type.decode ('utf-8')
        cur.execute ("INSERT INTO Affiliations (title, type) VALUES(?, ?)", (name, Type))
    f.close ()
    
    

    # Add Papers record
    f = open ('result5.xml', 'r')
    r = etree.fromstring (f.read ())
    for paper in r.xpath ('paper'):
        title = paper.xpath ('title/text()')[0]
        year = paper.xpath ('year/text()')[0]
        key = paper.xpath ('@key')[0]
        url = paper.xpath ('url/text()')[0]

        year = int (year)

        cur.execute ("INSERT INTO Papers (title, key, year, url) VALUES(?, ?, ?, ?)", (title, key, year, url))
        pid = cur.lastrowid

        if url.split ('/')[1] == 'conf':
            pubtype = 1
            cur.execute ("SELECT * FROM Conferences WHERE abbr = ?", [url.split ('/')[2]])
            pubid = cur.fetchone ()[0]
        else:
            pubtype = 2
            cur.execute ("SELECT * FROM Journals WHERE abbr = ?", [url.split ('/')[2]])
            pubid = cur.fetchone ()[0]

        rank = 0
        tot = len (paper.xpath ('rauthor'))
        total = 0
        for i in range (1, tot + 1):
            total = total + 1.0 / i

        for author in paper.xpath ('rauthor'):
            if not author.xpath ('name')[0].text:
                print 'fuck'
                continue
            name = fromLatinToUnicode (author.xpath ('name')[0].text)
            affn = fromLatinToUnicode (author.xpath ('affn')[0].text)

            aid = getauthorid (name, affn)   
            rank = rank + 1
            cur.execute ("INSERT INTO Copyrights (pid, pubtype, pubid, aid, rank, score) VALUES (?, ?, ?, ?, ?, ?)", \
                (pid, pubtype, pubid, aid, rank, 1.0 / rank / total))


