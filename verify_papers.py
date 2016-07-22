# Authors: Jonathan Aceituno and Alix Goguey

import os, re, sys

f = []
for (dirpath, dirnames, filenames) in os.walk('ihm14a_final_submissions/'):
	print dirnames
	for paper_nb in dirnames:
		print "Paper " + paper_nb
		paper_nb_filled = paper_nb.zfill(4)

		# META Data
		index_file = open('ihm14a_final_submissions/'+str(paper_nb)+'/index.html','r')

		title = ""
		authors = ""
		inAutor = False
		for row in index_file:
			row = row.split('\n')[0]

			if (row[:13] == '<h2 id=title>'):
				title = row[13:-5]
			elif (row == '<ul id=authors>'):
				inAutor = True
			elif ((row == '</ul>') and inAutor):
				inAutor = False
			elif ((row[:4] == '<li>') and inAutor):
				authors += row[4:].split(',')[0] + ', '

		authors = authors[:-2]

		doi_file = open('ihm14a_final_submissions/'+str(paper_nb)+'/doi.txt','r')
		doi = ""
		for row in doi_file:
			doi = row
			break

		print "META:"
		print " - Title: " + title
		print " - Authors: " + authors
		print " - Doi: " + doi

		os.system('ScriptsIHM14/ScriptsIHM14/PreparePDF -input ihm14a_final_submissions/'+
			str(paper_nb)+'/paper-'+str(paper_nb_filled)+
			'-paper.pdf -output paper_to_visual_check/paper-'+
			str(paper_nb_filled)+'-paper.pdf -debug 1')
	break

f = []
for (dirpath, dirnames, filenames) in os.walk('ihm14b_final_submissions/'):
	print dirnames
	for paper_nb in dirnames:
		print "TeC " + paper_nb
		paper_nb_filled = paper_nb.zfill(4)

		# META Data
		index_file = open('ihm14b_final_submissions/'+str(paper_nb)+'/index.html','r')

		title = ""
		authors = ""
		inAutor = False
		for row in index_file:
			row = row.split('\n')[0]

			if (row[:13] == '<h2 id=title>'):
				title = row[13:-5]
			elif (row == '<ul id=authors>'):
				inAutor = True
			elif ((row == '</ul>') and inAutor):
				inAutor = False
			elif ((row[:4] == '<li>') and inAutor):
				authors += row[4:].split(',')[0] + ', '

		authors = authors[:-2]

		doi_file = open('ihm14b_final_submissions/'+str(paper_nb)+'/doi.txt','r')
		doi = ""
		for row in doi_file:
			doi = row
			break

		print "META:"
		print " - Title: " + title
		print " - Authors: " + authors
		print " - Doi: " + doi

		os.system('ScriptsIHM14-TeC/ScriptsIHM14-TeC/PreparePDF -input ihm14b_final_submissions/'+
			str(paper_nb)+'/'+str(paper_nb_filled)+
			'-paper.pdf -output tec_to_visual_check/'+
			str(paper_nb_filled)+'-paper.pdf -debug 1')

	break

# -startpage <number>
#	Start from given page number (0 for no page numbers)
# -title <title>
#	Set the title in PDF metadata
# -author <author>
#	Set the authors in PDF metadata (comma-separated)
# -debug 1
#	Overlay debug lines
# -copyright <file.pdf>
#	Different copyright overlay
# -doi <text>
#	Add a text in the position of the DOI in ACM Author versions
# -logo <file.pdf>
#	Different logo overlay