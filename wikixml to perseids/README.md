Eagle Wikibase .xml to Perseids Translation's Epidoc 
====

XSLT to transform items from the EAGLE Wikibase into the epidoc standard for translations of inscription used by Perseids.

Uses cts urns still under discussion

the xsl is meant to run on the result of this url

http://www.eagle-network.eu/wiki/api.php?action=query&list=allpages&apnamespace=120&aplimit=500&format=xml

and return one single file with all the items in it.
the test files in it consider several cases present in the wiki