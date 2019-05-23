import os, os.path
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, NUMERIC
from whoosh.analysis import StemmingAnalyzer
from whoosh import index


def lies(datei):
	f = open(datei, "r")
	lines = f.readlines()
	f.close()
	return lines

def mkSchema():
	schema = Schema(date=ID(stored=True),
				city=TEXT(stored=True),
				state=TEXT(stored=True),
				country=TEXT(stored=True),
				shape=TEXT(stored=True),
				durationSecs=NUMERIC(stored=True),
				# RAUSGENOMMEN durationHoursMins=TEXT(stored=True), # eventuell rausnehmen, da Sekunden exakter sind
				comments=TEXT(analyzer=StemmingAnalyzer(), stored=True), # oder Standardanalyzer
				datePosted=ID(stored=True),
				latitude=NUMERIC(float, stored=True),
				longitude=NUMERIC(float, stored=True)
				)
	return schema

def createIndex(name, schema):
   if not os.path.exists(name):
      os.mkdir(name)
   ix = index.create_in(name, schema)
   return ix
    		
def ordne(lines, ix):
	writer = ix.writer()
	for line in lines:
		fields = line.split(",")
		if not fields[5].isdecimal():
			fields[5] = "0"
		if not isfloat(fields[9]):
			fields[9] = "0.0"
		if not isfloat(fields[10]):
			fields[10] = "0.0"
		i = 0
		for field in fields:
			if field == "" and i == 5:
				field = "0" # als default unbekannten Wert (man könnte auch über nan nachdenken?)
			elif field == "" and (i == 9 or i == 10):
				field = "0.0"
			else:
				field = "UNKNOWN"	
			if "&#44" in field:
				field.replace("&#44", "") # contains hässliche HTML Tags
			if "&amp;" in field:
				field.replace("&amp;", "")
			i += 1
		writer.add_document(date = "u"+fields[0],
		                    city = "u"+fields[1],
		                    state = "u"+fields[2],
		                    country = "u"+fields[3],
		                    shape = "u"+fields[4],
		                    durationSecs = fields[5],
		                    # duration in Stunden + Minuten lass ich aus, fields[6]
		                    comments = "u"+fields[7],
		                    datePosted = "u"+fields[8],
		                    latitude = fields[9],
		                    longitude = fields[10])
	writer.commit()
	
def checkNumbers(lines):
	for line in lines:
		fields = line.split(",")
		if not fields[5].isdecimal():
			fields[5] = "0"
		if not isfloat(fields[9]):
			fields[9] = "0.0"
		if not isfloat(fields[10]):
			fields[10] = "0.0"
		
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

if __name__ == "__main__":
	#print(isfloat(".14"))
	#print("0.0".isdecimal())
	txt = lies("scrubbed.csv")
	schema = mkSchema()
	ix = createIndex("ufo_index", schema)
	ordne(txt, ix)
