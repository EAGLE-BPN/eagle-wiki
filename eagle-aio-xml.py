# -*- coding: utf-8 -*-

"""

Accepted options:

	-dry
		Dry run: don't edit the wiki, but process and print all the data.
		It's useful together with -always to check for crashes in the script before launching the bot.
		
	-always
		Don't ask for confirmation before submitting a new item to the wiki.
		
	-start:<filename>
		Start from file "<filename>.xml". Useful for resuming an interrupted import.

"""

import pywikibot, os, webbrowser, re
from bs4 import BeautifulSoup

DATA_DIR = 'EAGLE-data/AIO/data-new/'

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
		
	for fileName in os.listdir(DATA_DIR):
		data = {} # Resets element info
		
		if startsWith:
			if fileName != startsWith + '.xml':
				continue # Skips files until start
			else:
				startsWith = False # Resets
		
		soup = BeautifulSoup(open(DATA_DIR + fileName))
		
		# Label and description
		data['label'] = elementText(soup.translation_source)
		data['description'] = elementText(soup.root.translation_title)
		
		pywikibot.output("\n>>>>> " + data['label'] + " <<<<<\n")
		pywikibot.output('Processing file ' + DATA_DIR + fileName)
		pywikibot.output('Label: ' + data['label'])
		pywikibot.output('Description: ' + data['description'])
		
		# ID and URL
		data['aioid'] = elementText(soup.aio_key).split('_')[1]
		data['url'] = 'http://' + elementText(soup.url)
		pywikibot.output('AIO ID: ' + data['aioid'])
		pywikibot.output('URL: ' + data['url'])
		
		# IPR (License)
		data['ipr'] = LICENSE
		pywikibot.output('IPR: ' + data['ipr'])
		
		# Translation EN:
		data['translationEn'] = elementText(soup.translation)
		pywikibot.output('EN translation: ' + data['translationEn'])
		
		# Publication author
		data['pubAuthor'] = AUTHOR
		pywikibot.output('Publication author: ' + data['pubAuthor'])
		
		# Translation author
		authors = soup.translators.find_all('item')
		data['transAuthors'] = []
		for i in authors:
			authorName = elementText(i)
			data['transAuthors'].append(authorName)
			pywikibot.output('Translation author: ' + authorName)
		
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
			page = pywikibot.ItemPage(site)
			page.editEntity({'labels':{'en': data['label']}, 'descriptions':{'en': data['description']}})
			page.get()
			
			aioidClaim = pywikibot.Claim(site, 'P51')
			aioidClaim.setTarget(data['aioid'])
			page.addClaim(aioidClaim)
			
			urlClaim = pywikibot.Claim(site, 'P52')
			urlClaim.setTarget(data['url'])
			aioidClaim.addSource(urlClaim)
			
			addClaimToItem(site, page, 'P25', data['ipr'])
			
			transClaim = pywikibot.Claim(site, 'P11')
			transClaim.setTarget(data['translationEn'])
			page.addClaim(transClaim)
			
			sources = []
			
			for i in data['transAuthors']:
				transAuthorClaim = pywikibot.Claim(site, 'P21')
				transAuthorClaim.setTarget(i)
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
	# We need to re-parse the XML in translation_source and translation_title because it's escaped.
	soup = BeautifulSoup(elem.get_text(' ', strip=True))
	
	sups = soup.find_all('sup')
	for i in sups:
		i.replaceWith(replaceSuperscript(i.string))
	text = soup.get_text(' ', strip=True)
	text = text.replace(u' %sup%', '')
	text = re.sub('\n', ' ', text)
	text = re.sub('\s{2,}', ' ', text)
	return text

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()