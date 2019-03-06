#Project: CDM2CSV
#Organization: SIUE Lovejoy Library, Digital Initiatives Department
#Programmers: Dale Auten, Jacob Grubb
#Contacts: dauten@siue.edu, jagrubb@siue.edu
#Description: A Python script to help mediate the transfer of library data between ContentDM and Omeka S
import requests, re
import sys, time
import csv, io, json
#function uses args as input and returns a list of the collections names in a format like "/sie_meander"
def getCollectionList(contentDMcollection, contentDMusername, contentDMpassword):
	print("Beginning collection reading")
	#uses args as info to scrape document.
	r=requests.get(contentDMcollection, auth=(contentDMusername, contentDMpassword))
	#print(r.text)
	#the data we want is in a drop down box.  This regex matches the content from drop down boxes
	pattern='value="\/.{1,6}_.{1,16}"'
	text=re.findall(pattern,r.text)
	collection=[]

	#the regex includes 'value="' and '"' in the returned string so take substring to cut those bits off
	for node in text:
	#	print("Got: "+node[7:-1])
		collection.append(node[7:-1])
	#after all data is added to collection
	print("collection:")
	print(collection)
	return collection

#P: Json Object representing output of a carli collection
#Q: Json-L Object representing what omeka API expects to be passed
def carliToOmeka(json_object, fieldmap, params):
	#for every json object (aka every item in the collection)
	q=[]
	haveSeen = []

	for f in fieldmap:
		if len(f) < 4:
			print(f)
	imageFormat = ["jpg","png","gif","jp2"]
	pdfPage = "collections.carli.illinois.edu/utils/getdownloaditem/collection/{0}/id/{1}/filename/584.pdfpage/mapsto/pdf"
	for j in json.loads(json_data):
		if "CONTENTdm file name" in j.keys() and j["CONTENTdm file name"][-3:] == "cpd":
			current = {}
			#for every aspect (title description etc) in that object
			for key in j.keys():
				for field in fieldmap:
					if field[0] == key:
						current[field[1]] = [ {} ]
						current[field[1]][0]["type"] = "literal"
						current[field[1]][0]["@value"] = j[key]
						current[field[1]][0]["property_id"] = field[2]
			r = requests.post("http://146.163.157.78/omeka-s/api/items", headers={"Content-type":"application/json"}, json=current,  params=params )
			omekaNumber = json.loads(r.text)["o:id"]
			if j["CONTENTdm file path"][-3:] == "pdf":
				url = j["Reference URL"]
				source = requests.get(url).text
				p=re.compile("/utils/.*/mapsto/pdf")
				print("PDF has length of "+str(len(p.findall(source))))
				print("that is from\n\n\n"+source)
				pdfUrl = "http://collections.carli.illinois.edu" + p.findall(source)[0]
				try:
					response = requests.get(pdfUrl)
					with open('./contentdm_files/'+j["Title"].replace(".","")+'.pdf', 'wb') as f:
						f.write(response.content)
				except Exception as e:
					raise
				current = {}
				data = {
				    "o:ingester": "upload",
				    "file_index": "0",
				    "o:item": {"o:id": omekaNumber},
				}
				files = [
				     ('data', (None, json.dumps(data), 'application/json')),
				     ('file[0]', (j["Title"].replace(".","")+".pdf", open('./contentdm_files/'+j["Title"].replace(".","")+".pdf", 'rb'), 'application/pdf'))
				]
				response = requests.post('http://146.163.157.78/omeka-s/api/media', params=params, files=files)
				print("Response from server for our POST:\n\t"+str(response))
				if "500" in str(response):
					print("\t"+str(files)+str(params))



			for media in q:
				current = {}
				data = {
				    "o:ingester": "upload",
				    "file_index": "0",
				    "o:item": {"o:id": omekaNumber},
				}
				for key in media.keys():
					for field in fieldmap:
						if field[0] == key:
							data[field[1]] = [ {} ]
							data[field[1]][0]["type"] = "literal"
							data[field[1]][0]["@value"] = media[key]
							data[field[1]][0]["property_id"] = field[2]
				files = [
				     ('data', (None, json.dumps(data), 'application/json')),
				     ('file[0]', (media["Title"], open('./contentdm_files/'+media["Title"], 'rb'), 'image/jpg'))
				]
				response = requests.post('http://146.163.157.78/omeka-s/api/media', params=params, files=files)
				print("Response from server for our POST:\n\t"+str(response))
			q=[]




		#else it is media
		elif "CONTENTdm file name" in j.keys() and j["CONTENTdm file name"][-3:] in imageFormat:
			#download image with title as filename into hidden folder
			try:
				response = requests.get(imageTemplate.format(j["CONTENTdm file path"].split("/")[1], j["CONTENTdm number"] ))
				with open('./contentdm_files/'+j["Title"], 'wb') as f:
					f.write(response.content)
			except Exception as e:
				raise
			#add this item to our list of things to add.
			#right now we don't know what item this goes to, we save them for when we do
			q.append(j)

		else:
			if "CONTENTdm file name" in j.keys() and j["CONTENTdm file name"].split(".")[-1] not in haveSeen:
				print("."+str(j["CONTENTdm file name"].split(".")[-1]))
				print("\t("+str(j)+")")
				haveSeen.append(j["CONTENTdm file name"].split(".")[-1])


#Below is the template URL for scraping images
options=open("config.ini", "r").read().split("\n")
for line in range(0, len(options)):
	options[line] = "=".join(options[line].split("=")[1:])

contentDMusername=options[0]
contentDMpassword=options[1]
contentDMcollection=options[2]
key_identity=options[3]
key_credential=options[4]
omekaURL=options[5]
imageTemplate = options[6]
generateTemplate = options[7]
exportTemplate= options[8]


#EXECUTION BEGIN
collectionList = getCollectionList(contentDMcollection, contentDMusername, contentDMpassword)
idRange = 0, 0 #Tuple to represent the range of ID to be drawn, where idRange[0] is the start ID and idRange[1] is the end ID


tsv = []

counter = 0;

fieldmap = []
file = open("fieldmap", "r")
for line in file:
	fieldmap.append( line.replace("\n", "").split("->") )

'''
metadata = open(".dbcmap", "r").read().split("\n")

for f in fieldmap:
	for line in metadata:
		if f[1] == line.split("\t")[0]:
			f.append(line.split("\t")[1])
			f.append(line.split("\t")[2])
'''

csv.field_size_limit(sys.maxsize)
for collection in collectionList:
	#generate file
	url=generateTemplate.format(collection)
	r=requests.get(url, auth=(contentDMusername, contentDMpassword))

	#download file
	url=exportTemplate.format(collection)
	r=requests.get(url, auth=(contentDMusername, contentDMpassword))

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
	open(".last.csv", "w").write(json_data)
	carliToOmeka(json_data, fieldmap, {"key_identity":key_identity, "key_credential":key_credential} )
	print("===="+collection+" complete====")
