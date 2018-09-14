# contentDM-Export
(Software and therefore README incomplete)
Script designed to export collections from ContentDM, into a form that can be uploaded to Omeka

Usage:
>python3 CDM2CSV.py \<collections.carli......collections.exe\> \<username\> \<password\>

Where <collections.carli......collections.exe> is the URL of your collection page on your CONTENTdm dashboard

You will also need to create a Field Map.  This is a text file that has a format like contentdmfield->dublincorefield: for example
Title->dcterms:title
Access Rights->dcterms:accessRights
Date Accepted->dcterms:dateAccepted
etc->etc:etc
For all fields in all of your contentDM collections.  A sample Field Map file is included that may work for some contentDM setups.
Verify that all of the dublincore data used in the map matches the properties of the dublin core vocabulary.
