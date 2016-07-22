#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# Authors: Jonathan Aceituno and Alix Goguey

import csv
import argparse
import subprocess
import os
import sys

class Author(object):
	def __init__(self, firstname, lastname, email, affiliation, secondaryaffiliation = None):
		self.firstname, self.lastname, self.email, self.affiliation, self.secondaryaffiliation = firstname, lastname, email, affiliation, secondaryaffiliation
	
	def name_string(self):
		return self.firstname + " " + self.lastname
	
	def name_and_mail_string(self):
		return self.name_string() + " <" + self.email + ">"

	def affiliations_string(self):
		if len(self.secondaryaffiliation) == 0:
			return self.affiliation
		return self.affiliation + ", " + self.secondaryaffiliation

	def name_and_affiliations_string(self, name_suffix = ""):
		return self.name_string() + name_suffix +  " (" + self.affiliations_string() + ")"

	def __str__(self):
		return self.name_and_affiliations_string()

def make_author_from_submission_row(row, number):
	numberstr = str(number)
	checkcolumn = 'Given name ' + numberstr
	if not checkcolumn in row or len(row[checkcolumn]) == 0:
		return None
	return Author(row['Given name ' + numberstr], row['Family name ' + numberstr], row['Email address ' + numberstr], row['Primary Affiliation ' + numberstr + ' - Institution'], row['Secondary Affiliation (optional) ' + numberstr + ' - Institution'])

class Submission(object):
	def __init__(self, title, session, order, filename, authors = [], contact_author = None):
		self.title, self.session, self.order, self.authors, self.contact_author = title, session, order, authors, contact_author
		self.filename = filename
		self.doi = None
	
	def authors_string(self, indicate_contact_author = False):
		return ", ".join([author.name_and_affiliations_string("*") if author == self.contact_author else author.name_and_affiliations_string() for author in self.authors])
	
	def short_authors_string(self):
		return ", ".join([author.name_string() for author in self.authors])

	def short_description(self):
		return self.title + ". " + self.authors_string(True) + "."

	def __str__(self):
		return self.short_description()
	
	def prepare_pdf(self, start_page = 1, debug = False, copyright = True, pagination = True):
		path_of_PreparePDF = os.path.dirname(os.path.realpath(sys.argv[0]))
		path_to_PreparePDF = os.path.join(path_of_PreparePDF, 'PreparePDF')
		dirname, basename = os.path.split(self.filename)
		outfilename = os.path.join(dirname, 'prepared-' + basename)
		startpage = start_page
		if not pagination:
			startpage = 1
		arguments = [path_to_PreparePDF, '-input', self.filename, '-output', outfilename, '-debug', str(int(debug)), '-startpage', str(startpage), '-title', self.title, '-author', self.short_authors_string()]
		if not copyright:
			if self.doi:
				arguments.append('-doi')
				arguments.append(self.doi)
				arguments.append('-copyright')
				arguments.append(os.path.join(path_of_PreparePDF, 'copyright2.pdf'))
			else:
				arguments.append('-copyright')
				arguments.append('none')
		process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = process.communicate()
		returncode = process.returncode
		sys.stderr.write(stderr)
		if returncode != 0:
			return -1
		new_start_page = int(stdout)
		self.page_count = new_start_page - start_page
		return new_start_page
	
def make_submission_from_row(row, directory):
	session = int(row['Session'])
	order_in_session = int(row['Order in session'])
	order = session * 100 + order_in_session
	authors = []
	contact_author = row['Contact given name'] + ' ' + row['Contact family name'] + ' <' + row['Contact Email'] + '>'
	end_of_authors = False
	while not end_of_authors:
		author = make_author_from_submission_row(row, len(authors) + 1)
		if author != None:
			authors.append(author)
		else:
			end_of_authors = True
	sub = Submission(row['Title'], session, order, os.path.join(directory, row['File']), authors, contact_author)
	if 'DOI' in row:
		sub.doi = row['DOI']
	return sub

if __name__ == "__main__":
	submissions = []
	author_index = dict()
	
	# Parse the arguments
	parser = argparse.ArgumentParser(description='Génère les actes depuis un répertoire doté d\'un index (index.csv) au format CSV séparé par des point-virgules.')
	parser.add_argument('source', metavar='source', help='Le répertoire source')
	parser.add_argument('--debug', action='store_true', default=False)
	parser.add_argument('--no-copyright', action='store_true', default=False)
	parser.add_argument('--no-pagination', action='store_true', default=False)
	args = parser.parse_args()
	
	# Read the CSV
	with open(args.source + '/index.csv', 'rb') as csvfile:
		csvreader = csv.DictReader(csvfile, delimiter=';')
		for row in csvreader:
			submissions.append(make_submission_from_row(row, args.source))
	
	# Prepare the PDFs, and in the meantime, prepare the author index
	start_page = 1
	for submission in submissions:
		print '- %s' % submission.title
		print 'Contact: %s' % submission.contact_author
		submission.start_page = start_page
		new_start_page = submission.prepare_pdf(start_page, args.debug, not args.no_copyright, not args.no_pagination)
		for author in submission.authors:
			name = author.lastname + " " + author.firstname
			if name in author_index:
				author_index[name].append(start_page)
			else:
				author_index[name] = [start_page]
		start_page = new_start_page
		print '\n'
	
	# Display the table of contents
	print '\nTable of contents:'
	for submission in submissions:
		print '%d\t%s (%s)' % (submission.start_page, submission.title, submission.short_authors_string())
	
	# Display the author index
	print '\nAuthor index:'
	letter = ''
	for author, pages in sorted(author_index.items(), key=lambda kv: kv[0]):
		new_letter = author.upper()[0]
		if new_letter != letter:
			print '\n' + new_letter
		print author + ', ' + ', '.join([str(page) for page in pages])
		letter = new_letter
