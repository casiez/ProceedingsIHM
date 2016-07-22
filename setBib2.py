#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Authors: Jonathan Aceituno and Alix Goguey

import os, re, sys
import csv
from pyPdf import PdfFileReader
import unicodedata

final = False

if (len(sys.argv) > 2):
	print ''
	print 'Too many arguments'
	print 'Usage: python setArchive.py [-final]'
	print ' -final : set the final archive (with auxiliary materials'
	print ''
	sys.exit()
elif ((len(sys.argv) == 2) and (sys.argv[1] == '-final')):
	final = True
elif (len(sys.argv) == 2):
	print ''
	print 'Unknown argument'
	print 'Usage: python setArchive.py [-final]'
	print ' -final : set the final archive (with auxiliary materials'
	print ''
	sys.exit()

def remove_accents(data):
    return data.replace('é','e').replace('è','e')

def formatName(name):
	name = name.lower()
	return remove_accents(name)

def formatNames(names):
	s = ''

	for name in names.split(' '):
		for sub_name in name.split('-'):
			sub_name = sub_name[0].upper() + sub_name[1:].lower()
			s += sub_name + ' '
		s = s[:-1] + ' '
	s = s[:-1]

	return s

def formatHalAuthor(data,indx_h):
	authors = ""
	for k in range(1,11):
		if (data[indx_h['Given name ' + str(k)]] != ""):
			authors += '<author role="aut">\n'
			authors += '<persName>\n'
			authors += '<forename type="first">'
			authors += formatNames(data[indx_h['Family name ' + str(k)]])
			authors += '</forename>\n'
			authors += '<surname>'
			authors += formatNames(data[indx_h['Given name ' + str(k)]])
			authors += '</surname>\n'
			authors += '</persName>\n'

			authors += '<email>'
			authors += data[indx_h['Email address ' + str(k)]]
			authors += '</email>\n'

			authors += '<affiliation ref="'
			authors += data[indx_h['Primary Affiliation ' + str(k) + ' - Institution']].replace('&','&amp;')
			authors += '"/>\n'

			if (data[indx_h['Secondary Affiliation (optional) ' + str(k) + ' - Institution']] != ""):
				authors += '<affiliation ref="'
				authors += data[indx_h['Secondary Affiliation (optional) ' + str(k) + ' - Institution']].replace('&','&amp;')
				authors += '"/>\n'

			authors += '</author>\n'

	return authors

indx_h = None

indexa = {}
reader = csv.reader(open("Articles/ihm14a_submissions.csv", "rb"))
for row in reader:
	for k in range(len(row)):
		indexa[row[k]] = k
	break

indexb = {}
reader = csv.reader(open("TeC/ihm14b_submissions.csv", "rb"))
for row in reader:
	for k in range(len(row)):
		indexb[row[k]] = k
	break
indexb['Title in English'] = indexb['Title in english:']
indexb['Abstract in English'] = indexb['Abstract in english:']
indexb['Keywords in Englsh'] = indexb['Keywords in english:']

indx_h = indexa

toc = open('Table_of_Content.txt','r')

os.system('mkdir hal-one-by-one/proceedings/')
os.system('cp archive-hal/proceedings.pdf hal-one-by-one/proceedings/proceedings.pdf')
toc_out = open('hal-one-by-one/proceedings/toHal.xml','w')

toc_out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
toc_out.write('<TEI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
toc_out.write('xsi:schemaLocation="http://www.tei-c.org/ns/1.0 http://api.archives-ouvertes.fr/documents/aofr-sword.xsd"\n')
toc_out.write('xmlns="http://www.tei-c.org/ns/1.0" xmlns:hal="http://hal.archives-ouvertes.fr/">\n')
toc_out.write('<text>\n')
toc_out.write('<body>\n')
toc_out.write('<listBibl>\n')

toc_out.write('<biblFull>\n')
toc_out.write('<titleStmt>\n')
toc_out.write('<title xml:lang="FR">Actes de la 26ième conférence francophone sur l’Interaction Homme-Machine</title>\n')

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
toc_out.write('<note type="commentary">Ce fichier regroupe en un seul document la préface et l\'index des auteurs des actes de la conférence IHM\'14</note>\n')
toc_out.write('</notesStmt>\n')
toc_out.write('<sourceDesc>\n')
toc_out.write('<biblStruct>\n')
toc_out.write('<analytic>\n')
toc_out.write('<title xml:lang="FR">Actes de la 26ième conférence francophone sur l’Interaction Homme-Machine</title>\n')
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
toc_out.write('<publisher>ACM</publisher>\n')
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

dir_file = 'ihm14a_final_submissions/'
prePdf = 'paper-'
authors = ""
title = ""

curPage = 1
indx = 1

for row in toc:
	row = row.split('\n')[0]

	if (dir_file == 'ihm14b_final_submissions/'):
		reader = csv.reader(open("TeC/ihm14b_submissions.csv", "rb"))
	else:
		reader = csv.reader(open("Articles/ihm14a_submissions.csv", "rb"))

	if (row[:7] == "Session"):
		#toc_out.write(row + '\n\n')
		continue
	elif (row[:2] == 'Pr'):
		#toc_out.write('Session: Travaux en Cours (TeC)\n\n')
		dir_file = 'ihm14b_final_submissions/'
		indx_h = indexb
		prePdf = ''
	elif (row[:6] == 'Title:'):
		title = row
	elif (row[:8] == 'Authors:'):
		authors = row
	elif (row[:8] == 'PCS-ind:'):

		paper_nb = int(row[9:])
		paper_nb_filled = str(paper_nb).zfill(4)

		skipHeader = True
		csv_data = None
		for csv_row in reader:
			if skipHeader:
				skipHeader = False
				continue
			else:
				if (dir_file == 'ihm14b_final_submissions/'):
					if (int(csv_row[indx_h['ID']]) == int(paper_nb)):
						csv_data = csv_row
						break
				else:
					if (int(csv_row[indx_h['ID']][6:]) == int(paper_nb)):
						csv_data = csv_row
						break

		pdf = PdfFileReader(open(dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-paper.pdf','rb'))
		nbPage = pdf.getNumPages()

		indx += 1

		doi_file = open(dir_file+str(paper_nb)+'/doi.txt','r')
		doi = ''
		for row in doi_file:
			doi = row
			break

		paper_basename = 'p'+str(curPage)+'-'+formatName(authors[9:].split(',')[0].split(' ')[-1])
		curPage += nbPage

		thumbnail = False
		if (os.path.exists(dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file1.png')):
			thumbnail = dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file1.png'
		elif (os.path.exists(dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file1.jpg')):
			thumbnail = dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file1.jpg'
		elif (os.path.exists(dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file2.png')):
			thumbnail = dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file2.png'
		elif (os.path.exists(dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file2.jpg')):
			thumbnail = dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file2.jpg'

		# if (final and (thumbnail != False)):
		# 	os.system('cp '+thumbnail+' archive-hal/'+paper_basename+'-thumbnail'+thumbnail[-4:])

		video = False
		if (os.path.exists(dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file1.mp4')):
			video = dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file1.mp4'
		elif (os.path.exists(dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file1.mov')):
			video = dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file1.mov'
		elif (os.path.exists(dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file2.mp4')):
			video = dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file2.mp4'
		elif (os.path.exists(dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file2.mov')):
			video = dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file2.mov'

		# if (final and (video != False)):
		# 	os.system('cp '+video+' archive-hal/'+paper_basename+'-video'+video[-4:])

		poster = False
		if (os.path.exists(dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file1.pdf')):
			poster = dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file1.pdf'

		# if (final and (poster != False)):
		# 	os.system('cp '+poster+' archive-hal/'+paper_basename+'-poster.pdf')

		os.system('mkdir hal-one-by-one/'+paper_basename)
		os.system('cp archive-hal/'+paper_basename+'.pdf hal-one-by-one/'+paper_basename+'/'+paper_basename+'.pdf')
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
		toc_out.write(title[7:])
		toc_out.write('</title>\n')
		toc_out.write('<title xml:lang="EN">')
		toc_out.write(csv_data[indx_h['Title in English']])
		toc_out.write('</title>\n')
		toc_out.write(formatHalAuthor(csv_data,indx_h))
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
		toc_out.write(title[7:])
		toc_out.write('</title>\n')
		toc_out.write('<title xml:lang="EN">')
		toc_out.write(csv_data[indx_h['Title in English']])
		toc_out.write('</title>\n')
		toc_out.write(formatHalAuthor(csv_data,indx_h))
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
		toc_out.write('<publisher>ACM</publisher>\n')
		toc_out.write('<biblScope unit="pp">\n')
		toc_out.write(str(curPage-nbPage)+'-'+str(curPage-1))
		toc_out.write('</biblScope>\n')
		toc_out.write('<date type="datePub">2014</date>\n')
		toc_out.write('</imprint>\n</monogr>\n')
		toc_out.write('</biblStruct>\n</sourceDesc>\n')

		toc_out.write('<profileDesc>\n')
		toc_out.write('<langUsage>\n<language ident="FR"/>\n</langUsage>\n')
		# toc_out.write('<textClass>\n<keywords scheme="author">\n')
		# toc_out.write("".join(['<term xml:lang="fr">{}</term>\n'.format(i) for i in csv_data[indx_h['Keywords']].split(';')]))
		# toc_out.write('</keywords>\n</textClass>\n')
		toc_out.write('<textClass>\n<keywords scheme="author">\n')
		toc_out.write("".join(['<term xml:lang="en">{}</term>\n'.format(i) for i in csv_data[indx_h['Keywords in Englsh']].replace(';',',').split(',')]))
		toc_out.write('</keywords>\n')
		toc_out.write('<classCode scheme="halDomain" n="info"/>\n')
		toc_out.write('<classCode scheme="halTypology" n="COMM"></classCode>\n')
		toc_out.write('</textClass>\n')
		toc_out.write('<abstract xml:lang="fr">')
		toc_out.write(csv_data[indx_h['Abstract']])
		toc_out.write('</abstract>\n')
		toc_out.write('<abstract xml:lang="en">')
		toc_out.write(csv_data[indx_h['Abstract in English']])
		toc_out.write('</abstract>\n')

		toc_out.write('</profileDesc>\n')

		toc_out.write('</biblFull>\n\n\n')

		toc_out.write('</listBibl>\n')
		toc_out.write('</body>\n')
		toc_out.write('</text>\n')
		toc_out.write('</TEI>\n')

		toc_out.close()
