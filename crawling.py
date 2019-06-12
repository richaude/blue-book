from urllib.request import urlopen
from bs4 import BeautifulSoup

# zuerst für diese Seite, mit den einzelnen Sichtungen: https://en.wikipedia.org/wiki/List_of_reported_UFO_sightings
source = urlopen("https://en.wikipedia.org/wiki/List_of_reported_UFO_sightings")
bs = BeautifulSoup(source, "lxml")
#sightings = bs.findAll("table", {"class": "wikitable sortable jquery-tablesorter"})
#sightings = bs.findAll("tbody") #findet zu viel
sightings = bs.findAll("tr")
# List slicing, von fiery disks bis letzte
# dann alle Elemente entfernen wo nur Metadaten (Name, Zeit, Land usw. drin stehen)
#v = 0
#for s in sightings:
	#txt = s.text
	#if "fiery disks" in txt:
	#	print(str(v))
	#if "2018 Ireland UFO sighting" in txt:
	#	print(str(v))
	#v+=1
	
cropped = sightings[9:198]
index = 0
for c in cropped:
	if "Date\nName\nCity, State\nCountry\nDescription\nSources\nHynek Scale" in c.text:
		print(str(index))
	index += 1

del cropped[1]
del cropped[7]
del cropped[11]
del cropped[17]
del cropped[159]

# letzte Säuberungsversuche
for c in cropped:
	ls = c.text.split("\n")
	x=0
	while x < len(ls):
		if ls[x] == "":
			del ls[x]
		x+=2
     #del ls[x]
	print(ls) # ls ist nun eine Liste mit [0] nichts, [1] Datum, [2] nichts, [3] Name, [4] nichts, [5] Bundesstaat US, [6] nichts, [7] Staat, [8] nichts, [9] ist die Beschreibung, [10] ist nichts, [11] ist die Quelle, [12] ist nichts, [13] ist Hymnek Index, [14] ist nichts
	# Säuberungsversuche sind vergeblich
