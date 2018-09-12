import requests
import re
import sys

if len(sys.argv)<4:
	print("Usage: python3 CDM2CSV.py [collections.carli......exe] [username] [password]")
	sys.exit(1)
pattern='value="\/.{1,6}_.{1,16}"'
r=requests.get(sys.argv[1], auth=(sys.argv[2], sys.argv[3]));
text=re.findall(pattern,r.text)
collection=[]
for node in text:
	collection.append(node[7:-1])

print(collection)
