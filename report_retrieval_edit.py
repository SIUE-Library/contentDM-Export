import requests
import time
import getpass


#uname = input("Please input ContentDM username: ")
#pword = getpass.getpass()

collectionsList = ["sie_alum","siue_civilw","sie_ajt","sie_cwmusic","sie_drumman","sie_drum","sie_ebr1","sie_mmmarch","sie_moore","sie_cabet","sie_dill","sie_kmox","sie_arch","sie_muse","sie_finiels","sie_observe","sie_plants","sie-meander","sie_seedbed","sie_pioneer","sie_shurt","sie_soccer","sie_swiss","sie_brink","sie_diary"]

#datesList = ["201701", "201702", "201703", "201704", "201705", "201706", "201707", "201708", "201709", "201710", "201711", "201712", "201801", "201802", "201803", "201804", "201805", "201806", "201807", "201808", "201809"]

#get from
urlTemplate = #Enter the url for downloading here, with a {0} to be substituted with the collection name
outFile = open("./output.txt", "w")
#outFile.write("\"Date\"\t\"Collection\"\t\"Item ID\"\t\"Pageviews\"\t\"Item Title\"\t\"Item Ref Url\"\n")
for collection in collectionsList:
	time.sleep(1)
	url = urlTemplate.format(collection)
	print("Processing: " + collection)		
	#req = requests.get(url, auth=(uname, pword), allow_redirects=False)
		#Previous request, with formatting above
	req = requests.get(url, allow_redirects=False)
