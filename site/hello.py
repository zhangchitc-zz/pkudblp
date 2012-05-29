from bottle import static_file, post, route, run, template, request
import sqlite3

con = sqlite3.connect ('pkudblp.db')

@route('/static/:filename')
def getfile (filename):
    return static_file (filename, root='static')

@route('/')
def index():
    with con:
        cur = con.cursor ()
        ret = """
        <html>
        <head>
        <script language="JavaScript">
        function SetAllCheckBoxes(FormName, FieldName, CheckValue)
        {
            if(!document.forms[FormName]) return;
            var objCheckBoxes = document.forms[FormName].elements[FieldName];
            if(!objCheckBoxes) return;
            var countCheckBoxes = objCheckBoxes.length;
            if(!countCheckBoxes) objCheckBoxes.checked = CheckValue;
            else
                 // set the check value for all check boxes
                 for(var i = 0; i < countCheckBoxes; i++) {
                    // alert (objCheckBoxes[i].value);
                    objCheckBoxes[i].checked = CheckValue;
                 }
        }
        </script>

        </head>
        <body>
        <form name="list" action="/rank" method="post">
        <table>
        """

        cur.execute ("SELECT * FROM Conferences")
        rows = cur.fetchall ()

        for row in rows:
            ret = ret + "<tr>"
            ret = ret + """<td> <input type="checkbox" name="conf" value=" """ + str (row[0]) + """ "></td> """
            ret = ret + "<td> Conference </td>"
            ret = ret + "<td>" + row[1].upper () + "</td>"
            ret = ret + "<td>" + row[2] + "</td>"
            ret = ret + "</tr>"
 
        cur.execute ("SELECT * FROM Journals")
        rows = cur.fetchall ()

        for row in rows:
            ret = ret + "<tr>"
            ret = ret + """<td> <input type="checkbox" name="journal" value=" """ + str (row[0]) + """ "></td> """
            ret = ret + "<td> Journal </td>"
            ret = ret + "<td>" + row[1].upper () + "</td>"
            ret = ret + "<td>" + row[2] + "</td>"
            ret = ret + "</tr>"
       
        ret = ret + """</table> 
            <input type="button" onClick="SetAllCheckBoxes('list', 'conf', true);" value= "Select All Conferences"/> <br/> 
            <input type="button" onClick="SetAllCheckBoxes('list', 'journal', true)" value="Select All Journals"/> <br/>
            <input type="button" onClick="SetAllCheckBoxes('list', 'conf', false); SetAllCheckBoxes('list', 'journal', false);" value="Clear All"/>
        
        """
        ret = ret + '<input type="submit" onclick="document.list.action=\'/rank\'; return true;" value="Rank All Affiliations"><br>'

        cur.execute ("SELECT * FROM Affiliations")
        rows = cur.fetchall ()

        ret = ret + "<select name='sid'>"
        for row in rows:
            ret = ret + '<option value="' + str (row[0]) + '">' + row[1] + '</option>'
        ret = ret + '</select>'


        ret = ret + '<input type="button" value="See Trend" onclick="document.list.action=\'/trend\'; document.list.submit (); return true;"><br/>'

        ret = ret + "<select name='sid2'>"
        for row in rows:
            ret = ret + '<option value="' + str (row[0]) + '">' + row[1] + '</option>'
        ret = ret + '</select>'


        ret = ret + '<input type="button" value="Compare Them" onclick="document.list.action=\'/compare\'; document.list.submit (); return true;"><br/>'

        ret = ret + """</form> </body></html>"""
        return ret

@post ('/rank')
def index ():
    conf = request.forms.getlist ('conf')
    journal = request.forms.getlist ('journal')

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
                ret = ret + template ("tpl/rank2", rank=rank, affn=row[1], total="%.2f" % row[4], conf="%.2f" % row[3], journal="%.2f" % row[2])
            else:
                ret = ret + template ("tpl/rank3", rank=rank, affn=row[1], total="%.2f" % row[4], conf="%.2f" % row[3], journal="%.2f" % row[2])
 
            rank = rank + 1

        ret = ret + template ("tpl/rank4")

        return ret


@post ('/trend')
def index ():
    conf = request.forms.getlist ('conf')
    journal = request.forms.getlist ('journal')
    sid = request.forms.get ('sid')
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

run(host='192.168.3.189', port=8888, debug=False)
