# -*- coding: utf-8 -*-
"""

This is the family file for the EAGLE Wiki.
It should be put in the pywikibot/families folder.

Configuration parameters:
  url = http://www.eagle-network.eu/wiki/index.php/Main_Page
  name = eagle

Please do not commit this to the pywikibot repository!

"""

from pywikibot import family

class Family(family.Family):
    def __init__(self):
        family.Family.__init__(self)
        self.name = 'eagle'
        self.langs = {
            'en': 'www.eagle-network.eu',
        }

    def scriptpath(self, code):
        return {
            'en': '/wiki',
        }[code]

    def version(self, code):
    	# Check me
    	# http://eagle-network.eu/wiki/index.php/Special:Version
        return {
            'en': u'1.23',
        }[code]
        
    def shared_data_repository(self, code, transcluded=False):
        """Always return a repository tupe. This enables testing whether
        the site opject is the repository itself, see Site.is_data_repository()

        """
        if transcluded:
            return (None, None)
        else:
            if code == 'en':
                return ('en', 'eagle')
            else:
                return (None, None)
    
    def shared_image_repository(self, code):
        return ('commons', 'commons')
