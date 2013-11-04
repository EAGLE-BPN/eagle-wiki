# -*- coding: utf-8 -*-

import pywikibot, csv, re

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
		#id = row[0]
		#pywikibot.output("\n>>>>> " + id + " <<<<<\n")
		
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
		
		BorhyID = normalizeText(row[8])
		pywikibot.output('BorhyID: ' + BorhyID)
		
		edh = normalizeText(row[9])
		pywikibot.output('EDH: ' + edh)
		
		pywikibot.output('') # newline
		
		if not always:
			choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All'], ['y', 'N', 'a'], 'N')
		else:
			choice = 'y'
		if choice in ['A', 'a']:
			always = True
			choice = 'y'
		if not dryrun and choice in ['Y', 'y']:
			page = pywikibot.ItemPage.createNew(site, labels={'hu': BorhyID})
		
			# HU translation
			transClaim = pywikibot.Claim(site, 'P19')
			transClaim.setTarget(translationHu)
			page.addClaim(transClaim)
		
			# Sources of translation
		
			authorClaim = pywikibot.Claim(site, 'P21')
			authorClaim.setTarget(author)
		
			pubTitleClaim = pywikibot.Claim(site, 'P32')
			pubTitleClaim.setTarget(pubTitle)
		
			yearClaim = pywikibot.Claim(site, 'P29')
			yearClaim.setTarget(year)
		
			placeClaim = pywikibot.Claim(site, 'P28')
			placeClaim.setTarget(place)
		
			publisherClaim = pywikibot.Claim(site, 'P41')
			publisherClaim.setTarget(publisher)
			
			transClaim.addSources([authorClaim, pubTitleClaim, yearClaim, placeClaim, publisherClaim])
			
			# Other properties
			
			addClaimToItem(site, page, 'P25', ipr)
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
	
if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()