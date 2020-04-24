from pygbif import occurrences as occ #pakiet do łączenia sie z bazą gbif przez język python
import datetime

def searching(name, myDate):
    now = datetime.datetime.now().strftime("%Y-%m-%d") #pobranie aktualnej daty

    x = occ.search(q=name, eventDate=(myDate+','+now)) #wyszukanie frazy od daty do teraz

    dane = (x['results']) #zapisanie danych
    limit = len(dane)

    wektor = list() #wektor przechowujacy rekordy

    for i in range(limit):
        #zapisanie potrzebnych informacji z danych do list
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
        dataKey = dane[i]['key']
        wektor.append((dataKey,country,scientificName,eventDate,recordedBy)) #połączenie wyników z list do jednej listy

    wektor.sort(key=takeDate,reverse=True) #poszeregowanie zmiennych po dacie, od daty najwcześniejszej
    return wektor

def takeDate(elem):
    #funkcja potrzebna do szeregowania rekordów po dacie
    return elem[3]
