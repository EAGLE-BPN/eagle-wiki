# -*- coding: utf-8 -*-

import pywikibot, os, csv, webbrowser, re
from bs4 import BeautifulSoup

DATA_DIR = '/Users/pietro/Downloads/AIO/data/'
CSVFILE = '/Users/pietro/Downloads/AIO/AIO.csv'

LICENSE = 'Creative Commons Attribution-ShareAlike 3.0 http://creativecommons.org/licenses/by-sa/3.0/'
AUTHOR = 'Stephen Lambert'
PUB_TITLE = 'Attic Inscriptions Online'
BASE_URL = 'http://www.atticinscriptions.com/inscription/'

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
		data['label'] = elementText(soup.find('aside').find_all('p')[1])
		
		pywikibot.output("\n>>>>> " + data['label'] + " <<<<<\n")
		pywikibot.output('Processing file ' + DATA_DIR + fileName)
		pywikibot.output('Label: ' + data['label'])
		pywikibot.output('Description: ' + data['description'])
		
		# URL
		data['aioid'] = urlDict[fileName]
		pywikibot.output('AIO ID: ' + data['aioid'])
		
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
				webbrowser.open(BASE_URL + data['aioid'])
				choice = None # Re-ask
		
		if not dryrun and choice in ['Y', 'y']:
			page = pywikibot.ItemPage.createNew(site, labels={'en': data['label']}, descriptions={'en': data['description']})
			
			addClaimToItem(site, page, 'P51', data['aioid'])
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

def replaceSuperscript(text):
	superRep = [
		(u'1', u'¹'),
		(u'2', u'²'),
		(u'3', u'³'),
		(u'4', u'⁴'),
		(u'5', u'⁵'),
		(u'6', u'⁶'),
		(u'7', u'⁷'),
		(u'8', u'⁸'),
		(u'9', u'⁹'),
		(u'0', u'⁰'),
	]
	for i in superRep:
		text = text.replace(i[0], u'%sup%' + i[1])
	return text

def elementText(elem):
	sups = elem.find_all('sup')
	for i in sups:
		i.replaceWith(replaceSuperscript(i.string))
	text = elem.get_text(' ', strip=True)
	text = text.replace(u' %sup%', '')
	return text

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()