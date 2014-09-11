# -*- coding: utf-8 -*-

import pywikibot, os, re, csv
import xml.etree.ElementTree as ET

DATA_DIR = '/Users/pietro/EAGLE-data/insAph/data/'

LICENSE = "Creative Commons licence Attribution 2.5 (http://creativecommons.org/licenses/by/2.5/).\
 All reuse or distribution of this work must contain somewhere a link back to the URL http://insaph.kcl.ac.uk/"

unpublished_regex = re.compile("Unpublished inscription\. This version born digital\.?")

knownPublications = {
	'ala2004': {
		'pubTitle': 'Originally published in Aphrodisias in Late Antiquity: The Late Roman and Byzantine Inscriptions (2004)', # title
		'author': 'Charlotte Roueché', # author
		'pubPlace': 'London', # place
		'year': '2004',
	}
}

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
		data = {} # Resets element info
		
		if startsWith:
			if fileName != (startsWith + '.xml'):
				continue # Skips files until start
			elif fileName == (startsWith + '.xml'):
				startsWith = False # Resets
		
		tree = ET.parse(DATA_DIR + fileName)
		root = tree.getroot()
		
		# ID
		data['insAphID'] = root.get('id')
		
		# ID
		pywikibot.output("\n>>>>> " + data['insAphID'] + " <<<<<\n")
		
		# Title
		data['title'] = elementText(root.find('./teiHeader/fileDesc/titleStmt/title'))
		pywikibot.output('Title: ' + data['title'])
		
		# IPR (License)
		data['ipr'] = LICENSE
		pywikibot.output('IPR: ' + data['ipr'])
		
		# Translation EN:
		transElem = root.find("./text/body/div[@type='translation']")
		if transElem is None:
			pywikibot.output('WARNING: no translation found for ' + data['insAphID'] + '.')
			continue # TODO: How should I handle this?
		
		normalizeTranslation(transElem)
		data['translationEn'] = elementText(transElem)
		if data['translationEn'] == '':
			pywikibot.output('WARNING: no translation. Skipping.')
			continue
		pywikibot.output('EN translation: ' + data['translationEn'])
		
		# Authors
		authors = root.findall('./teiHeader/fileDesc/publicationStmt//bibl/editor')
		data['author'] = ''
		for au in authors:
			data['author'] += elementText(au) + ', '
		data['author'] = data['author'][0:-2] # removes last comma
		
		# Date
		dateElem = root.find('./teiHeader/fileDesc/sourceDesc//bibl/date')
		if dateElem is not None:
			data['year'] = elementText(dateElem)
		
		# Publication title
		data['pubTitle'] = elementText(root.find('./teiHeader/fileDesc/sourceDesc/p'))
		
		if unpublished_regex.match(data['pubTitle']): # Born digital
			data['pubTitle'] = 'Inscriptions of Aphrodisias'
			data['year'] = '2007'
			
		
		# Known publication?
		bibl = root.find('./teiHeader/fileDesc/sourceDesc//bibl')
		if bibl is not None:
			data['publicationID'] = bibl.get('n')
			if data['publicationID'] in knownPublications.keys():
				data.update(knownPublications[data['publicationID']])
			
		pywikibot.output('Authors: ' + data['author'])
		if 'year' in data:
			pywikibot.output('Date: ' + data['year'])
		pywikibot.output('Publication title: ' + data['pubTitle'])
		if 'pubPlace' in data:
			pywikibot.output('Publication place: ' + data['pubPlace'])
		
		pywikibot.output('') # newline
		
		if not always:
			choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All'], ['y', 'N', 'a'], 'N')
		else:
			choice = 'y'
		if choice in ['A', 'a']:
			always = True
			choice = 'y'
		if not dryrun and choice in ['Y', 'y']:
			page = pywikibot.ItemPage(site)
			page.editEntity({'labels':{'en': data['insAphID']}, 'descriptions':{'en': data['title']}})
			page.get()
						
			addClaimToItem(site, page, 'P50', data['insAphID'])
			addClaimToItem(site, page, 'P25', data['ipr'])
			
			transClaim = pywikibot.Claim(site, 'P11')
			transClaim.setTarget(data['translationEn'])
			page.addClaim(transClaim)
			
			sources = []
			
			authorClaim = pywikibot.Claim(site, 'P21')
			authorClaim.setTarget(data['author'])
			sources.append(authorClaim)
			
			if data['pubTitle'] != '':
				pubClaim = pywikibot.Claim(site, 'P26')
				pubClaim.setTarget(data['pubTitle'])
				sources.append(pubClaim)
			
			if 'year' in data:		
				yearClaim = pywikibot.Claim(site, 'P29')
				yearClaim.setTarget(data['year'])
				sources.append(yearClaim)
			
			if 'pubPlace' in data:
				pubPlaceClaim = pywikibot.Claim(site, 'P28')
				pubPlaceClaim.setTarget(data['pubPlace'])
				sources.append(pubPlaceClaim)
			
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