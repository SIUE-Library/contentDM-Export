# ContentDM-Export
_(Software incomplete)_

Script designed to export collections from [ContentDM](https://www.oclc.org/en/contentdm.html) content management platform, into a form that can be uploaded the [Omeka S](https://omeka.org/s/) content management platform

Usage:
```
python3 CDM2CSV.py <collections.carli......collections.exe> <username> <password>
```

Where <collections.carli......collections.exe> is the URL of your collection page on your CONTENTdm dashboard. The <username> and <password> need to be for a contentDM account with access to report generation.
  
 _____________ 
__This project makes use of the [```requests.py```](http://docs.python-requests.org/en/master/) which uses TLS for security__

## Field Map
Users will also need to create a Field Map.  This is a text file that has a format like contentdmfield->dublincorefield

>Title->dcterms:title<br>
Access Rights->dcterms:accessRights<br>
Date Accepted->cterms:dateAccepted<br>
etc->etc:etc 

A list of Dublin Core Field items may be found at http://dublincore.org/documents/1999/07/02/dces/
Please verify that all of the dublincore data used in the map matches the properties of the dublin core vocabulary.


MIT LICENSE Copyright (c) 2018 SIUE Lovejoy Library
