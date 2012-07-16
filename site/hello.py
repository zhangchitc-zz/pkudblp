from bottle import static_file, post, route, run, template, request
import sqlite3

@route('/js/:filename')
def getfile (filename):
    return static_file (filename, root='js')

@route('/img/:filename')
def getfile (filename):
    return static_file (filename, root='img')

@route('/css/:filename')
def getfile (filename):
    return static_file (filename, root='css')


@route('/')
def index():
   con = sqlite3.connect ('pkudblp.db')

   with con:
        cur = con.cursor ()

        htmlrows = {}
        for area in range (1, 9):
            htmlrows[area] = ''

        cur.execute ("SELECT * FROM Conferences")
        rows = cur.fetchall ()

        for row in rows:
            area = row[2]
            htmlrows[area] = htmlrows[area] + template ('tpl/index3', lowtype = "conf", type='Conference', typecolor='success', name = str (row[2]) + row[1], id= row[0], desc = row[3], capname = row[1].upper ())
 
        cur.execute ("SELECT * FROM Journals")
        rows = cur.fetchall ()

        for row in rows:
            area = row[2]
            htmlrows[area] = htmlrows[area] + template ('tpl/index3', lowtype = "journal", type='Journal', typecolor='error', name = str (row[2]) + row[1], id= row[0], desc = row[3], capname = row[1].upper ())
 
 
        tabs = ''
        for area in range (1, 9):
            if area == 1:
                tabs = tabs + template ('tpl/index2', active = "active", area=area, htmlrows = htmlrows[area])
            else:
                tabs = tabs + template ('tpl/index2', active = "", area=area, htmlrows = htmlrows[area])

        return template ('tpl/index1', tabs = tabs)


@post('/select')
def select ():
   con = sqlite3.connect ('pkudblp.db')

   with con:
        cur = con.cursor ()

        conf = request.forms.getlist ('conf')
        journal = request.forms.getlist ('journal')

        hiddata = ''
        for c in conf:
            hiddata = hiddata + '<input type="hidden" name="conf" value="%s">\n' % c
        for j in journal:
            hiddata = hiddata + '<input type="hidden" name="journal" value="%s">\n' % j

        cur.execute ("SELECT * FROM Affiliations ORDER BY Title")
        rows = cur.fetchall ()

        affops = ''
        for row in rows:
            affops = affops + '<option value="%d">%s</option>\n' % (row[0], row[1])

        return template ('tpl/select1', hiddata = hiddata, affops = affops)


@post ('/rank')
def index ():
    conf = request.forms.getlist ('conf')
    journal = request.forms.getlist ('journal')
  
    con = sqlite3.connect ('pkudblp.db')

    with con:
        cur = con.cursor ()

        query = """
        select 
            Authors.affnid      AS affnid, 
            Affiliations.title  AS title, 
            SUM (CASE WHEN Copyrights.pubtype = 1 THEN Copyrights.score ELSE 0 END) AS conf_paper,
            SUM (CASE WHEN Copyrights.pubtype = 2 THEN Copyrights.score ELSE 0 END) AS journal_paper,
            SUM (Copyrights.score) AS paper

        FROM Copyrights 
        INNER JOIN Authors on Copyrights.aid = Authors.aid 
        INNER JOIN Affiliations on Affiliations.sid = Authors.affnid
        WHERE 1 = 0 """

        for c in conf:
            query = query + " OR (Copyrights.pubtype = 1 AND Copyrights.pubid = " + c + ")"

        for j in journal:
            query = query + " OR (Copyrights.pubtype = 2 AND Copyrights.pubid = " + j + ")"

        query = query + " GROUP BY Authors.affnid ORDER BY paper DESC"

        cur.execute (query)

        ret = template ("tpl/rank1")
        
        rows = cur.fetchall ()
        rank = 1
        for row in rows:
            if row[0] == 1:
                continue

            if rank % 2 == 1:
                ret = ret + template ("tpl/rank2", rank=rank, affn=row[1], total="%.2f" % row[4], conf="%.2f" % row[2], journal="%.2f" % row[3])
            else:
                ret = ret + template ("tpl/rank3", rank=rank, affn=row[1], total="%.2f" % row[4], conf="%.2f" % row[2], journal="%.2f" % row[3])
 
            rank = rank + 1

        ret = ret + template ("tpl/rank4")

        return ret


@post ('/trend')
def index ():
    conf = request.forms.getlist ('conf')
    journal = request.forms.getlist ('journal')
    sid = request.forms.get ('sid')
   
    con = sqlite3.connect ('pkudblp.db')

    with con:
        cur = con.cursor ()
        ret = template ("tpl/trend1")

        cur.execute ("SELECT * FROM Affiliations WHERE sid = ?", [sid])
        ret = ret + """<input type="hidden" id="univ1" value=" """ + cur.fetchone ()[1] + """ "/>"""

        query = """
        select 
            Authors.affnid      AS affnid, 
            Affiliations.title  AS title, 
            Papers.year         AS year, 
            SUM (CASE WHEN Copyrights.pubtype = 1 THEN Copyrights.score ELSE 0 END) AS conf_paper,
            SUM (CASE WHEN Copyrights.pubtype = 2 THEN Copyrights.score ELSE 0 END) AS journal_paper,
            SUM (Copyrights.score) AS paper

        FROM Copyrights 
        INNER JOIN Authors on Copyrights.aid = Authors.aid 
        INNER JOIN Affiliations on Affiliations.sid = Authors.affnid
        INNER JOIN Papers on Papers.pid = Copyrights.pid
        WHERE Affiliations.sid = """ + sid + ' AND (1 = 0 '

        for c in conf:
            query = query + " OR (Copyrights.pubtype = 1 AND Copyrights.pubid = " + c + ")"

        for j in journal:
            query = query + " OR (Copyrights.pubtype = 2 AND Copyrights.pubid = " + j + ")"

        query = query + ") GROUP BY Authors.affnid, Papers.year ORDER BY paper DESC"

        cur.execute (query)
 
        rows = cur.fetchall ()
        for row in rows:
	        ret = ret + '<input type="hidden" id="data_1_' + str (row[2]) + '" conf="' + str (row[3]) + '" journal="' + str (row[4]) + '" total="' + str(row[5]) + '"/>'

        ret = ret + template ("tpl/trend2")

        return ret


@post ('/compare')
def index ():
    conf = request.forms.getlist ('conf')
    journal = request.forms.getlist ('journal')
    sid = request.forms.get ('sid')
    sid2 = request.forms.get ('sid2')

    con = sqlite3.connect ('pkudblp.db')

    with con:
        cur = con.cursor ()
        ret = template ("tpl/compare1")
        
        cur.execute ("SELECT * FROM Affiliations WHERE sid = ?", [sid])
        name1 = cur.fetchone ()[1]
        cur.execute ("SELECT * FROM Affiliations WHERE sid = ?", [sid2])
        name2 = cur.fetchone ()[1]


        ret = ret + """<h2> Comparison between %s and %s </h2>
	<div id="chart"></div> 
        </div>
        <input type="hidden" id="univ1" value="%s"/>
	    <input type="hidden" id="univ2" value="%s"/>
	
        """ % (name1, name2, name1, name2)

        query = """
        select 
            Authors.affnid      AS affnid, 
            Affiliations.title  AS title, 
            Papers.year         AS year, 
            SUM (CASE WHEN Copyrights.pubtype = 1 THEN Copyrights.score ELSE 0 END) AS conf_paper,
            SUM (CASE WHEN Copyrights.pubtype = 2 THEN Copyrights.score ELSE 0 END) AS journal_paper,
            SUM (Copyrights.score) AS paper

        FROM Copyrights 
        INNER JOIN Authors on Copyrights.aid = Authors.aid 
        INNER JOIN Affiliations on Affiliations.sid = Authors.affnid
        INNER JOIN Papers on Papers.pid = Copyrights.pid
        WHERE Affiliations.sid = """ + sid + ' AND (1 = 0 '

        for c in conf:
            query = query + " OR (Copyrights.pubtype = 1 AND Copyrights.pubid = " + c + ")"

        for j in journal:
            query = query + " OR (Copyrights.pubtype = 2 AND Copyrights.pubid = " + j + ")"

        query = query + ") GROUP BY Authors.affnid, Papers.year ORDER BY paper DESC"

        cur.execute (query)
 
        rows = cur.fetchall ()
        for row in rows:
	        ret = ret + '<input type="hidden" id="data_1_' + str (row[2]) + '" conf="' + str (row[3]) + '" journal="' + str (row[4]) + '" total="' + str(row[5]) + '"/>'
        
        query = """
        select 
            Authors.affnid      AS affnid, 
            Affiliations.title  AS title, 
            Papers.year         AS year, 
            SUM (CASE WHEN Copyrights.pubtype = 1 THEN Copyrights.score ELSE 0 END) AS conf_paper,
            SUM (CASE WHEN Copyrights.pubtype = 2 THEN Copyrights.score ELSE 0 END) AS journal_paper,
            SUM (Copyrights.score) AS paper

        FROM Copyrights 
        INNER JOIN Authors on Copyrights.aid = Authors.aid 
        INNER JOIN Affiliations on Affiliations.sid = Authors.affnid
        INNER JOIN Papers on Papers.pid = Copyrights.pid
        WHERE Affiliations.sid = """ + sid2 + ' AND (1 = 0 '

        for c in conf:
            query = query + " OR (Copyrights.pubtype = 1 AND Copyrights.pubid = " + c + ")"

        for j in journal:
            query = query + " OR (Copyrights.pubtype = 2 AND Copyrights.pubid = " + j + ")"

        query = query + ") GROUP BY Authors.affnid, Papers.year ORDER BY paper DESC"

        cur.execute (query)
 
        rows = cur.fetchall ()
        for row in rows:
	        ret = ret + '<input type="hidden" id="data_2_' + str (row[2]) + '" conf="' + str (row[3]) + '" journal="' + str (row[4]) + '" total="' + str(row[5]) + '"/>'


        ret = ret + template ("tpl/compare2")

        return ret

run(host='localhost', port=8888, debug=False)
