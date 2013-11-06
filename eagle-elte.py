# -*- coding: utf-8 -*-

import pywikibot, csv, re, urllib2
import xml.etree.ElementTree as ET

DATA_FILE = '/Users/pietro/Dropbox/Dati/elte.csv'

def main():
	always = dryrun = False
	
	# Handles command-line arguments for pywikibot.
	for arg in pywikibot.handleArgs():
		if arg == '-dry': # Performs a dry run (does not edit site)
			dryrun = True
		if arg == '-always': # Does not ask for confirmation
			always = True
	
	# pywikibot/families/eagle_family.py
	site = pywikibot.Site('en', 'eagle').data_repository()
	
	f = open(DATA_FILE, 'r')
	reader = csv.reader(f, delimiter=";")
	for row in reader:
		BorhyID = normalizeText(row[8])
		
		pywikibot.output("\n>>>>> " + BorhyID + " <<<<<\n")
		pywikibot.output('BorhyID: ' + BorhyID)
		
		translationHu = normalizeText(row[1])
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
			page = pywikibot.ItemPage.createNew(site, labels={'en': BorhyID}, descriptions=descriptions)
		
			# HU translation
			transClaim = pywikibot.Claim(site, 'P19')
			transClaim.setTarget(translationHu)
			page.addClaim(transClaim)
		
			# Sources of translation
			sources = []
			
			authorClaim = pywikibot.Claim(site, 'P21')
			authorClaim.setTarget(author)
			sources.append(authorClaim)
		
			pubTitleClaim = pywikibot.Claim(site, 'P32')
			pubTitleClaim.setTarget(pubTitle)
			sources.append(pubTitleClaim)
		
			yearClaim = pywikibot.Claim(site, 'P29')
			yearClaim.setTarget(year)
			sources.append(yearClaim)
		
			placeClaim = pywikibot.Claim(site, 'P26')
			placeClaim.setTarget(place)
			sources.append(placeClaim)
		
			publisherClaim = pywikibot.Claim(site, 'P41')
			publisherClaim.setTarget(publisher)
			sources.append(publisherClaim)
			
			transClaim.addSources(sources)
			
			# Other properties
			
			addClaimToItem(site, page, 'P25', ipr)
			if edh:
				addClaimToItem(site, page, 'P24', edh)
			
	f.close()
	
def addClaimToItem(site, page, id, value):
	"""Adds a claim to an ItemPage."""
	claim = pywikibot.Claim(site, id)
	claim.setTarget(value)
	page.addClaim(claim)

def normalizeText(text):
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
	data['description'] = root.find('.//' + namespacePrefix + 'title').text
	
	return data
		
if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()