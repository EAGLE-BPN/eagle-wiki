# -*- coding: utf-8 -*-

import pywikibot, os, webbrowser, re
from bs4 import BeautifulSoup

DATA_DIR = '/Users/pietro/EAGLE-data/rib/'
INDEX_FILE = 'doclist.xml'
BASE_URL = 'http://romaninscriptionsofbritain.org/rib/inscriptions/'

def main():
	always = dryrun = startsWith = False
	
	# Handles command-line arguments for pywikibot.
	for arg in pywikibot.handleArgs():
		if arg == '-dry': # Performs a dry run (does not edit site)
			dryrun = True
		if arg == '-always': # Does not ask for confirmation
			always = True
		if arg.startswith('-start:'): # Example: -start:rib02356
			startsWith = arg.replace('-start:', '')
	
	if not dryrun:
		# pywikibot/families/eagle_family.py
		site = pywikibot.Site('en', 'eagle').data_repository()
	
	# Process index file to get the list of files
	soup = BeautifulSoup(open(DATA_DIR + INDEX_FILE))
	resources = soup.list.find_all('resource')
	fileList = []
	for r in resources:
		fileList.append(r['filename'])
	
	for fileName in fileList:
		data = {} # Resets element info
		
		if startsWith:
			if fileName != startsWith + '.xml':
				continue # Skips files until start
			else:
				startsWith = False # Resets
		
		soup = BeautifulSoup(open(DATA_DIR + fileName))
		
		# Label
		data['label'] = elementText(soup.teiheader.filedesc.titlestmt.title)
		
		pywikibot.output("\n>>>>> " + data['label'] + " <<<<<\n")
		pywikibot.output('Processing file ' + DATA_DIR + fileName)
		pywikibot.output('Label: ' + data['label'])
		
		# Translation EN:
		transElem = soup.find('div', type='translation')
		if transElem:
			data['translationEn'] = elementText(transElem)
			if data['translationEn'] != '':
				pywikibot.output('EN translation: ' + data['translationEn'])
			else:
				pywikibot.output('WARNING: empty translation found! Skipping...')
				continue
		else:
			pywikibot.output('WARNING: no translation found! Skipping...')
			continue
		
		# Description
		#data['description'] = elementText(soup)
		#pywikibot.output('Description: ' + data['description'])
		
		# ID and URL
		data['rib_id'] = elementText(soup.teiheader.filedesc.publicationstmt.find('idno', type='rib'))
		data['url'] = BASE_URL + data['rib_id']
		pywikibot.output('RIB ID: ' + data['rib_id'])
		pywikibot.output('URL: ' + data['url'])
		
		# IPR (License)
		licenseItem = soup.teiheader.filedesc.publicationstmt.licence
		data['ipr'] = elementText(licenseItem) + ' ' + licenseItem['target']
		pywikibot.output('IPR: ' + data['ipr'])
		
		bibl = soup.teiheader.filedesc.sourcedesc.bibl
		
		# Publication title
		data['pubTitle'] = elementText(bibl.title)
		pywikibot.output('Publication title: ' + data['pubTitle'])
		
		# Publication place
		data['pubPlace'] = elementText(bibl.pubplace)
		pywikibot.output('Publication place: ' + data['pubPlace'])
		
		# Publisher
		data['publisher'] = elementText(bibl.publisher)
		pywikibot.output('Publisher: ' + data['publisher'])
		
		# Volume
		data['volume'] = elementText(bibl.find('biblscope', unit='vol'))
		pywikibot.output('Volume: ' + data['volume'])
		
		# Pages
		data['pages'] = elementText(bibl.find('biblscope', unit='pp'))
		pywikibot.output('Pages: ' + data['pages'])
		
		# Year
		data['year'] = elementText(bibl.date)
		pywikibot.output('Year: ' + data['year'])
		
		# Authors
		authors = soup.teiheader.filedesc.sourcedesc.bibl.find_all('author')
		data['authors'] = []
		for au in authors:
			data['authors'].append(elementText(au))
		pywikibot.output('Authors: ' + ', '.join(data['authors']))
		
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
			page.editEntity({'labels': {'en': data['label']}})
			page.get()
			
			ribidClaim = pywikibot.Claim(site, 'P63')
			ribidClaim.setTarget(data['rib_id'])
			page.addClaim(ribidClaim)
			
			urlClaim = pywikibot.Claim(site, 'P52')
			urlClaim.setTarget(data['url'])
			ribidClaim.addSource(urlClaim)
			
			addClaimToItem(site, page, 'P25', data['ipr'])
			
			transClaim = pywikibot.Claim(site, 'P11')
			transClaim.setTarget(data['translationEn'])
			page.addClaim(transClaim)
			
			sources = []
			
			for i in data['authors']:
				transAuthorClaim = pywikibot.Claim(site, 'P21')
				transAuthorClaim.setTarget(i)
				sources.append(transAuthorClaim)
			
			pubClaim = pywikibot.Claim(site, 'P26')
			pubClaim.setTarget(data['pubTitle'])
			sources.append(pubClaim)
			
			volumeClaim = pywikibot.Claim(site, 'P27')
			volumeClaim.setTarget(data['volume'])
			sources.append(volumeClaim)
			
			pagesClaim = pywikibot.Claim(site, 'P30')
			pagesClaim.setTarget(data['pages'])
			sources.append(pagesClaim)
			
			pubPlaceClaim = pywikibot.Claim(site, 'P28')
			pubPlaceClaim.setTarget(data['pubPlace'])
			sources.append(pubPlaceClaim)
			
			publisherClaim = pywikibot.Claim(site, 'P41')
			publisherClaim.setTarget(data['publisher'])
			sources.append(publisherClaim)
			
			yearClaim = pywikibot.Claim(site, 'P29')
			yearClaim.setTarget(data['year'])
			sources.append(yearClaim)
			
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
	text = re.sub('\n', ' ', text)
	text = re.sub('\s{2,}', ' ', text)
	return text
	

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()