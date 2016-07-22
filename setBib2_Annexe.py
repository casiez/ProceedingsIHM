#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Authors: Jonathan Aceituno and Alix Goguey

import os, re, sys
from pyPdf import PdfFileReader
import unicodedata
import glob

def remove_accents(data):
	return data.replace('é','e').replace('è','e')

def formatName(name):
	name = name.lower()
	return remove_accents(name).split(' ')[0]

def oneLineAuthor(authors_gname,authors_fname):
	authors = ""
	for k in range(len(authors_gname)):
		authors += authors_gname[k].strip()
		authors += ' '
		authors += authors_fname[k].strip()
		authors += ', '

	#authors.replace('  ',' ').replace('   ',' ')
	return authors[:-2]

def formatHalAuthor(authors_gname,authors_fname,authors_aff,authors_email):#data,indx_h):
	authors = ""
	for k in range(len(authors_gname)):
		authors += '<author role="aut">\n'
		authors += '<persName>\n'
		authors += '<forename type="first">'
		authors += authors_fname[k]
		authors += '</forename>\n'
		authors += '<surname>'
		authors += authors_gname[k]
		authors += '</surname>\n'
		authors += '</persName>\n'

		authors += '<email>'
		authors += authors_email[k]
		authors += '</email>\n'

		for l in range(len(authors_aff[k])):
			authors += '<affiliation ref="'
			authors += authors_aff[k][l].replace('&','&amp;')
			authors += '"/>\n'

		authors += '</author>\n'

	return authors


os.system('mkdir hal-one-by-one/proceedingsAnnexe/')
os.system('cp archive-hal-annexe/proceedings.pdf hal-one-by-one/proceedingsAnnexe/proceedings.pdf')
toc_out = open('hal-one-by-one/proceedingsAnnexe/toHal.xml','w')

toc_out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
toc_out.write('<TEI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
toc_out.write('xsi:schemaLocation="http://www.tei-c.org/ns/1.0 http://api.archives-ouvertes.fr/documents/aofr-sword.xsd"\n')
toc_out.write('xmlns="http://www.tei-c.org/ns/1.0" xmlns:hal="http://hal.archives-ouvertes.fr/">\n')
toc_out.write('<text>\n')
toc_out.write('<body>\n')
toc_out.write('<listBibl>\n')

toc_out.write('<biblFull>\n')
toc_out.write('<titleStmt>\n')
toc_out.write('<title xml:lang="FR">Annexes des Actes de la 26ième conférence francophone sur l’Interaction Homme-Machine</title>\n')

toc_out.write('<author role="aut">\n')
toc_out.write('<persName>\n')
toc_out.write('<forename type="first">Goguey</forename>\n')
toc_out.write('<surname>Alix</surname>\n')
toc_out.write('</persName>\n')
toc_out.write('<email>alix.goguey@inria.fr</email>\n')
toc_out.write('<affiliation ref="Mint, Inria, Lille, France"/>\n')
toc_out.write('</author>\n')

toc_out.write('<author role="aut">\n')
toc_out.write('<persName>\n')
toc_out.write('<forename type="first">Chapuis</forename>\n')
toc_out.write('<surname>Olivier</surname>\n')
toc_out.write('</persName>\n')
toc_out.write('<email>chapuis@lri.fr</email>\n')
toc_out.write('<affiliation ref="Univ Paris-Sud &amp; CNRS(LRI), Orsay, France"/>\n')
toc_out.write('<affiliation ref="Inria, Orsay, France"/>\n')
toc_out.write('</author>\n')

toc_out.write('<author role="aut">\n')
toc_out.write('<persName>\n')
toc_out.write('<forename type="first">Conversy</forename>\n')
toc_out.write('<surname>Stéphane</surname>\n')
toc_out.write('</persName>\n')
toc_out.write('<email>chapuis@lri.fr</email>\n')
toc_out.write('<affiliation ref="Université de Toulouse - ENAC, France"/>\n')
toc_out.write('</author>\n')

toc_out.write('<author role="aut">\n')
toc_out.write('<persName>\n')
toc_out.write('<forename type="first">Rouillard</forename>\n')
toc_out.write('<surname>José</surname>\n')
toc_out.write('</persName>\n')
toc_out.write('<email>jose.rouillard@univ-lille1.fr</email>\n')
toc_out.write('<affiliation ref="LIFL Université Lille 1, France"/>\n')
toc_out.write('</author>\n')

toc_out.write('<author role="aut">\n')
toc_out.write('<persName>\n')
toc_out.write('<forename type="first">Vigouroux</forename>\n')
toc_out.write('<surname>Nadine</surname>\n')
toc_out.write('</persName>\n')
toc_out.write('<email>vigourou@irit.fr</email>\n')
toc_out.write('<affiliation ref="IRIT UMR 5505, Université de Toulouse 3 Paul Sabatier, Toulouse, France"/>\n')
toc_out.write('</author>\n')

toc_out.write('<author role="aut">\n')
toc_out.write('<persName>\n')
toc_out.write('<forename type="first">Casiez</forename>\n')
toc_out.write('<surname>Géry</surname>\n')
toc_out.write('</persName>\n')
toc_out.write('<email>gery.casiez@lifl.fr</email>\n')
toc_out.write('<affiliation ref="Université Lille 1, France"/>\n')
toc_out.write('</author>\n')

toc_out.write('<author role="aut">\n')
toc_out.write('<persName>\n')
toc_out.write('<forename type="first">Pietrzak</forename>\n')
toc_out.write('<surname>Thomas</surname>\n')
toc_out.write('</persName>\n')
toc_out.write('<email>thomas.pietrzak@lifl.fr</email>\n')
toc_out.write('<affiliation ref="Université Lille 1, France"/>\n')
toc_out.write('</author>\n')

toc_out.write('</titleStmt>\n')
toc_out.write('<editionStmt><edition>\n')
toc_out.write('<date notBefore="2014-11-10"/><date type="whenWritten">2014</date><ref type="file" target="proceedings.pdf" subtype="author" n="1" />\n')
toc_out.write('</edition></editionStmt>\n')
toc_out.write('<notesStmt>\n')
toc_out.write('<note type="audience" n="2"/>\n')
toc_out.write('<note type="popular" n="0"/>\n')
toc_out.write('<note type="proceedings" n="1"/>\n')
toc_out.write('<note type="peer" n="1"/>\n')
toc_out.write('<note type="invited" n="0"/>\n')
toc_out.write('<note type="commentary">Ce fichier regroupe en un seul document la préface et l\'index des auteurs des annexes des actes de la conférence IHM\'14</note>\n')
toc_out.write('</notesStmt>\n')
toc_out.write('<sourceDesc>\n')
toc_out.write('<biblStruct>\n')
toc_out.write('<analytic>\n')
toc_out.write('<title xml:lang="FR">Annexes des Actes de la 26ième conférence francophone sur l’Interaction Homme-Machine</title>\n')
toc_out.write('<author role="aut">\n')
toc_out.write('<persName>\n')
toc_out.write('<forename type="first">Goguey</forename>\n')
toc_out.write('<surname>Alix</surname>\n')
toc_out.write('</persName>\n')
toc_out.write('<email>alix.goguey@inria.fr</email>\n')
toc_out.write('<affiliation ref="Mint, Inria, Lille, France"/>\n')
toc_out.write('</author>\n')
toc_out.write('</analytic>\n')
toc_out.write('<monogr>\n')
toc_out.write('<title level="m">26e conférence francophone sur l\'Interaction Homme-Machine</title>\n')
toc_out.write('<meeting>\n')
toc_out.write('<title>26e conférence francophone sur l\'Interaction Homme-Machine</title>\n')
toc_out.write('<date type="start">2014-10-28</date>\n')
toc_out.write('<date type="end">2014-10-31</date>\n')
toc_out.write('<settlement>Lille</settlement>\n')
toc_out.write('<country key="FR"/>\n')
toc_out.write('</meeting>\n')
toc_out.write('<imprint>\n')
toc_out.write('<biblScope unit="pp">\n')
toc_out.write('1-8</biblScope>\n')
toc_out.write('<date type="datePub">2014</date>\n')
toc_out.write('</imprint>\n')
toc_out.write('</monogr>\n')
toc_out.write('</biblStruct>\n')
toc_out.write('</sourceDesc>\n')
toc_out.write('<profileDesc>\n')
toc_out.write('<langUsage>\n')
toc_out.write('<language ident="FR"/>\n')
toc_out.write('</langUsage>\n')
toc_out.write('<abstract xml:lang="fr">L\'Association Francophone d\'Interaction Homme-Machine (AFIHM) et Inria sont heureux de présenter la 26ième édition de la conférence IHM, organisée cette année à Villeneuve d\'Ascq.</abstract>\n')
toc_out.write('</profileDesc>\n')
toc_out.write('</biblFull>\n\n')

toc_out.write('</listBibl>\n')
toc_out.write('</body>\n')
toc_out.write('</text>\n')
toc_out.write('</TEI>\n')

toc_out.close()

dir_file = 'Annexes14/All/'

curPage = 1

session = None
session_aux = None
indx_session = {}
for row in open(dir_file+'toc.txt','r'):
	row.strip().strip('\r\n')
	indx_session[row[0]] = row[4:]

all_authors = []
associate_pages = {}

for file in glob.glob(dir_file+"*.pdf"):
	print file
	#print file[:-3]+'txt'

	authors_fname = []
	authors_gname = []
	authors_aff = []
	authors_email = []
	title = ""
	abstract = ""
	keywords = []

	if (session_aux != indx_session[file.split('/')[-1][0]]):
		session_aux = indx_session[file.split('/')[-1][0]]
		session = session_aux.replace("'","\\'").replace(' ','\ ').replace('>',"\\>")#.replace('é','e').replace('è','e')

	for row in open(file[:-3]+'txt','r'):
		row = row.strip().strip('\r\n')
		#print row
		if (row[:5] == "Titre"):
			title =  row[8:]
			#print 'titre'
		elif (row[:8] == 'Abstract'):
			abstract = row[11:]
			#print 'abs'
		elif (row[:8] == 'Keywords'):
			keywords = row[11:].split(';')
			#print 'key'
		elif (row[:7] == 'Prénom'):
			authors_gname.append(row[12:])
			authors_aff.append([])
			#print 'pre'
		elif (row[:3] == 'Nom'):
			authors_fname.append(row[8:])
			#print 'nom'
		elif (row[:5] == 'Email'):
			authors_email.append(row[10:])
			#print 'email'
		elif (row[:11] == 'Affiliation'):
			authors_aff[-1].append(row[18:])
			#print 'aff'

	pdf = PdfFileReader(open(file,'rb'))
	nbPage = pdf.getNumPages()

	#print authors_fname
	#print authors_gname
	paper_basename = 'p'+str(curPage)+'-'+formatName(authors_fname[0])
	curPage += nbPage

	for k in range(len(authors_fname)):
		author = authors_gname[k].strip()
		author += ' '
		author += authors_fname[k].strip()
		all_authors.append(author)
		associate_pages.setdefault(author, [])
		associate_pages[author].append(curPage-nbPage)

	os.system('mkdir hal-one-by-one/'+paper_basename)
	os.system('cp archive-hal-annexe/'+paper_basename+'.pdf hal-one-by-one/'+paper_basename+'/'+paper_basename+'.pdf')
	toc_out = open('hal-one-by-one/'+paper_basename+'/toHal.xml','w')

	toc_out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
	toc_out.write('<TEI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
	toc_out.write('xsi:schemaLocation="http://www.tei-c.org/ns/1.0 http://api.archives-ouvertes.fr/documents/aofr-sword.xsd"\n')
	toc_out.write('xmlns="http://www.tei-c.org/ns/1.0" xmlns:hal="http://hal.archives-ouvertes.fr/">\n')
	toc_out.write('<text>\n')
	toc_out.write('<body>\n')
	toc_out.write('<listBibl>\n')

	toc_out.write('<biblFull>\n')

	toc_out.write('<titleStmt>\n')
	toc_out.write('<title xml:lang="FR">')
	toc_out.write(title.replace('<','&lt;').replace('>','&gt;'))
	toc_out.write('</title>\n')
	toc_out.write(formatHalAuthor(authors_gname,authors_fname,authors_aff,authors_email))
	toc_out.write('</titleStmt>\n')

	toc_out.write('<editionStmt><edition>\n')

	toc_out.write('<date notBefore="2014-11-10"/>')
	toc_out.write('<date type="whenWritten">2014</date>')
	toc_out.write('<ref type="file" target="')
	toc_out.write(paper_basename + '.pdf')
	toc_out.write('" subtype="author" n="1" />\n')

	toc_out.write('</edition></editionStmt>\n')

	toc_out.write('<notesStmt>\n')
	toc_out.write('<note type="audience" n="2"/>\n')
	toc_out.write('<note type="popular" n="0"/>\n')
	toc_out.write('<note type="proceedings" n="1"/>\n')
	toc_out.write('<note type="peer" n="1"/>\n')
	toc_out.write('<note type="invited" n="0"/>\n')
	toc_out.write('</notesStmt>\n')


	toc_out.write('<sourceDesc>\n<biblStruct>\n')
	toc_out.write('<analytic>\n')
	toc_out.write('<title xml:lang="FR">')
	toc_out.write(title.replace('<','&lt;').replace('>','&gt;'))
	toc_out.write('</title>\n')
	toc_out.write(formatHalAuthor(authors_gname,authors_fname,authors_aff,authors_email))
	toc_out.write('</analytic>\n')
	toc_out.write('<monogr>\n')
	toc_out.write('<title level="m">26e conférence francophone sur l\'Interaction Homme-Machine</title>\n')
	toc_out.write('<meeting>\n')
	toc_out.write('<title>26e conférence francophone sur l\'Interaction Homme-Machine</title>\n')
	toc_out.write('<date type="start">2014-10-28</date>\n')
	toc_out.write('<date type="end">2014-10-31</date>\n')
	toc_out.write('<settlement>Lille</settlement>\n')
	toc_out.write('<country key="FR"/>\n')
	toc_out.write('</meeting>\n')
	toc_out.write('<imprint>\n')
	toc_out.write('<biblScope unit="pp">\n')
	toc_out.write(str(curPage-nbPage)+'-'+str(curPage-1))
	toc_out.write('</biblScope>\n')
	toc_out.write('<date type="datePub">2014</date>\n')
	toc_out.write('</imprint>\n</monogr>\n')
	toc_out.write('</biblStruct>\n</sourceDesc>\n')

	toc_out.write('<profileDesc>\n')
	toc_out.write('<langUsage>\n<language ident="FR"/>\n</langUsage>\n')
	toc_out.write('<textClass>\n<keywords scheme="author">\n')
	toc_out.write("".join(['<term xml:lang="fr">{}</term>\n'.format(i) for i in keywords]))
	toc_out.write('</keywords>\n')
	toc_out.write('<classCode scheme="halDomain" n="info"/>\n')
	toc_out.write('<classCode scheme="halTypology" n="COMM"></classCode>\n')
	toc_out.write('</textClass>\n')
	toc_out.write('<abstract xml:lang="fr">')
	toc_out.write(abstract.replace('<','&lt;').replace('>','&gt;'))
	toc_out.write('</abstract>\n')

	toc_out.write('</profileDesc>\n')

	toc_out.write('</biblFull>\n\n\n')

	toc_out.write('</listBibl>\n')
	toc_out.write('</body>\n')
	toc_out.write('</text>\n')
	toc_out.write('</TEI>\n')

	toc_out.close()
