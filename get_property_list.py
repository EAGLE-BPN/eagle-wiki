# -*- coding: utf-8 -*-

import pywikibot, operator
from pywikibot import pagegenerators

"""

This script prints out a list of links to items having the property given via the -property argument.
The output is sent to stdout so it can be easily redirected to a file.

Accepted options:

	-property:<N>
		It's the only mandatory option.
		Example:
			-property:28
		All and only the items containing this property will be fetched.
		
	-show:[ property | label | title ]
		How the links should be titled.
		'property': the title of each link is the text of the property (default)
		'label': the title of each link is the item label
		'title': the title of each link is the item title
		Optional argument.
		
	-sort:[ property | label | title ]
		'title': sorts by item title
		'property': sort by the property specified via -property (default)
		'label': sort by item label
		Default: same as "show".
	
	-label-lang:[ en | it | fr | ... ]
		The language of the label if "-show:label" is given.
		"en" is the default.
	
	-file:<filename>
		Optional argument. File containing the IDs of the elements to fetch, one per row, without brackets.
		The format of the titles must be "Qxxxx" (without namespace). See also the example below.
		If -file is indicated, the script will fetch and list (by title, label or property
		as indicated by -show) all and only the elements in the file.
	
Example #1:

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


Example #2: 

	getting the list for http://eagle-network.eu/wiki/index.php/Inscriptions_of_Aphrodisias
	and saving it in file insaph_list.txt

	python get_property_list.py -property:50 -show:property > insaph_list.txt
	
"""

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
	output = getItemsForProperty(repo, prop, sort, labelLang, fileName)
	
	for i in output:
		pywikibot.output('* [[' + i['title'] + '|' + i[show] + ']]', toStdout=True)


def getItemsForProperty(repo, property, sort='property', labelLang='en', fileName=None, additionalProperties=[]):
	
	"""
	Returns a list of dictionaries
	{
		title:"Qxxx",
		property:<N>,
		label:"<Label>",
		additionalProperties:{'1': 'dfnj', '2': 'sdfsad'},
	}
	This function can be called from other scripts.
	
	Arguments:
		repo:
			Wikidata repository
			
		property:
			number of the property to fetch
			
		sort:[ property | title | label ]
			how to sort the list of links
			
		labelLang:[ en | it | de | ... ]
			language of the label
			
		fileName:<filename>
			Optional argument. File containing the IDs of the elements to fetch, one per row, without brackets.
			The format of the titles must be "Qxxxx" (without namespace). See also the example below.
			If -file is indicated, the function will fetch and list all and only the elements in the file.
		
		additionalProperties:['1, '45', '92', ...]
			list of additional properties to fetch
	"""
	
	SORT_TITLES = 'title'
	SORT_PROP = 'property'
	SORT_LABEL = 'label'
	ITEM_NAMESPACE = 120
	
	propertyId = 'p' + str(property) # Example: "p11"
	
	ids = [] # Array of item IDs
	if fileName:
		with open(fileName, 'r') as f:
			for id in f:
				id = id.strip() # strip newline
				ids.append(id)
	else:
		propPage = pywikibot.PropertyPage(repo, 'Property:P' + str(property))
		refGen = pywikibot.pagegenerators.ReferringPageGenerator(propPage, followRedirects=False,
						   withTemplateInclusion=False,
						   onlyTemplateInclusion=False)
		for i in refGen:
			if i.namespace() == ITEM_NAMESPACE: # quite ugly, to improve
				ids.append(i.title(withNamespace=False))
	
	if len(ids) == 0:
		return
	
	result = loadItems(repo, ids)
	output = []
	
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
					claimValue = claimDict['mainsnak']['datavalue']['value']
					outputItem = {
						'title': itemTitle,
						'property': claimValue,
						'label': itemLabel,
					 }
				
				outputItem['additionalProperties'] = {}
				for prop in additionalProperties:
					if ('p'+prop) in item['claims'].keys():
						for claimDict in item['claims']['p'+prop]:
							claimValue = claimDict['mainsnak']['datavalue']['value']
							outputItem['additionalProperties'][prop] = claimValue
				
				output.append(outputItem)
	
	if sort == SORT_TITLES:
		output = sorted(output, key=operator.itemgetter('title'))
	elif sort == SORT_PROP:
		output = sorted(output, key=operator.itemgetter('property'))
	elif sort == SORT_LABEL:
		output = sorted(output, key=operator.itemgetter('label'))
	
	return output
	

def loadItems(repo, idList):
	
	# Loads the item data from a list of item ids, from the Wikibase API.
	
	API_LIMIT = 500
	
	chunks = divide(idList, API_LIMIT)
	result = {}
	for ids in chunks:
		idString = '|'.join(ids) # Concatenated IDs for API call
		result.update(repo.loadcontent(identification={'ids': idString})) # API call
	return result


def divide(theList, size):
	
	# Divides a list in blocks of size "size".
	# Returns a list of lists.

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