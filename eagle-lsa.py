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

import pywikibot, re, os
from bs4 import BeautifulSoup

DATA_FOLDER = '/Users/pietro/EAGLE-data/LSA-processed/'
IPR = 'University of Oxford'
PUBLISHER = 'Last Statue of Antiquities'
YEAR = '2012'
SEPARE_REFS = '$$##$$'

def main():
	always = dryrun = startsWith = False
	
	# Handles command-line arguments for pywikibot.
	for arg in pywikibot.handleArgs():
		if arg == '-dry': # Performs a dry run (does not edit site)
			dryrun = True
		if arg == '-always': # Does not ask for confirmation
			always = True
		if arg.startswith('-start:'): # Label, for example: -start:UBBVarga000001
			startsWith = arg.replace('-start:', '')
	
	if not dryrun:
		# pywikibot/families/eagle_family.py
		site = pywikibot.Site('en', 'eagle').data_repository()
		commons = pywikibot.Site('commons', 'commons')
		
	# Correct "natural" file sorting
	for fileName in sorted(os.listdir(DATA_FOLDER), key=lambda path: int(re.search('LSA-(\d+)\.txt', path).group(1))):
		if startsWith:
			if fileName != startsWith + '.txt':
				continue # Skips files until start
			elif fileName == startsWith + '.txt':
				startsWith = False # Resets
		
		data = {} # Resets element info
		with open(DATA_FOLDER + fileName, 'r') as f:
			htmlText = f.read()
		
		htmlText = htmlText.replace('<br><br>', SEPARE_REFS) # only way to divide references
		soup = BeautifulSoup(htmlText)
	
		tabletop = soup.table.find('tr', class_='tabletop')
		contentTable = soup.table.find('table', id='table')
	
		data['id'] = elementText(tabletop.find_all('td')[0])
		pywikibot.output("\n>>>>> " + data['id'] + " <<<<<\n")
	
		data['description'] = elementText(tabletop.find_all('td')[1])
		
		refTd = contentTable.find_all('tr')[14].td
		
		# Splits references and removes whitespace
		refs = map(lambda x: x.strip(), elementText(refTd).split(SEPARE_REFS))
		
		data['label'] = refs[0] # The first reference is the label
		data['references'] = []
		for r in refs:
			if r == '':
				continue
			data['references'].append(r)
			
		# Translation
		data['translationEn'] = elementText(contentTable.find_all('tr')[16].find_all('td', class_='tabletextdata')[1])
		
		# Skips items with missing translation
		if data['translationEn'] == '':
			pywikibot.output('WARNING: no translation for ' + data['id'] + '. Skipping.')
			continue
	
		# Fixed data
		data['ipr'] = IPR
		data['publisher'] = PUBLISHER
		data['year'] = YEAR
	
		pywikibot.output('Label: ' + data['label'])
		pywikibot.output('Description: ' + data['description'])
		pywikibot.output('Translation EN: ' + data['translationEn'])
		pywikibot.output('IPR: ' + data['ipr'])
		pywikibot.output('Publisher: ' + data['publisher'])
		pywikibot.output('Year: ' + data['year'])
		pywikibot.output('References:')
		for i, r in enumerate(data['references']):
			pywikibot.output('\t#' + str(i) + ': ' + r)
	
		pywikibot.output('') # newline

		choice = None
		while choice is None:
			if not always:
				choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All'], ['y', 'N', 'a'], 'N')
			else:
				choice = 'y'
			if choice in ['A', 'a']:
				always = True
				choice = 'y'

		if not dryrun and choice in ['Y', 'y']:
			try:
				page = pywikibot.ItemPage(site)
				page.editEntity({'labels':{'en': data['label']}, 'descriptions':{'en': data['description']}})
				page.get()
			
				addClaimToItem(site, page, 'P47', data['id'])
				addClaimToItem(site, page, 'P25', data['ipr'])
		
				transClaim = pywikibot.Claim(site, 'P11')
				transClaim.setTarget(data['translationEn'])
				page.addClaim(transClaim)
		
				sources = []
		
				publisherClaim = pywikibot.Claim(site, 'P41')
				publisherClaim.setTarget(data['publisher'])
				sources.append(publisherClaim)
		
				yearClaim = pywikibot.Claim(site, 'P29')
				yearClaim.setTarget(data['year'])
				sources.append(yearClaim)
			
				for ref in data['references']:
					refClaim = pywikibot.Claim(site, 'P54')
					refClaim.setTarget(ref)
					sources.append(refClaim)
		
				transClaim.addSources(sources)
			
			except pywikibot.data.api.APIError as e:
				pywikibot.output(e)

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