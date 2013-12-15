# -*- coding: utf-8 -*-

import pywikibot, os, csv, webbrowser, re
from bs4 import BeautifulSoup

DATA_DIR = '/Users/pietro/Downloads/AIO/data/'
CSVFILE = '/Users/pietro/Downloads/AIO/AIO.csv'

LICENSE = 'Creative Commons Attribution-ShareAlike 3.0 http://creativecommons.org/licenses/by-sa/3.0/'
AUTHOR = 'Stephen Lambert'
PUB_TITLE = 'Attic Inscriptions Online'

def main():
	always = dryrun = startsWith = False
	
	# Handles command-line arguments for pywikibot.
	for arg in pywikibot.handleArgs():
		if arg == '-dry': # Performs a dry run (does not edit site)
			dryrun = True
		if arg == '-always': # Does not ask for confirmation
			always = True
		if arg.startswith('-start:'): # Example: -start:57
			startsWith = arg.replace('-start:', '')
	
	if not dryrun:
		# pywikibot/families/eagle_family.py
		site = pywikibot.Site('en', 'eagle').data_repository()
	
	transAuthorRegex = re.compile('^Translation by:')
	
	urlDict = {}
	with open(CSVFILE, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			urlDict[row[0]] = row[1]
		
	for fileName in os.listdir(DATA_DIR):
		data = {} # Resets element info
		
		if startsWith:
			if fileName != startsWith:
				continue # Skips files until start
			elif fileName == startsWith:
				startsWith = False # Resets
		
		soup = BeautifulSoup(open(DATA_DIR + fileName))
		
		# Label and description
		data['description'] = elementText(soup.find('h3'))
		data['label'] = elementText(soup.find('h4'))
		
		pywikibot.output("\n>>>>> " + data['label'] + " <<<<<\n")
		pywikibot.output('Processing file ' + DATA_DIR + fileName + '.')
		pywikibot.output('Label: ' + data['label'])
		pywikibot.output('Description: ' + data['description'])
		
		# URL
		data['url'] = urlDict[fileName]
		pywikibot.output('URL: ' + data['url'])
		
		# IPR (License)
		data['ipr'] = LICENSE
		pywikibot.output('IPR: ' + data['ipr'])
		
		# Translation EN:
		transElem = soup.find('div', id='inscription')
		
		data['translationEn'] = elementText(transElem)
		pywikibot.output('EN translation: ' + data['translationEn'])
		
		# Publication author
		data['pubAuthor'] = AUTHOR
		pywikibot.output('Publication author: ' + data['pubAuthor'])
		
		# Translation author
		data['transAuthor'] = elementText(soup.find('aside')\
			.find('p', text=transAuthorRegex))\
			.replace('Translation by: ', '')
		pywikibot.output('Translation author: ' + data['transAuthor'])
		
		# Publication title
		data['pubTitle'] = PUB_TITLE
		pywikibot.output('Publication title: ' + data['pubTitle'])
		
		pywikibot.output('') # newline
		
		choice = None
		while choice is None:
			if not always:
				choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All', 'open in browser'], ['y', 'N', 'a', 'b'], 'N')
			else:
				choice = 'y'
			if choice in ['A', 'a']:
				always = True
				choice = 'y'
			elif choice in ['B', 'b']:
				webbrowser.open(data['url'])
				choice = None # Re-ask
		
		if not dryrun and choice in ['Y', 'y']:
			page = pywikibot.ItemPage.createNew(site, labels={'en': data['label']}, descriptions={'en': data['description']})
			
			addClaimToItem(site, page, 'P51', data['url'])
			addClaimToItem(site, page, 'P25', data['ipr'])
			
			transClaim = pywikibot.Claim(site, 'P11')
			transClaim.setTarget(data['translationEn'])
			page.addClaim(transClaim)
			
			sources = []
			
			transAuthorClaim = pywikibot.Claim(site, 'P21')
			transAuthorClaim.setTarget(data['transAuthor'])
			sources.append(transAuthorClaim)
			
			pubAuthorClaim = pywikibot.Claim(site, 'P46')
			pubAuthorClaim.setTarget(data['pubAuthor'])
			sources.append(pubAuthorClaim)
			
			pubClaim = pywikibot.Claim(site, 'P26')
			pubClaim.setTarget(data['pubTitle'])
			sources.append(pubClaim)
			
			transClaim.addSources(sources)

def addClaimToItem(site, page, id, value):
	"""Adds a claim to an ItemPage."""
	claim = pywikibot.Claim(site, id)
	claim.setTarget(value)
	page.addClaim(claim)

def elementText(elem):
	return elem.get_text(' ', strip=True)

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()