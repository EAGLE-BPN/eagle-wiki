# -*- coding: utf-8 -*-

import pywikibot, os, webbrowser, re, csv
from bs4 import BeautifulSoup

DATA_DIR = '/Users/pietro/EAGLE-data/rib/'
INDEX_FILE = 'doclist.xml'
ID_FILE = 'RIB-EDH-TM.txt'
BASE_URL = 'http://romaninscriptionsofbritain.org/rib/inscriptions/'

PUB_AUTHOR = 'Scott Vanderbilt'

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
	with open(DATA_DIR + INDEX_FILE) as indexfile:
		soup = BeautifulSoup(indexfile)
		resources = soup.list.find_all('resource')
		fileList = []
		for r in resources:
			fileList.append(r['filename'])
	
	# Process CSV files with ID mappings
	id_map = {}
	with open(DATA_DIR + ID_FILE, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter='\t')
		for row in reader:
			id_map[row[2]] = {'edh': row[0], 'tm': row[1]}
	
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
		
		# Description
		try:
			data['description'] = elementText(soup.find('text').listbibl.bibl)
			pywikibot.output('Description: ' + data['description'])
		except:
			pywikibot.output('WARNING: no description!')
		
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
		
		# Publication author
		data['pubAuthor'] = PUB_AUTHOR
		pywikibot.output('Publication author: ' + data['pubAuthor'])
		
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
		
		# TM ID
		if data['rib_id'] in id_map and id_map[data['rib_id']]['tm']:
			data['tm_id'] = id_map[data['rib_id']]['tm']
			pywikibot.output('TM ID: ' + data['tm_id'])
		
		# EDH ID
		edh_ref = soup.find('text').find('ref', target='bibA00118')
		if edh_ref:
			data['edh_id'] = elementText(edh_ref.find_next_sibling('biblscope', unit='dbid'))
			pywikibot.output('EDH ID: ' + data['edh_id'])
		elif data['rib_id'] in id_map and id_map[data['rib_id']]['edh']:
			data['edh_id'] = id_map[data['rib_id']]['edh']
			pywikibot.output('EDH ID: ' + data['edh_id'])
		
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
			
			entityData = {'labels': {'en': data['label']}}
			if 'description' in data:
				entityData['descriptions'] = {'en': data['description']}
			
			page.editEntity(entityData)
			page.get()
			
			ribidClaim = pywikibot.Claim(site, 'P63')
			ribidClaim.setTarget(data['rib_id'])
			page.addClaim(ribidClaim)
			
			pubAuthorClaim = pywikibot.Claim(site, 'P46')
			pubAuthorClaim.setTarget(data['pubAuthor'])
			ribidClaim.addSource(pubAuthorClaim)
			
			if 'edh_id' in data:
				addClaimToItem(site, page, 'P24', data['edh_id'])
			if 'tm_id' in data:
				addClaimToItem(site, page, 'P3', data['tm_id'])
			
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


def elementText(elem):
	text = elem.get_text()
	text = re.sub('\n', ' ', text)
	text = re.sub('\s{2,}', ' ', text)
	text = text.strip()
	return text


if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()