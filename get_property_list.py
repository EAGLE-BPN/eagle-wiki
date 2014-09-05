# -*- coding: utf-8 -*-

import pywikibot, operator
from pywikibot import pagegenerators

"""

This script prints out a list of ItemPages.
The title of the link is the content of the property specified via the -property parameter.

Parameters:
	-file:
		Optional argument. File containing the IDs of the elements to list, one per row, without brackets.
		If not specified, the script fetches all items containing the property indicated with -property.
	
	-property:
		Number of the property to get.
		Items not containing the specified property will be ignored.
		
	-show: the title of the links
		'property': the title of each link is the text of the property (default)
		'label': the title of each link is the item label
		'title': the title of each link is the item title
		Optional argument.
		
	-sort:
		'title': sorts by item title
		'property': sort by the property specified via -property (default)
		'label': sort by item label
		Default: same as "show".
	
	-label-lang:
		The language of the label if "-show:label" is specified (it, en, fr...)
		"en" is the default.
	
Example:

python get_property_list.py -file:new_items.txt -property:24 -show:property

Content of new_items.txt:
Q4700
Q4701
Q4706

Output:

* [[Item:Q4700|HD016153]]
* [[Item:Q4701|HD065254]]
* [[Item:Q4706|HD065353]]

("HD..." is the property P24 of the items in this case)

"""

SORT_TITLES = 'title'
SORT_PROP = 'property'
SORT_LABEL = 'label'
API_LIMIT = 500
ITEM_NAMESPACE = 120

def main():
	
	# pywikibot/families/eagle_family.py
	site = pywikibot.Site('en', 'eagle')
	repo = site.data_repository()
	
	sort = None
	fileName = None
	labelLang = 'en'
	show = 'property'
	
	# Handles command-line arguments for pywikibot.
	for arg in pywikibot.handleArgs():
		if arg.startswith('-file:'):
			fileName = arg.replace('-file:', '')
		if arg.startswith('-property:'):
			prop = arg.replace('-property:', '')
		if arg.startswith('-sort:'):
			sort = arg.replace('-sort:', '')
		if arg.startswith('-show:'):
			show = arg.replace('-show:', '')
		if arg.startswith('-label-lang:'):
			labelLang = arg.replace('-label-lang:', '')
	
	if sort == None:
		sort = show
	
	propertyId = 'p' + prop # Example: "p11"
	
	ids = [] # Array of item IDs
	if fileName:
		with open(fileName, 'r') as f:
			for id in f:
				id = id.strip() # strip newline
				ids.append(id)
	else:
		propPage = pywikibot.PropertyPage(repo, 'Property:P' + prop)
		refGen = pywikibot.pagegenerators.ReferringPageGenerator(propPage, followRedirects=False,
						   withTemplateInclusion=False,
						   onlyTemplateInclusion=False)
		for i in refGen:
			if i.namespace() == ITEM_NAMESPACE: # quite ugly, to improve
				ids.append(i.title(withNamespace=False))
		
	result = loadItems(repo, ids)
	output = [] # List of dictionaries {title, prop}
	
	for id, item in result.items():
		if 'claims' in item.keys():
			if propertyId in item['claims'].keys():
				itemTitle = item['title']
				if not 'labels' in item:
					itemLabel = 'NO LABEL'
				elif labelLang in item['labels']:
					itemLabel = item['labels'][labelLang]['value']
				else: # label in random language (better than nothing)
					itemLabel = item['labels'].values()[0]['value']
				
				for claimDict in item['claims'][propertyId]:
					claim = pywikibot.Claim.fromJSON(repo, claimDict)
					output.append( {
						'title': itemTitle,
						'property': claim.getTarget(),
						'label': itemLabel } )
	
	if sort == SORT_TITLES:
		output = sorted(output, key=operator.itemgetter('title'))
	elif sort == SORT_PROP:
		output = sorted(output, key=operator.itemgetter('property'))
	elif sort == SORT_LABEL:
		output = sorted(output, key=operator.itemgetter('label'))
	
	for i in output:
		pywikibot.output('* [[' + i['title'] + '|' + i[show] + ']]')

def loadItems(repo, idList):
	chunks = divide(idList, API_LIMIT)
	result = {}
	for ids in chunks:
		idString = '|'.join(ids) # Concatenated IDs for API call
		result.update(repo.loadcontent(identification={'ids': idString})) # API call
	return result

# Divides a list in blocks of size "size".
# Returns a list of lists.
def divide(theList, size):
	result = []
	lst = list(theList) # copy
	while len(lst)>size:
		result.append(lst[0:size])
		lst = lst[size:]
	result.append(lst)
	return result

if __name__ == "__main__":
	try:
		main()
	finally:
		pywikibot.stopme()