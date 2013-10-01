# -*- coding: utf-8 -*-

import pywikibot, os, re
import xml.etree.ElementTree as ET

DATA_DIR = '/Users/pietro/Dropbox/Dati/British School of Rome/'

def main():
	args = pywikibot.handleArgs()
	
	# pywikibot/families/eagle_family.py
	site = pywikibot.Site('en', 'eagle').data_repository()
	all = False
	
	for fileName in os.listdir(DATA_DIR):
		tree = ET.parse(DATA_DIR + fileName)
		root = tree.getroot()
		title = elementText(root.findall('./teiHeader/fileDesc/titleStmt/title')[0])
	
		# ID
		pywikibot.output(">>>>> " + title + " <<<<<")
		
		if not all:
			choice = pywikibot.inputChoice(u"Proceed?",  ['Yes', 'No', 'All'], ['y', 'N', 'a'], 'N')
		else:
			choice = 'y'
		if choice in ['A', 'a']:
			all = True
			choice = 'y'
		if choice in ['Y', 'y']:
			page = pywikibot.ItemPage.createNew(site, labels={'en': title}) # New item
			
			# BSR ID
			addClaimToItem(site, page, 'P40', fileName[0:-4]) # Remove extension
			
			# IPR
			ipr = elementText(root.findall('./teiHeader/fileDesc/publicationStmt/p')[0])
			ipr = re.sub(' \(.*?\)', '', ipr)
			print 'IPR: ' + ipr
			addClaimToItem(site, page, 'P25', ipr)
			
			# EN Translation
			transClaim = pywikibot.Claim(site, 'P11')
			translationEn = elementText(root.findall('./text/body/div[@type=\'translation\']/p')[0])
			print 'EN: ' + translationEn
			transClaim.setTarget(translationEn)
			page.addClaim(transClaim)
			
			# Authors
			authors = root.findall('./teiHeader/fileDesc/titleStmt/editor')
			authorString = ''
			for au in authors:
				authorString += au.text + ', '
			authorString = authorString[0:-2]
			print authorString
			authorClaim = pywikibot.Claim(site, 'P21')
			authorClaim.setTarget(authorString)
			
			# Publication title
			pubTitle = elementText(root.findall('./teiHeader/fileDesc/sourceDesc//title')[0])
			print 'PubTitle: ' + pubTitle
			pubClaim = pywikibot.Claim(site, 'P26')
			pubClaim.setTarget(pubTitle)
			
			# Publication place
			pubPlace = elementText(root.findall('./teiHeader/fileDesc/sourceDesc//pubPlace')[0])
			print 'PubPlace: ' + pubPlace
			pubPlaceClaim = pywikibot.Claim(site, 'P28')
			pubPlaceClaim.setTarget(pubPlace)
			
			# Date
			dateText = elementText(root.findall('./teiHeader/fileDesc/sourceDesc//date')[0])
			print 'Date: ' + dateText
			dateClaim = pywikibot.Claim(site, 'P29')
			dateClaim.setTarget(dateText)
			
			transClaim.addSources([authorClaim, pubClaim, dateClaim, pubPlaceClaim])

# Adds a claim to an ItemPage.		
def addClaimToItem(site, page, id, value):
	claim = pywikibot.Claim(site, id)
	claim.setTarget(value)
	page.addClaim(claim)

# Get inner element text, stripping tags of sub-elements.
def elementText(elem):
	return ''.join(elem.itertext()).strip()

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()