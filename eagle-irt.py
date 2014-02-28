# -*- coding: utf-8 -*-

import pywikibot, os, re, csv
import xml.etree.ElementTree as ET

DATA_DIR = '/Users/pietro/EAGLE-data/British School of Rome/'

LICENSE = "Creative Commons licence Attribution UK 2.0 (http://creativecommons.org/licenses/by/2.0/uk/). All reuse or distribution of this work must contain somewhere a link back to the URL http://irt.kcl.ac.uk/"

def main():
	always = dryrun = startsWith = False
	
	# Handles command-line arguments for pywikibot.
	for arg in pywikibot.handleArgs():
		if arg == '-dry': # Performs a dry run (does not edit site)
			dryrun = True
		if arg == '-always': # Does not ask for confirmation
			always = True
		if arg.startswith('-start:'): # Example: -start:IRT013
			startsWith = arg.replace('-start:', '')
	
	if not dryrun:
		# pywikibot/families/eagle_family.py
		site = pywikibot.Site('en', 'eagle').data_repository()
	
	# EDH ids
	edhIds = {}
	with open('irt-edh.txt', 'r') as f:
		reader = csv.reader(f, delimiter="\t")
		for row in reader:
			edhIds[row[1]] = row[0]
	
	for fileName in os.listdir(DATA_DIR):
		if startsWith:
			if fileName != (startsWith + '.xml'):
				continue # Skips files until start
			elif fileName == (startsWith + '.xml'):
				startsWith = False # Resets
		
		tree = ET.parse(DATA_DIR + fileName)
		root = tree.getroot()
		
		# BSR
		bsr = fileName[0:-4] # Remove extension (.xml)
		
		# ID
		pywikibot.output("\n>>>>> " + bsr + " <<<<<\n")
		
		# Title
		title = elementText(root.findall('./teiHeader/fileDesc/titleStmt/title')[0])
		pywikibot.output('Title: ' + title)
		
		# Tries to guess EDH
		if bsr in edhIds:
			edh = edhIds[bsr]
		elif re.sub('[a-z]$', '', bsr) in edhIds:
			edh = edhIds[re.sub('[a-z]$', '', bsr)]
		elif bsr + 'a' in edhIds:
			edh = edhIds[bsr + 'a']
		else:
			edh = ''
			pywikibot.output('WARNING: no EDH found for ' + bsr + '.')
		
		if edh:
			pywikibot.output('EDH: ' + edh)
		
		# IPR (License)
		# ipr = elementText(root.findall('./teiHeader/fileDesc/publicationStmt/p')[0])
		# ipr = re.sub(' \(.*?\)', '', ipr)
		ipr = LICENSE
		pywikibot.output('IPR: ' + ipr)
		
		# Translation EN:
		try:
			transElem = root.findall('./text/body/div[@type=\'translation\']/p')[0]
			normalizeTranslation(transElem)
			translationEn = elementText(transElem)
			pywikibot.output('EN translation: ' + translationEn)
		except IndexError:
			pywikibot.output('WARNING: no translation found for ' + bsr + '.')
			continue # TODO: How should I handle this?
		
		# Authors
		# authors = root.findall('./teiHeader/fileDesc/titleStmt/editor')
		# authorString = ''
		# for au in authors:
		# 	authorString += au.text + ', '
		# authorString = authorString[0:-2]
		authorString = 'J. M. Reynolds'
		pywikibot.output('Authors: ' + authorString)
		
		# Publication title
		# pubTitle = elementText(root.findall('./teiHeader/fileDesc/sourceDesc//title')[0])
		pubTitle = 'IRT2009'
		pywikibot.output('PubTitle: ' + pubTitle)
		
		# Publication place
		#pubPlace = elementText(root.findall('./teiHeader/fileDesc/sourceDesc//pubPlace')[0])
		pubPlace = 'London'
		pywikibot.output('PubPlace: ' + pubPlace)
		
		# Publisher
		# publisher = elementText(root.findall('./teiHeader/fileDesc/sourceDesc//publisher')[0])
		publisher = "King's College London"
		pywikibot.output('Publisher: ' + publisher)
		
		# Date
		# year = elementText(root.findall('./teiHeader/fileDesc/sourceDesc//date')[0])
		year = '2009'
		pywikibot.output('Date: ' + year)
		
		pywikibot.output('') # newline
		
		if not always:
			choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All'], ['y', 'N', 'a'], 'N')
		else:
			choice = 'y'
		if choice in ['A', 'a']:
			always = True
			choice = 'y'
		if not dryrun and choice in ['Y', 'y']:
			page = pywikibot.ItemPage.createNew(site, labels={'en': bsr}, descriptions={'en': title})
			
			addClaimToItem(site, page, 'P40', bsr)
			if edh:
				addClaimToItem(site, page, 'P24', edh)
			addClaimToItem(site, page, 'P25', ipr)
			
			transClaim = pywikibot.Claim(site, 'P11')
			transClaim.setTarget(translationEn)
			page.addClaim(transClaim)
			
			authorClaim = pywikibot.Claim(site, 'P21')
			authorClaim.setTarget(authorString)
			
			pubClaim = pywikibot.Claim(site, 'P26')
			pubClaim.setTarget(pubTitle)
			
			pubPlaceClaim = pywikibot.Claim(site, 'P28')
			pubPlaceClaim.setTarget(pubPlace)
			
			publisherClaim = pywikibot.Claim(site, 'P41')
			publisherClaim.setTarget(publisher)
			
			yearClaim = pywikibot.Claim(site, 'P29')
			yearClaim.setTarget(year)
			
			transClaim.addSources([authorClaim, pubClaim, yearClaim, publisherClaim, pubPlaceClaim])

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