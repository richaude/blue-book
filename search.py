# Ausführung z.B. mit: python3 search.py "Germany"
from whoosh.qparser import MultifieldParser
from whoosh import index
from indexing import mkSchema
import sys

def suche(schema, index_ordner, query):
	multiParser = MultifieldParser(["city", "country", "shape", "comments"], schema=schema)
	mq = multiParser.parse(query)
	ix = index.open_dir(index_ordner)
	with ix.searcher() as s:
         results = s.search(mq)
         #results.fragmenter.charlimit = None
         for r in results:
           print(r["date"]+":\n"+r["city"]+"\n"+r["country"]+"\n"+r["comments"])
	            
if __name__ == "__main__":
	q = sys.argv[1]
	schema = mkSchema()
	suche(schema, "ufo_index", q)
	            
#queryParser = QueryParser("comments",schema=schema)
#sq = queryParser.parse(u"sky")

# Gedanken: Die Schnittstelle zum Interface ist am Wichtigsten. Alle Fragen der Darstellung besprechen.
# nächste Orte finden mit Hilfe von Breitengrad/Längengrad?
# To do: Die CSV Datei für das Indexieren komplett einlesen (evtl. Formatierungen wie &#44, &#amp; beseitigen), Ranking verbessern, fuzzy Wörter usw!
