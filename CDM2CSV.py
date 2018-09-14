#Project: CDM2CSV
#Organization: SIUE Lovejoy Library, Digital Initiatives Department
#Programmers: Jacob Grubb, Dale Auten
#Contacts: jagrubb@siue.edu, dauten@siue.edu
#Description: A Python script to help mediate the transfer of library data between ContentDM and Omeka S
import requests, re
import sys, time
import csv, io, json

#function uses args as input and returns a list of the collections names in a format like "/sie_meander"
def getCollectionList():
	#uses args as info to scrape document.
	r=requests.get(sys.argv[1], auth=(sys.argv[2], sys.argv[3]))
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

tsv = []

counter = 0;

fieldmap = []
file = open("fieldmap", "r")
for line in file:
	fieldmap.append( line.replace("\n", "").split("->") )
for each in fieldmap:
	print(each)


for collection in collectionList:
	#generate file
	url=generateTemplate.format(collection)
	requests.get(url, auth=(sys.argv[2], sys.argv[3]))
	#download file
	url=exportTemplate.format(collection)
	r=requests.get(url, auth=(sys.argv[2], sys.argv[3]))

	#do some text cleaning on the file
	text="\""+r.text.replace("\t",'","').replace("\n", '"\n"')

	text=text.split("\n")

	for field in fieldmap:
		text[0]=text[0].replace(field[0], field[1])

	out = ""

	for line in text:
		out+=line+"\n"

	#convert to json and write
	reader = csv.DictReader(io.StringIO(out))
	open("."+str(counter)+".csv", "w").write(out)
	json_data = json.dumps(list(reader))
	open("."+str(counter)+".json", "w").write(json_data)
	counter += 1
	print(json_data+"\nwaiting...\n")
	time.sleep(1)

