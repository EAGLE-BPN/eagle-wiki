# -*- coding: utf-8 -*-

"""

Accepted options:

	-dry
		Dry run: don't edit the wiki, but process and print all the data.
		It's useful together with -always to check for crashes in the script before launching the bot.
		
	-always
		Don't ask for confirmation before submitting a new item to the wiki.
		
	-start:<label>
		Start from item whose label is <label>. Useful for resuming an interrupted import.

"""

import pywikibot, re
from bs4 import BeautifulSoup

FILE_PATH = 'EAGLE-data/ubbeagleALL.xml'
AUTHORITY = 'Universitatea Babeş-Bolyai'

def main():
	always = dryrun = startsWith = False
	edhRegex = re.compile('\s*(HD\d+)[\s.]*')
	
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
		
	soup = BeautifulSoup(open(FILE_PATH))
	for xml_item in soup.ubb.find_all('tei'):
		data = {} # Resets element info
		
		# Label and description
		url = xml_item.teiheader.filedesc.publicationstmt.find('idno', {'type': 'URI'}).get_text()
		match = re.search('/([^/]*?)/([^/]*?)/(\d+)\.xml$', url)
		data['label'] = match.group(1) + match.group(2) + match.group(3)
		
		if startsWith:
			if data['label'] != startsWith:
				continue # Skips files until start
			elif data['label'] == startsWith:
				startsWith = False # Resets
		
		pywikibot.output("\n>>>>> " + data['label'] + " <<<<<\n")
		
		# UBB Identifier
		data['ubb'] = url
		pywikibot.output("UBB identifier: " + data['ubb'])
		
		# Description
		data['description'] = elementText(xml_item.teiheader.profiledesc.textclass.keywords.term)
		pywikibot.output("Description: " + data['description'])
		
		# Translation
		try:
			data['translation'] = elementText(xml_item.find('text').body.find('div', {'type': 'translation'}).p)
		except AttributeError:
			pywikibot.output('ERROR: translation not found!')
			continue
		
		# Author
		data['author'] = elementText(xml_item.teiheader.revisiondesc.change)
		pywikibot.output("Author: " + data['author'])
		if data['author'] == 'Rada Varga':
			data['trans_lang'] = 'en'
		elif data['author'] == 'Ioan Piso':
			data['trans_lang'] = 'fr'
		else:
			pywikibot.output('ERROR! Author not recognized!')
			exit()
		
		pywikibot.output("Translation (" + data['trans_lang'].upper() + "): " + data['translation'])
		
		# IPR
		data['ipr'] = xml_item.find('text').body.find('div', {'type': 'translation'}).desc.ref['target']
		pywikibot.output("IPR: " + data['ipr'])
		
		# Publisher
		data['publisher'] = AUTHORITY
		# data['publisher'] = elementText(xml_item.teiheader.filedesc.publicationstmt.authority).title()
		pywikibot.output("Publisher: " + data['publisher'])
		
		# Process bibliography
		data['bibliography'] = []
		bibList = xml_item.find('text').body.find('div', {'type': 'bibliography'}).find_all('bibl')
		for b in bibList:
			bibText = elementText(b)
			if not bibText:
				continue
			match = edhRegex.match(bibText)
			if match:
				data['edh'] = match.group(1)
			else:
				data['bibliography'].append(bibText)
				pywikibot.output('Bib note #' + str(len(data['bibliography'])) + ': ' + bibText)
				
		if 'edh' in data:
			pywikibot.output("EDH: " + data['edh'])
		
		# Images
		data['images'] = []
		try:
			imgs = xml_item.facsimile.find_all('graphic')
			for i in imgs:
				# Wikidata only wants the image title
				img_title = i['url'].replace('https://commons.wikimedia.org/wiki/File:', '')
				data['images'].append(img_title)
				pywikibot.output('Image #' + str(len(data['images'])) + ': ' + i['url'])
		except AttributeError: # No <facsimile>
			pass
		
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
			page = pywikibot.ItemPage(site)
			page.editEntity({'labels': {'en': data['label']}, 'descriptions': {data['trans_lang']: data['description']}})
			page.get()
			
			addClaimToItem(site, page, 'P59', data['ubb'])
			addClaimToItem(site, page, 'P25', data['ipr'])
			
			if 'edh' in data:
				addClaimToItem(site, page, 'P24', data['edh'])
				
			for img_title in data['images']:
				img_page = pywikibot.ImagePage(commons, img_title)
				addClaimToItem(site, page, 'P10', img_page)
			
			if data['trans_lang'] == 'en':
				trans_property = 'P11'
			elif data['trans_lang'] == 'fr':
				trans_property = 'P15'
			transClaim = pywikibot.Claim(site, trans_property)
			transClaim.setTarget(data['translation'])
			page.addClaim(transClaim)
		
			sources = []
			
			authorClaim = pywikibot.Claim(site, 'P21')
			authorClaim.setTarget(data['author'])
			sources.append(authorClaim)
			
			publisherClaim = pywikibot.Claim(site, 'P41')
			publisherClaim.setTarget(data['publisher'])
			sources.append(publisherClaim)
			
			for b in data['bibliography']:
				bibClaim = pywikibot.Claim(site, 'P54')
				bibClaim.setTarget(b)
				sources.append(bibClaim)
		
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