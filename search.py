from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, NUMERIC
from whoosh.analysis import StemmingAnalyzer



# ist momentan etwas repetitiv, eventuell überlegen wie man das Schema aus einer anderen Datei importieren kann
schema = Schema(date=ID(stored=True),
				city=TEXT(stored=True),
				state=TEXT(stored=True),
				country=TEXT(stored=True),
				shape=TEXT(stored=True),
				durationSecs=NUMERIC(stored=True),
				durationHoursMins=TEXT(stored=True), # eventuell rausnehmen, da Sekunden exakter sind
				comments=TEXT(analyzer=StemmingAnalyzer(), stored=True), # oder Standardanalyzer. stored = True hinzugefügt, die Ergebnisse verdoppeln sich?
				datePosted=ID(stored=True),
				latitude=NUMERIC(float, stored=True),
				longitude=NUMERIC(float, stored=True)
				)

queryParser = QueryParser("comments",schema=schema)
multiParser = MultifieldParser(["city", "shape", "comments"], schema=schema)

mq = multiParser.parse(u"sky")
sq = queryParser.parse(u"sky")

ix = index.open_dir("indexAlpha")

with ix.searcher() as s:
    results = s.search(sq)
    results.fragmenter.charlimit = None
    for r in results:
	            print(r["city"]+"\n"+r["comments"])
	            #print(r.highlights("comments")) 
	
    #singleResults = s.search(sq)

# Gedanken: Die Schnittstelle zum Interface ist am Wichtigsten. Alle Fragen der Darstellung besprechen.
# nächste Orte finden mit Hilfe von Breitengrad/Längengrad?
# To do: Die CSV Datei für das Indexieren komplett einlesen (evtl. Formatierungen wie &#44, &#amp; beseitigen), Ranking verbessern, fuzzy Wörter usw!
