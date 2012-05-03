#!/usr/bin/python

from lxml import etree
import sys, os

confs = []
journals = []

def prepare (cfile, jfile):
	f = open (cfile, 'r')
	for line in f.readlines():
		confs.append(line.split ('\t')[0])
	f.close ()
	
	f = open (jfile, 'r')
	for line in f.readlines():
		journals.append(line.split ('\t')[0])
	f.close ()


def parse (inputfile, outputfile, years = ['2006', '2007', '2008', '2009', '2010', '2011', '2012']):
	f = open (inputfile, 'r')
	o = open (outputfile, 'w')

	context = etree.iterparse (f, dtd_validation=True, events = ("end", ))
	count = 0
	total = 0

	# write a header for output xml
	o.write ("""<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE dblp SYSTEM "dblp.dtd">""")

	for event, elem in context:
		tag = elem.tag
		
		# if this node represent academic paper
		if tag in ['article', 'inproceedings', 'proceedings']:
			key = elem.get ('key')
			year = elem.xpath ('year/text()')[0]

			# if this paper appears in our desired top conference or journals
			if (key.startswith ('journals') and (key.split ('/')[1] in journals)) or \
			   (key.startswith ('conf') 	and (key.split ('/')[1] in confs)):
				# if this paper is relatively new
				if year in years:
					o.write (etree.tostring (elem).replace (' xmlns:="dblp"', ''))
					count = count + 1 
					print count
			
			elem.clear ()
			while elem.getprevious () is not None:
				del elem.getparent ()[0]

	o.write ("</dblp>")

	del context
	o.close ()
	f.close ()
	print total

if __name__ == '__main__':
	prepare (sys.argv[1], sys.argv[2])
	parse (sys.argv[3], sys.argv[4])
