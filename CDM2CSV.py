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


#P: Json Object representing output of a carli collection
#Q: Json-L Object representing what omeka API expects to be passed
def carliToOmeka(json_object, fieldmap):
	#for every json object (aka every item in the collection)
	for j in json.loads(json_data):
		if j["CONTENTdm file name"][-3:] == "cpd":
			current = {}
			#for every aspect (title description etc) in that object
			for key in j.keys():
				for field in fieldmap:
					if field[0] == key:
						current[field[1]] = [ {} ]
						current[field[1]][0]["type"] = "literal"
						current[field[1]][0]["@value"] = j[key]
						current[field[1]][0]["property_id"] = field[2]
			r = requests.post("http://146.163.157.78/omeka-s/api/items", headers={"Content-type":"application/json"}, json=current,  params={"key_identity":"NuXE6YOtL3tS5T1iNe5MZJdo3hzvgcXU", "key_credential":"Hi4KqIqa4FBFKJcRG3YgtYkP0mxwIdbB"} )


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

csv.field_size_limit(sys.maxsize)
for collection in collectionList:
	#generate file
	url=generateTemplate.format(collection)
	requests.get(url, auth=(sys.argv[2], sys.argv[3]))
	#download file
	url=exportTemplate.format(collection)
	r=requests.get(url, auth=(sys.argv[2], sys.argv[3]))

	#do some text cleaning on the file to replace tabs with commas and wrap fields with quotes
	text=r.text

	text=text.split("\n")

	#update any fieldnames that were aliased in the fieldmap
	for field in fieldmap:
		text[0]=text[0].replace('"'+field[0]+'"', '"'+field[1]+'"')

	out = ""

	for line in text:
		out+=line+"\n"

	#convert to json and write
	open("."+str(counter)+".csv", "w").write(out)
	json_data = json.dumps(list(csv.DictReader(io.StringIO(out), delimiter="\t")), indent=4, sort_keys=True)
	open("."+str(counter)+".json", "w").write(json_data)
	counter += 1
	#print(json_data+"\nwaiting...\n")
	open(".last.csv", "w").write(json_data)
	time.sleep(.25)
	carliToOmeka(json_data, fieldmap)

