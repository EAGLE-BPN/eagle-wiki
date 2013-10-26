# -*- coding: utf-8 -*-

# Importing Ubi Erat Lupa monuments
# XML: http://www.ubi-erat-lupa.org/eagle/monuments.xml.php
# Guide: http://www.ubi-erat-lupa.org/eagle/

import pywikibot, re
import xml.etree.ElementTree as ET

FILE_PATH = '/Users/pietro/Dropbox/Dati/UbiEratLupa.xml'

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
	
	tree = ET.parse(FILE_PATH)
	root = tree.getroot()
	
	for m in root.findall('monument'):
		id = m.find('id').text
		if startsWith:
			if id != startsWith:
				continue # Skips monuments until start
			elif id == startsWith:
				startsWith = False # Resets
		
		# ID
		pywikibot.output("\n>>>>> " + id + " <<<<<\n")
		
		# Title
		title = m.find('title').text
		pywikibot.output('Title: ' + title)
		
		# Translation DE:
		transElem = m.find('./inscription/translation')
		if transElem is not None:
			translation = elementText(transElem)
			pywikibot.output('DE translation: ' + translation)
		else:
			translation = None
			pywikibot.output('WARNING: no translation found for ID: ' + id + '.')
		
		# Publication title
		pubTitle = 'Ubi Erat Lupa'
		pywikibot.output('Publication title: ' + pubTitle)
		
		pywikibot.output('') # newline
		
		if not always:
			choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All'], ['y', 'N', 'a'], 'N')
		else:
			choice = 'y'
		if choice in ['A', 'a']:
			always = True
			choice = 'y'
		if not dryrun and choice in ['Y', 'y']:
			page = pywikibot.ItemPage.createNew(site, labels={'en': id, 'de': id}, descriptions={'de': title})
			
			addClaimToItem(site, page, 'P34', id)
			
			transClaim = pywikibot.Claim(site, 'P12')
			transClaim.setTarget(translation)
			page.addClaim(transClaim)
			
			pubClaim = pywikibot.Claim(site, 'P26')
			pubClaim.setTarget(pubTitle)
			
			transClaim.addSources([pubClaim])

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

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()