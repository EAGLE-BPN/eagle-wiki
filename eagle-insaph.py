# -*- coding: utf-8 -*-

import pywikibot, os, re, csv
import xml.etree.ElementTree as ET

DATA_DIR = '/Users/pietro/Dropbox/Dati/insaph/'

LICENSE = "Creative Commons licence Attribution 2.5 (http://creativecommons.org/licenses/by/2.5/).\
 All reuse or distribution of this work must contain somewhere a link back to the URL http://insaph.kcl.ac.uk/"

def main():
	always = dryrun = startsWith = False
	
	# Handles command-line arguments for pywikibot.
	for arg in pywikibot.handleArgs():
		if arg == '-dry': # Performs a dry run (does not edit site)
			dryrun = True
		if arg == '-always': # Does not ask for confirmation
			always = True
		if arg.startswith('-start:'): # Example: -start:iAph010004
			startsWith = arg.replace('-start:', '')
	
	if not dryrun:
		# pywikibot/families/eagle_family.py
		site = pywikibot.Site('en', 'eagle').data_repository()
	
	for fileName in os.listdir(DATA_DIR):
		if startsWith:
			if fileName != (startsWith + '.xml'):
				continue # Skips files until start
			elif fileName == (startsWith + '.xml'):
				startsWith = False # Resets
		
		tree = ET.parse(DATA_DIR + fileName)
		root = tree.getroot()
		
		# ID
		insAphID = root.get('id')
		
		# ID
		pywikibot.output("\n>>>>> " + insAphID + " <<<<<\n")
		
		# Title
		title = elementText(root.find('./teiHeader/fileDesc/titleStmt/title'))
		pywikibot.output('Title: ' + title)
		
		# IPR (License)
		# ipr = elementText(root.findall('./teiHeader/fileDesc/publicationStmt/p')[0])
		# ipr = re.sub(' \(.*?\)', '', ipr)
		ipr = LICENSE
		pywikibot.output('IPR: ' + ipr)
		
		# Translation EN:
		try:
			transElem = root.find('./text/body/div[@type=\'translation\']')
			normalizeTranslation(transElem)
			translationEn = elementText(transElem)
			pywikibot.output('EN translation: ' + translationEn)
		except IndexError:
			pywikibot.output('WARNING: no translation found for ' + insAphID + '.')
			continue # TODO: How should I handle this?
		
		# Authors
		authors = root.findall('./teiHeader/fileDesc/publicationStmt//bibl/editor')
		authorString = ''
		for au in authors:
			authorString += elementText(au) + ', '
		authorString = authorString[0:-2] # removes last comma
		pywikibot.output('Authors: ' + authorString)
		
		# Date
		year = elementText(root.find('./teiHeader/fileDesc/publicationStmt//bibl/date'))
		pywikibot.output('Date: ' + year)
		
		# Publication title
		pubTitle = elementText(root.find('./teiHeader/fileDesc/sourceDesc/p'))
		pywikibot.output('PubTitle: ' + pubTitle)
		
		# Publication place
		#pubPlace = elementText(root.findall('./teiHeader/fileDesc/sourceDesc//pubPlace')[0])
		#pubPlace = 'London'
		#pywikibot.output('PubPlace: ' + pubPlace)
		
		# Publisher
		# publisher = elementText(root.findall('./teiHeader/fileDesc/sourceDesc//publisher')[0])
		# publisher = "King's College London"
		# pywikibot.output('Publisher: ' + publisher)
		
		pywikibot.output('') # newline
		
		if not always:
			choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All'], ['y', 'N', 'a'], 'N')
		else:
			choice = 'y'
		if choice in ['A', 'a']:
			always = True
			choice = 'y'
		if not dryrun and choice in ['Y', 'y']:
			page = pywikibot.ItemPage.createNew(site, labels={'en': insAphID}, descriptions={'en': title})
			
			addClaimToItem(site, page, 'P50', insAphID)
			addClaimToItem(site, page, 'P25', ipr)
			
			transClaim = pywikibot.Claim(site, 'P11')
			transClaim.setTarget(translationEn)
			page.addClaim(transClaim)
			
			sources = []
			
			authorClaim = pywikibot.Claim(site, 'P21')
 			authorClaim.setTarget(authorString)
 			sources.append(authorClaim)
			
			pubClaim = pywikibot.Claim(site, 'P26')
			pubClaim.setTarget(pubTitle)
			sources.append(pubClaim)
# 			
# 			pubPlaceClaim = pywikibot.Claim(site, 'P28')
# 			pubPlaceClaim.setTarget(pubPlace)
# 			
# 			publisherClaim = pywikibot.Claim(site, 'P41')
# 			publisherClaim.setTarget(publisher)
# 			
 			yearClaim = pywikibot.Claim(site, 'P29')
 			yearClaim.setTarget(year)
 			sources.append(yearClaim)
			
			transClaim.addSources(sources)

def addClaimToItem(site, page, id, value):
	"""Adds a claim to an ItemPage."""
	claim = pywikibot.Claim(site, id)
	claim.setTarget(value)
	page.addClaim(claim)

def elementText(elem):
	"""Gets inner element text, stripping tags of sub-elements."""
	text = ''.join(elem.itertext()).strip()
	text = re.sub('\n', ' ', text)
	text = re.sub('\s{2,}', ' ', text)
	return text

def normalizeTranslation(elem):
	"""Processes translation text"""
	
	# <head>
	elem.find('.//head').text = ''
		
	# <gap />
	gaps = elem.findall('.//gap')
	for g in gaps:
		g.text = '[...]'
	
	# <note>
	notes = elem.findall('.//note')
	for n in notes:
		if n.text and n.text.startswith('Not usefully'): # Not usefully translat(a|ea)ble
			n.text = elementText(n)
		else:
			addBracesToElement(n, '(', ')')
	
	# <supplied>
	supplied = elem.findall('.//supplied')
	for s in supplied:
		addBracesToElement(s, '[', ']')

def addBracesToElement(elem, openBrace='(', closeBrace=')'):
	"""Encloses elem into braces."""
	if elem.text:
		elem.text = openBrace + elem.text
	else:
		elem.text = openBrace
	if elem.tail:
		elem.tail = closeBrace + elem.tail
	else:
		elem.tail = closeBrace

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()