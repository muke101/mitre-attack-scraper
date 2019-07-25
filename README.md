# mitre-attack-scraper
Basic scraper that takes specific text fields from eah other windows techniques listed on the Mitre Attack framework (https://attack.mitre.org/)
and then parses through a template file to insert the extracted text into it, outputting a new .html file for every page on the mitre attack site.
These files will then be uploaded automatically to the internal Visa wiki with the second script (coming soon) and then have Visa specific information
added to them, keeping all the relevant information of an attack vector centralized and easily accessible.

This was made with the requests, beautiful soup and splinter libraries.
