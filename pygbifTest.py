from pygbif import species as species
from pygbif import occurrences as occ
import datetime

def searching(name, myDate):
    now = datetime.datetime.now().strftime("%Y-%m-%d")

    x = occ.search(q=name, eventDate=(myDate+','+now))

    dane = (x['results'])
    limit = len(dane)

    wektor = list()
    listOfKeys = list()

    for i in range(limit):
        country = None
        scientificName = None
        eventDate = None
        recordedBy = None
        try:
            country = dane[i]['country']
        except:
            pass
        try:
            scientificName = dane[i]['scientificName']
        except:
            pass
        try:
            eventDate = dane[i]['eventDate']
        except:
            pass
        try:
            recordedBy = dane[i]['recordedBy']
        except:
            pass
        listOfKeys.append(dane[i]['key'])
        wektor.append((i+1,country,scientificName,eventDate,recordedBy))

    return wektor, listOfKeys
