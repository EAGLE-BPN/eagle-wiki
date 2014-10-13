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

import pywikibot, os, csv, webbrowser, re
from bs4 import BeautifulSoup

DATA_DIR = '/Users/pietro/EAGLE-data/Petrae/'

def main():
	always = dryrun = startsWith = False
	
	# Handles command-line arguments for pywikibot.
	for arg in pywikibot.handleArgs():
		if arg == '-dry': # Performs a dry run (does not edit site)
			dryrun = True
		if arg == '-always': # Does not ask for confirmation
			always = True
		if arg.startswith('-start:'): # Example: -start:160100200005
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
		
		soup = BeautifulSoup(open(DATA_DIR + fileName))
		
		# Label and description
		data['description'] = elementText(soup.find('title'))
		data['petrae_id'] = elementText(soup.find('idno', type=False))
		data['label'] = data['petrae_id']
		
		pywikibot.output("\n>>>>> " + data['label'] + " <<<<<\n")
		pywikibot.output('Label: ' + data['label'])
		pywikibot.output('Description: ' + data['description'])
		pywikibot.output('Petrae ID: ' + data['petrae_id'])
		
		data['url'] = elementText(soup.find('idno', type='URI'))
		pywikibot.output('URL: ' + data['url'])
		
		# IPR (License)
		licenseTag = soup.find('licence')
		data['ipr'] = elementText(licenseTag) + ' ' + licenseTag['target']
		pywikibot.output('IPR: ' + data['ipr'])
		
		# Translation FR:
 		transElem = soup.find('div', type='translation').find('p')
		data['translationFr'] = elementText(transElem)
		if data['translationFr'] == '':
			pywikibot.output('WARNING: no translation! Skipping...')
			continue
 		pywikibot.output('FR translation: ' + data['translationFr'])
		
		# References
		refElem = soup.find('div', type='bibliography').find('p')
		data['references'] = elementText(refElem)
		if data['references'] != '':
			pywikibot.output('References: ' + data['references'])
			
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
			page.editEntity({'labels':{'en': data['label'], 'fr': data['label']}, 'descriptions':{'fr': data['description']}})
			page.get()
			
			idClaim = pywikibot.Claim(site, 'P33')
			idClaim.setTarget(data['petrae_id'])
			page.addClaim(idClaim)
			
			addClaimToItem(site, page, 'P25', data['ipr'])
			
			transClaim = pywikibot.Claim(site, 'P15')
			transClaim.setTarget(data['translationFr'])
			page.addClaim(transClaim)
			
			sources = []
			
			if data['references'] != '':
				refClaim = pywikibot.Claim(site, 'P54')
				refClaim.setTarget(data['references'])
				sources.append(refClaim)
			
			transClaim.addSources(sources)

def addClaimToItem(site, page, id, value):
	"""Adds a claim to an ItemPage."""
	claim = pywikibot.Claim(site, id)
	claim.setTarget(value)
	page.addClaim(claim)


def elementText(elem):
	text = elem.get_text(' ', strip=True)
	text = re.sub('[\n\t]', ' ', text)
	text = re.sub(' {2,}', ' ', text)
	return text

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()