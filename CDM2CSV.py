#Project: CDM2CSV
#Organization: SIUE Lovejoy Library, Digital Initiatives Department
#Programmers: Jacob Grubb, Dale Auten
#Contacts: jagrubb@siue.edu, dauten@siue.edu
#Description: A Python script to help mediate the transfer of library data between ContentDM and Omeka S
import requests
import re
import sys
import time

#function uses args as input and returns a list of the collections names in a format like "/sie_meander"
def getCollectionList():
	#uses args as info to scrape document.
	r=requests.get(sys.argv[1], auth=(sys.argv[2], sys.argv[3]));
	#the data we want is in a drop down box.  This regex matches the content from drop down boxes
	pattern='value="\/.{1,6}_.{1,16}"'	
	text=re.findall(pattern,r.text)
	collection=[]

	#the regex includes 'value="' and '"' in the returned string so take substring to cut those bits off
	for node in text:
		collection.append(node[7:-1])
	#after all data is added to collection
	return collection

#checks usage
#TODO: use regex to verify integrity of data
if len(sys.argv)<4:
	print("Usage: python3 CDM2CSV.py [collections.carli......collections.exe] [username] [password]")
	sys.exit(1)

#EXECUTION BEGIN
collectionList = getCollectionList()
idRange = 0, 0 #Tuple to represent the range of ID to be drawn, where idRange[0] is the start ID and idRange[1] is the end ID

#Below is the template URL for scraping images
imageTemplate = "http://collections.carli.illinois.edu/utils/ajaxhelper/?CISOROOT={0}&CISOPTR={1}&action=2&DMWIDTH=10000&DMHEIGHT=10000"
generateTemplate = "https://collections.carli.illinois.edu:8443/cgi-bin/admin/export.exe?CISODB={0}&CISOOP=ascii&CISOMODE=1&CISOPTRLIST="
exportTemplate= "https://collections.carli.illinois.edu:8443/cgi-bin/admin/getfile.exe?CISOMODE=1&CISOFILE={0}/index/description/export.txt"

#for collection in collectionList:

for collection in getCollectionList():
	url=generateTemplate.format(collection)
	requests.get(url, auth=(sys.argv[2], sys.argv[3]));
	url=exportTemplate.format(collection)
	r=requests.get(url, auth=(sys.argv[2], sys.argv[3]));
	print(r.text[0:100])
#	for id in range(82,84):
#		url = urlTemplate.format(collection, str(id))
#		print("Processing: " + collection + " | ID: " + str(id))
#		req = requests.get(url, alloq_redirects=False)
#		#Request Complete
#		time.sleep(0.1)
	