# -*- coding: utf-8 -*-

import pywikibot, re, os
from bs4 import BeautifulSoup

DATA_FOLDER = '/Users/pietro/EAGLE-data/DAI/'
AUTHOR = 'Arachne - Deutsches Archäologisches Institut'
IPR = 'CC0'

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
		
	# Correct "natural" file sorting
	for fileName in sorted(os.listdir(DATA_FOLDER)):
		soup = BeautifulSoup(open(DATA_FOLDER + fileName, 'r'))
		inscriptions = soup.find_all('crm:e34_inscription')
		
		for item in inscriptions:
			data = {} # Resets element info
			data['dai_id'] = item['rdf:about'].split('/')[-1]
			
			if startsWith:
				if data['dai_id'] != startsWith:
					continue # Skips files until start
				elif data['dai_id'] == startsWith:
					startsWith = False # Resets
			
			pywikibot.output("\n>>>>> " + data['dai_id'] + " <<<<<\n")
			
			# Label
			data['label'] = ''
			if item.find('crm:p48_has_preferred_identifier') and item.find('crm:p48_has_preferred_identifier').find('crm:e42_identifier'):
				data['label'] = elementText(item.find('crm:p48_has_preferred_identifier').find('crm:e42_identifier').find('rdf:value'))
			if(not data['label']):
				data['label'] = data['dai_id'] # fallback
			
			# Description
			descriptionTag = item.find('crm:p128i_is_carried_by')
			if descriptionTag:
				data['description'] = descriptionTag['rdf:resource']
			else:
				pywikibot.output('WARNING: no description!');
				data['description'] = ''
			
			# Translation DE
			if item.find('crm:p73_has_translation'):
				data['translation_de'] = elementText(item.find('crm:p73_has_translation').find('crm:e33_linguistic_object').find('rdf:value'))
			else:
				data['translation_de'] = ''
				pywikibot.output('WARNING: no translation!')
				continue
			
			# References
			if item.find('crm:p70i_is_documented_in'):
				data['references'] = item.find('crm:p70i_is_documented_in').find('crm:e31_document')['rdf:about']
			else:
				data['references'] = ''
				pywikibot.output('WARNING: no references found!')
			
			# Fixed data
			data['author'] = AUTHOR
			data['ipr'] = IPR
			
			pywikibot.output('Label: ' + data['label'])
			pywikibot.output('Description: ' + data['description'])
			pywikibot.output('Translation DE: ' + data['translation_de'])
			pywikibot.output('Author: ' + data['author'])
			pywikibot.output('IPR: ' + data['ipr'])
			pywikibot.output('References: ' + data['references'])
	
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
				page = pywikibot.ItemPage.createNew(site,\
					labels={'en': data['label']},\
					descriptions={'en': data['description']})
		
				addClaimToItem(site, page, 'P35', data['dai_id'])
				addClaimToItem(site, page, 'P25', data['ipr'])
		
				transClaim = pywikibot.Claim(site, 'P12')
				transClaim.setTarget(data['translation_de'])
				page.addClaim(transClaim)
		
				sources = []
		
				publisherClaim = pywikibot.Claim(site, 'P21')
				publisherClaim.setTarget(data['author'])
				sources.append(publisherClaim)
			
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