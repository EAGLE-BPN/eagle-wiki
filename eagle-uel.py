# -*- coding: utf-8 -*-
"""

Importing Ubi Erat Lupa monuments
XML: http://www.ubi-erat-lupa.org/eagle/monuments.xml.php
Guide: http://www.ubi-erat-lupa.org/eagle/

Accepted options:

	-dry
		Dry run: don't edit the wiki, but process and print all the data.
		It's useful together with -always to check for crashes in the script before launching the bot.
		
	-always
		Don't ask for confirmation before submitting a new item to the wiki.
		
	-start:<uel_id>
		Start from item whose UEL id is <uel_id>. Useful for resuming an interrupted import.

"""

import pywikibot, re
import xml.etree.ElementTree as ET

FILE_PATH = 'EAGLE-data/UbiEratLupa.xml'
IPR = 'CC0'

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
		if not title:
			pywikibot.output('WARNING: no title found for ID: ' + id + '. Skipping.')
			continue
		
		pywikibot.output('Title: ' + title)
		
		# Translation DE:
		transElem = m.find('./inscription/translation')
		if transElem is not None:
			translation = elementText(transElem)
		else:
			pywikibot.output('WARNING: no translation found for ID: ' + id + '. Skipping.')
			continue
		
		# (Heuristic) Splits author info from translation text
		author = None
		authorReg = re.compile(ur' (?:Translated by|Übersetzung): ?(.*)$', re.IGNORECASE | re.DOTALL)
		authMatch = authorReg.search(translation)
		if authMatch:
			author = authMatch.group(1)
			pywikibot.output('Author: ' + author)
			# Removes author from translation
			translation = authorReg.sub('', translation)
		
		pywikibot.output('DE translation: ' + translation)	
		
		# Publication title
		pubTitle = 'Ubi Erat Lupa'
		pywikibot.output('Publication title: ' + pubTitle)
		
		# IPR
		ipr = IPR
		pywikibot.output('IPR: ' + ipr)
		
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
			page.editEntity({'labels': {'en': id, 'de': id}, 'descriptions': {'de':title}})
			page.get()
			
			addClaimToItem(site, page, 'P34', id)
			addClaimToItem(site, page, 'P25', ipr)
			
			transClaim = pywikibot.Claim(site, 'P12')
			transClaim.setTarget(translation)
			page.addClaim(transClaim)
			
			sources = []
			
			pubClaim = pywikibot.Claim(site, 'P26')
			pubClaim.setTarget(pubTitle)
			sources.append(pubClaim)
			
			if author is not None:
				authorClaim = pywikibot.Claim(site, 'P21')
				authorClaim.setTarget(author)
				sources.append(authorClaim)
		
			transClaim.addSources(sources)

def addClaimToItem(site, page, id, value):
	"""Adds a claim to an ItemPage."""
	claim = pywikibot.Claim(site, id)
	claim.setTarget(value)
	page.addClaim(claim)

def elementText(elem):
	"""Gets inner element text, stripping tags of sub-elements."""
	text = ''.join(elem.itertext()).strip()
	text = re.sub('(\n|\t)', ' ', text)
	text = re.sub('\s{2,}', ' ', text)
	return text

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()