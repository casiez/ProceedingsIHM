#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Authors: Jonathan Aceituno and Alix Goguey

import os, re, sys
from pyPdf import PdfFileReader
import unicodedata
import csv

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

toc = open('Table_of_Content.txt','r')

toc_out = open('archive-acm/toc.txt','w')

toctoc = open('visual-check/toc.txt','w')

dir_file = 'ihm14a_final_submissions/'
prePdf = 'paper-'
authors = ""
title = ""

curPage = 1
indx = 1

session = None

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

for row in toc:
	row = row.split('\n')[0]

	if (dir_file == 'ihm14b_final_submissions/'):
		reader = csv.reader(open("TeC/ihm14b_submissions.csv", "rb"))
	else:
		reader = csv.reader(open("Articles/ihm14a_submissions.csv", "rb"))


	if (row[:7] == "Session"):
		session =  row.replace("'","\\'").replace(' ','\ ').replace('>',"\\>")#.replace('é','e').replace('è','e')
		toc_out.write(row + '\n\n')
	elif (row[:2] == 'Pr'):
		toc_out.write('Session : Travaux en Cours (TeC)\n\n')
		session =  'Session\ :\ Travaux\ en\ Cours\ \(TeC\)'
		dir_file = 'ihm14b_final_submissions/'
		prePdf = ''
		indx_h = indexb
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

		toctoc.write(str(indx) + '  ->  ' + str(curPage) + '\n')
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

		if (final and (thumbnail != False)):
			os.system('cp '+thumbnail+' archive-acm/'+paper_basename+'-thumbnail'+thumbnail[-4:])
			os.system('cp '+thumbnail+' archive-hal/'+paper_basename+'-thumbnail'+thumbnail[-4:])

		video = False
		if (os.path.exists(dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file1.mp4')):
			video = dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file1.mp4'
		elif (os.path.exists(dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file1.mov')):
			video = dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file1.mov'
		elif (os.path.exists(dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file2.mp4')):
			video = dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file2.mp4'
		elif (os.path.exists(dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file2.mov')):
			video = dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file2.mov'

		if (final and (video != False)):
			os.system('cp '+video+' archive-acm/'+paper_basename+'-video'+video[-4:])
			os.system('cp '+video+' archive-hal/'+paper_basename+'-video'+video[-4:])

		poster = False
		if (os.path.exists(dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file1.pdf')):
			poster = dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-file1.pdf'

		if (final and (poster != False)):
			os.system('cp '+poster+' archive-acm/'+paper_basename+'-poster.pdf')
			os.system('cp '+poster+' archive-hal/'+paper_basename+'-poster.pdf')


		toc_out.write('Original '+title+'\n')
		toc_out.write('Title in English: '+csv_data[indx_h['Title in English']]+'\n')
		toc_out.write('Original Abstract: '+csv_data[indx_h['Abstract']]+'\n')
		toc_out.write('Abstract in English: '+csv_data[indx_h['Abstract in English']]+'\n')
		#toc_out.write('Original Keywords: '+csv_data[indx_h['Keywords']]+'\n')
		toc_out.write('Keywords in English: '+csv_data[indx_h['Keywords in Englsh']]+'\n')
		toc_out.write(authors+'\n')
		toc_out.write('DOI: '+doi+'\n')
		toc_out.write('Paper name: '+paper_basename+'.pdf\n')
		toc_out.write('Pages: '+str(curPage-nbPage)+'-'+str(curPage-1)+'\n')
		if (thumbnail != False):
			toc_out.write('Thumbnail: '+paper_basename+'-thumbnail'+thumbnail[-4:]+'\n')
		else:
			toc_out.write('Thumbnail: NONE\n')

		if (video != False):
			toc_out.write('Video: '+paper_basename+'-video'+video[-4:]+'\n')
		else:
			toc_out.write('Video: NONE\n')

		if (poster != False):
			toc_out.write('Poster: '+paper_basename+'-poster.pdf\n\n')
		else:
			toc_out.write('Poster: NONE\n\n')


		print 'ScriptsIHM14/ScriptsIHM14/PreparePDF -input '+dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-paper.pdf'+' -output visual-check/'+paper_basename+'.pdf -debug 1'+" -conf IHM\\'14,\\ Villeneuve\\ d\\'Ascq,\\ France"+' -session '+session

		if (dir_file == 'ihm14a_final_submissions/'):
			os.system('ScriptsIHM14/ScriptsIHM14/PreparePDF -input '
				+dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-paper.pdf'
 				+' -output visual-check/'+paper_basename+'.pdf -debug 1'
				+" -conf IHM\\'14,\\ Villeneuve\\ d\\'Ascq,\\ France"+' -session '+session)
			os.system('ScriptsIHM14/ScriptsIHM14/PreparePDF -input '
				+dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-paper.pdf'
 				+' -output visual-check/'+paper_basename+'-hal.pdf -copyright ScriptsIHM14/ScriptsIHM14/copyright2.pdf'
				+' -doi '+doi+' -debug 1'
				+" -conf IHM\\'14,\\ Villeneuve\\ d\\'Ascq,\\ France"+' -session '+session)

			os.system('ScriptsIHM14/ScriptsIHM14/PreparePDF -input '
				+dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-paper.pdf'
 				+' -output archive-acm/'+paper_basename+'.pdf'
				+' -doi '+doi+' -startpage '+str(curPage-nbPage)+' -title '+title[7:]
				+' -author '+authors[9:]
				+" -conf IHM\\'14,\\ Villeneuve\\ d\\'Ascq,\\ France"+' -session '+session)
			os.system('ScriptsIHM14/ScriptsIHM14/PreparePDF -input '
				+dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-paper.pdf'
 				+' -output archive-hal/'+paper_basename+'.pdf -copyright ScriptsIHM14/ScriptsIHM14/copyright2.pdf'
				+' -doi '+doi+' -startpage '+str(curPage-nbPage)+' -title '+title[7:]
				+' -author '+authors[9:]
				+" -conf IHM\\'14,\\ Villeneuve\\ d\\'Ascq,\\ France"+' -session '+session)

		else:
			os.system('ScriptsIHM14-TeC/ScriptsIHM14-TeC/PreparePDF -input '
				+dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-paper_a4.pdf'
 				+' -output visual-check/'+paper_basename+'.pdf -debug 1'
				+" -conf IHM\\'14,\\ Villeneuve\\ d\\'Ascq,\\ France"+' -session '+session)
			os.system('ScriptsIHM14-TeC/ScriptsIHM14-TeC/PreparePDF -input '
				+dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-paper_a4.pdf'
 				+' -output visual-check/'+paper_basename+'-hal.pdf -copyright ScriptsIHM14-TeC/ScriptsIHM14-TeC/copyright2.pdf'
				+' -doi '+doi+' -debug 1'
				+" -conf IHM\\'14,\\ Villeneuve\\ d\\'Ascq,\\ France"+' -session '+session)

			os.system('ScriptsIHM14-TeC/ScriptsIHM14-TeC/PreparePDF -input '
				+dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-paper_a4.pdf'
 				+' -output archive-acm/'+paper_basename+'.pdf'
				+' -doi '+doi+' -startpage '+str(curPage-nbPage)+' -title '+title[7:]
				+' -author '+authors[9:]
				+" -conf IHM\\'14,\\ Villeneuve\\ d\\'Ascq,\\ France"+' -session '+session)
			os.system('ScriptsIHM14-TeC/ScriptsIHM14-TeC/PreparePDF -input '
				+dir_file+str(paper_nb)+'/'+prePdf+str(paper_nb_filled)+'-paper_a4.pdf'
 				+' -output archive-hal/'+paper_basename+'.pdf -copyright ScriptsIHM14/ScriptsIHM14/copyright2.pdf'
				+' -doi '+doi+' -startpage '+str(curPage-nbPage)+' -title '+title[7:]
				+' -author '+authors[9:]
				+" -conf IHM\\'14,\\ Villeneuve\\ d\\'Ascq,\\ France"+' -session '+session)


toctoc.close()
os.system('cp archive-acm/toc.txt archive-hal/toc.txt')
toc_out.close()

os.system('cp Actes14/meta_data.txt archive-acm/meta_data.txt')
os.system('cp Actes14/meta_data.txt archive-hal/meta_data.txt')

os.system('cp Actes14/frontmatter.pdf archive-acm/frontmatter.pdf')
os.system('cp Actes14/frontmatter.pdf archive-hal/frontmatter.pdf')

os.system('cp Actes14/backmatter.pdf archive-acm/backmatter.pdf')
os.system('cp Actes14/backmatter.pdf archive-hal/backmatter.pdf')

# f = []
# for (dirpath, dirnames, filenames) in os.walk('ihm14a_final_submissions/'):
# 	print dirnames
# 	for paper_nb in dirnames:
# 		print "Paper " + paper_nb
# 		paper_nb_filled = paper_nb.zfill(4)

# 		# META Data
# 		index_file = open('ihm14a_final_submissions/'+str(paper_nb)+'/index.html','r')

# 		title = ""
# 		authors = ""
# 		inAutor = False
# 		for row in index_file:
# 			row = row.split('\n')[0]

# 			if (row[:13] == '<h2 id=title>'):
# 				title = row[13:-5]
# 			elif (row == '<ul id=authors>'):
# 				inAutor = True
# 			elif ((row == '</ul>') and inAutor):
# 				inAutor = False
# 			elif ((row[:4] == '<li>') and inAutor):
# 				authors += row[4:].split(',')[0] + ', '

# 		authors = authors[:-2]

# 		doi_file = open('ihm14a_final_submissions/'+str(paper_nb)+'/doi.txt','r')
# 		doi = ""
# 		for row in doi_file:
# 			doi = row
# 			break

# 		print "META:"
# 		print " - Title: " + title
# 		print " - Authors: " + authors
# 		print " - Doi: " + doi

# 		os.system('ScriptsIHM14/ScriptsIHM14/PreparePDF -input ihm14a_final_submissions/'+
# 			str(paper_nb)+'/paper-'+str(paper_nb_filled)+
# 			'-paper.pdf -output paper_to_visual_check/paper-'+
# 			str(paper_nb_filled)+'-paper.pdf -debug 1')
# 	break

# f = []
# for (dirpath, dirnames, filenames) in os.walk('ihm14b_final_submissions/'):
# 	print dirnames
# 	for paper_nb in dirnames:
# 		print "TeC " + paper_nb
# 		paper_nb_filled = paper_nb.zfill(4)

# 		# META Data
# 		index_file = open('ihm14b_final_submissions/'+str(paper_nb)+'/index.html','r')

# 		title = ""
# 		authors = ""
# 		inAutor = False
# 		for row in index_file:
# 			row = row.split('\n')[0]

# 			if (row[:13] == '<h2 id=title>'):
# 				title = row[13:-5]
# 			elif (row == '<ul id=authors>'):
# 				inAutor = True
# 			elif ((row == '</ul>') and inAutor):
# 				inAutor = False
# 			elif ((row[:4] == '<li>') and inAutor):
# 				authors += row[4:].split(',')[0] + ', '

# 		authors = authors[:-2]

# 		doi_file = open('ihm14b_final_submissions/'+str(paper_nb)+'/doi.txt','r')
# 		doi = ""
# 		for row in doi_file:
# 			doi = row
# 			break

# 		print "META:"
# 		print " - Title: " + title
# 		print " - Authors: " + authors
# 		print " - Doi: " + doi

# 		os.system('ScriptsIHM14-TeC/ScriptsIHM14-TeC/PreparePDF -input ihm14b_final_submissions/'+
# 			str(paper_nb)+'/'+str(paper_nb_filled)+
# 			'-paper.pdf -output tec_to_visual_check/'+
# 			str(paper_nb_filled)+'-paper.pdf -debug 1')

# 	break

# # -startpage <number>
# #	Start from given page number (0 for no page numbers)
# # -title <title>
# #	Set the title in PDF metadata
# # -author <author>
# #	Set the authors in PDF metadata (comma-separated)
# # -debug 1
# #	Overlay debug lines
# # -copyright <file.pdf>
# #	Different copyright overlay
# # -doi <text>
# #	Add a text in the position of the DOI in ACM Author versions
# # -logo <file.pdf>
# #	Different logo overlay