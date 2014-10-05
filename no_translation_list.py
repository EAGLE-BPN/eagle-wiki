# -*- coding: utf-8 -*-

import pywikibot, operator
from pywikibot import pagegenerators

"""

This script prints out a list of items without translation.

"""

ITEM_NAMESPACE = 120
CAT_NAME = 'Category:Lists by translation language'

def main():
	
	# pywikibot/families/eagle_family.py
	site = pywikibot.Site('en', 'eagle')
	repo = site.data_repository()
	
	translatedItems = []
	listCat = pywikibot.Category(repo, CAT_NAME)
	pywikibot.output('Fetching list of translated items from ' + listCat.title(asLink=True) + ' ...')
	for tList in listCat.articles():
		pywikibot.output(tList.title(asLink=True))
		for p in tList.linkedPages(namespaces=ITEM_NAMESPACE):
			translatedItems.append(p.title(withNamespace=False))
	
	pywikibot.output("\nList of items with no translation:\n")
	for p in repo.allpages(namespace=ITEM_NAMESPACE):
		if p.title(withNamespace=False) not in translatedItems:
			pywikibot.output('* [[' + p.title() + ']]', toStdout=True)
	
if __name__ == "__main__":
	try:
		main()
	finally:
		pywikibot.stopme()