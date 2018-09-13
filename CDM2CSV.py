import requests
import re
import sys
import time

if len(sys.argv)<4:
	print("Usage: python3 CDM2CSV.py [collections.carli......exe] [username] [password]")
	sys.exit(1)
collectionList = getCollectionList(sys.argv)
idRange = 0, 0 #Tuple to represent the range of ID to be drawn, where idRange[0] is the start ID and idRange[1] is the end ID

#Below is the template URL for scraping images
urlTemplate = "http://collections.carli.illinois.edu/utils/ajaxhelper/?CISOROOT={0}&CISOPTR={1}&action=2&DMWIDTH=10000&DMHEIGHT=10000"

for collection in collectionList:
	for id in idRange[1] - idRange[0]:
		url = urlTemplate.format(collection, id)
		print("Processing: " + collection + " | ID: " + id)
		req = requests.get(url, alloq_redirects=False)
		#Request Complete
		time.sleep(0.1)


def getCollectionList(self):
	pattern='value="\/.{1,6}_.{1,16}"'
	r=requests.get(sys.argv[1], auth=(sys.argv[2], sys.argv[3]));
	text=re.findall(pattern,r.text)
	collection=[]
	for node in text:
		collection.append(node[7:-1])
	return collection
