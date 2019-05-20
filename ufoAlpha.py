from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, NUMERIC
from whoosh.analysis import StemmingAnalyzer
import os, os.path
from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser


#CSV sieht folgendermaßen aus: datetime,city,state,country,shape,duration (seconds),duration (hours/min),comments,date posted,latitude,longitude
schema = Schema(date=ID(stored=True),
				city=TEXT(stored=True),
				state=TEXT(stored=True),
				country=TEXT(stored=True),
				shape=TEXT(stored=True),
				durationSecs=NUMERIC(stored=True),
				durationHoursMins=TEXT(stored=True), # eventuell rausnehmen, da Sekunden exakter sind
				comments=TEXT(analyzer=StemmingAnalyzer()), # oder Standardanalyzer
				datePosted=ID(stored=True),
				latitude=NUMERIC(stored=True),
				longitude=NUMERIC(stored=True)
				)
				
#to create an index in a dictionary
if not os.path.exists("indexAlpha"):
    os.mkdir("indexAlpha")
ix = index.create_in("indexAlpha", schema)
#open an existing index object
ix = index.open_dir("indexAlpha")
#create a writer object to add documents to the index
writer = ix.writer()
#now we can add documents to the index

#10/10/1949 20:30,san marcos,tx,us,cylinder,2700,45 minutes,"This event took place in early fall around 1949-50. It occurred after a Boy Scout meeting in the Baptist Church. The Baptist Church sit",4/27/2004,29.8830556,-97.9411111

writer.add_document(date = u"10/10/1949 20:30",
					city = u"san marcos",
					state = u"tx",
					country = u"us",
					shape = u"cylinder",
					durationSecs = u"2700",
					durationHoursMins = u"45 minutes",
					comments = u"This event took place in early fall around 1949-50. It occurred after a Boy Scout meeting in the Baptist Church. The Baptist Church sit",
					datePosted = u"4/27/2004",
					latitude = u"29", # die Längen- und Breitengrade sind brutal verkürzt auf Int
					longitude = u"-97"
                   )
                   
writer.add_document(date = u"10/10/1949 21:00",
					city = u"lackland afb",
					state = u"tx",
					country = u"us",
					shape = u"light",
					durationSecs = u"7200",
					durationHoursMins = u"1 - 2 hours",
					comments = u"1949 Lackland AFB&#44 TX.  Lights racing across the sky &amp; making 90 degree turns on a dime.",
					datePosted = u"12/16/2005",
					latitude = u"29",
					longitude = u"-98"
                   )
# 10/17/2001 15:10,denver,co,us,sphere,1200,20 minutes,"Bright sphere in sky&#44 completely stationary&#44 then disappeared",1/11/2002,39.7391667,-104.9841667
                   
writer.add_document(date = u"10/17/2001 15:10",
					city = u"denver",
					state = u"co",
					country = u"us",
					shape = u"sphere",
					durationSecs = u"1200",
					durationHoursMins = u"20 minutes",
					comments = u"Bright sphere in sky&#44 completely stationary&#44 then disappeared",
					datePosted = u"1/11/2002",
					latitude = u"39",
					longitude = u"-104"
                   )
                   
writer.commit()

queryParser = QueryParser("comments",schema=schema)
multiParser = MultifieldParser(["city", "shape", "comments"], schema=schema)

mq = multiParser.parse(u"sky")
sq = queryParser.parse(u"sky")

with ix.searcher() as s:
    results = s.search(mq)
    for r in results:
	            print(r) 
	
    #singleResults = s.search(sq)
#print(results)
#print("\n")
#print(singleResults)

# Gedanken: Die Schnittstelle zum Interface ist am Wichtigsten. Alle Fragen der Darstellung besprechen.
# nächste Orte finden mit Hilfe von Breitengrad/Längengrad?
# To do: Die CSV Datei für das Indexieren komplett einlesen (evtl. Formatierungen wie &#44 beseitigen), NUMERIC für Float rauskriegen, Ranking verbessern, fuzzy Wörter usw!
          
