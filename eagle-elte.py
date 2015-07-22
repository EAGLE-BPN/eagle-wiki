# -*- coding: utf-8 -*-

"""

Accepted options:
	
	-dry
		Dry run: don't edit the wiki, but process and print all the data.
		It's useful together with -always to check for crashes in the script before launching the bot.
		
	-always
		Don't ask for confirmation before submitting a new item to the wiki.
		
	-start:<bohry_id>
		Start from the item whose Bohry id is <dai_id>. Useful for resuming an interrupted import.

"""

import pywikibot, csv, re, urllib2
import xml.etree.ElementTree as ET

elteinwiki = [1, 10, 107, 11, 112, 12, 13, 14, 15, 169,  17,  17,  18,  188,  19,  192,  2,  20,  21,  22,  23,  247,  25,  256,  27,  28,  3,  31,  35,  36,  38,  39,  4,  40,  41,  42,  43,  46,  47,  48,  49,  5,  50,  53,  54,  55,  56,  57,  58,  59,  6,  60,  61,  62,  63,  65,  66,  69,  7,  71,  73,  76,  77,  78,  8,  87,  88,  89,  9]

DATA_FILE = 'EAGLE-data/elte.csv'

def main():
	always = dryrun = startsWith = False
	
	# Handles command-line arguments for pywikibot.
	for arg in pywikibot.handleArgs():
		if arg == '-dry': # Performs a dry run (does not edit site)
			dryrun = True
		if arg == '-always': # Does not ask for confirmation
			always = True
		if arg.startswith('-start:'): # Example: -start:255
			startsWith = arg.replace('-start:', '')
	
	# pywikibot/families/eagle_family.py
	site = pywikibot.Site('en', 'eagle').data_repository()
	
	f = open(DATA_FILE, 'r')
	reader = csv.reader(f, delimiter=";")
	withtrans = []
	notinwiki = []

	for row in reader:
		if row[1] != '': 
			withtrans.append(row)

	for row in withtrans:
		if row[8] != '': 
			elteid = row[8]
		else:
			elteid = re.sub('HD','', row[9])

		if int(elteid) not in elteinwiki:
			notinwiki.append(row)

	for row in notinwiki:

		if row[8] != '': 
			BorhyID = normalizeText(row[8])
		else:
			BorhyID = normalizeText(row[9])
		if startsWith:
			if BorhyID != startsWith:
				continue # Skips files until start
			elif BorhyID == startsWith:
				startsWith = False # Resets
		
		pywikibot.output("\n>>>>> " + BorhyID + " <<<<<\n")
		pywikibot.output('ELTE identifier: ' + BorhyID)
		
		translationHu = normalizeText(row[1])
		if translationHu == '':
			pywikibot.output('WARNING: no translation. Skipping.')
			continue
		pywikibot.output('Translation HU: ' + translationHu)
		
		ipr = normalizeText(row[2])
		pywikibot.output('IPR: ' + ipr)
		
		author = normalizeText(row[3])
		pywikibot.output('Author: ' + author)
		
		pubTitle = normalizeText(row[4])
		pywikibot.output('Publication title: ' + pubTitle)
		
		year = normalizeText(row[5])
		pywikibot.output('Year: ' + year)
		
		place = normalizeText(row[6])
		pywikibot.output('Publication place: ' + place)
		
		publisher = normalizeText(row[7])
		pywikibot.output('Publisher: ' + publisher)
		
		edh = normalizeText(row[9])
		if edh:
			pywikibot.output('EDH: ' + edh)
		else:
			pywikibot.output('WARNING: no EDH!')
		
		data = {}
		if edh:
			data = getDataFromEDH(edh)
			pywikibot.output('Description: ' + data['description'])
		
		pywikibot.output('') # newline
		
		if not always:
			choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All'], ['y', 'N', 'a'], 'N')
		else:
			choice = 'y'
		if choice in ['A', 'a']:
			always = True
			choice = 'y'
		if not dryrun and choice in ['Y', 'y']:
			descriptions = {}
			if 'description' in data:
				descriptions['de'] = data['description']
			
			page = pywikibot.ItemPage(site)
			page.editEntity({'labels':{'en': BorhyID}, 'descriptions':descriptions})
			page.get()
		
			# HU translation
			transClaim = pywikibot.Claim(site, 'P19')
			transClaim.setTarget(translationHu)
			page.addClaim(transClaim)
		
			# Sources of translation
			sources = []
			
			authorClaim = pywikibot.Claim(site, 'P21')
			authorClaim.setTarget(author)
			sources.append(authorClaim)
		
			pubTitleClaim = pywikibot.Claim(site, 'P26')
			pubTitleClaim.setTarget(pubTitle)
			sources.append(pubTitleClaim)
		
			yearClaim = pywikibot.Claim(site, 'P29')
			yearClaim.setTarget(year)
			sources.append(yearClaim)
		
			placeClaim = pywikibot.Claim(site, 'P28')
			placeClaim.setTarget(place)
			sources.append(placeClaim)
		
			publisherClaim = pywikibot.Claim(site, 'P41')
			publisherClaim.setTarget(publisher)
			sources.append(publisherClaim)
			
			transClaim.addSources(sources)
			
			# Other properties
			
			addClaimToItem(site, page, 'P25', ipr)
			addClaimToItem(site, page, 'P48', BorhyID) # ELTE identifier
			if edh:
				addClaimToItem(site, page, 'P24', edh)
			
	f.close()
	
def addClaimToItem(site, page, id, value):
	"""Adds a claim to an ItemPage."""
	claim = pywikibot.Claim(site, id)
	claim.setTarget(value)
	page.addClaim(claim)

def normalizeText(text):
	"""Removes double spaces, newlines and spaces at the beginning or at the end of the string"""
	text = re.sub('\n', ' ', text.strip())
	text = re.sub('\s{2,}', ' ', text)
	return text

def getDataFromEDH(edh):
	"""Gets data from an online XML source"""
	
	namespacePrefix = '{http://www.tei-c.org/ns/1.0}'
	url = "http://edh-www.adw.uni-heidelberg.de/edh/inschrift/" + edh + ".xml"
	
	response = urllib2.urlopen(url)
	xmlCode = response.read()
	root = ET.XML(xmlCode)
	
	data = {}
	data['description'] = normalizeText(root.find('.//' + namespacePrefix + 'title').text)
	
	return data
		
if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()