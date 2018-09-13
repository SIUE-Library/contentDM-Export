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

for collection in collectionList:
	print(collection)
#	for id in idRange[1] - idRange[0]:
#		url = urlTemplate.format(collection, id)
#		print("Processing: " + collection + " | ID: " + id)
#		req = requests.get(url, alloq_redirects=False)
		#Request Complete
#		time.sleep(0.1)
	

