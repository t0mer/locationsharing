import os
import re
import pickle
import requests
import http.client 
from loguru import logger

http.client._MAXHEADERS = 1000

class CookiesHandler(object):

    def refresh(self):
        try:
            self.cookiefile = "./cookies/" + os.getenv("COOKIES_FILE_NAME")
            cookies = self.parseCookieFile()
            response = requests.get('https://maps.google.com', cookies=cookies)
            cookies = response.cookies
            logger.info('Cookies reloaded')
        except Exception as e:
            logger.error("Error refreshing cookies. " + str(e))



    def parseCookieFile(self):
        logger.info("Reading cookies")
        cookies = {}
        with open (self.cookiefile, 'r') as fp:
            for line in fp:
                if not re.match(r'^\#', line):
                    lineFields = line.strip().split('\t')
                    if len (lineFields) >= 6:
                        cookies[lineFields[5]] = lineFields[6]
                    
        return cookies
