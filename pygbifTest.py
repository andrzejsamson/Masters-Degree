from pygbif import species as species
from pygbif import occurrences as occ

#Wyświetlanie liczby rekordów:
"""
splist = ['Cyanocitta stelleri', 'Junco hyemalis', 'Aix sponsa',
'Ursus americanus', 'Pinus contorta', 'Poa annuus']

keys = [ species.name_backbone(x)['usageKey'] for x in splist ]
out = [ occ.search(taxonKey = x, limit=0)['count'] for x in keys ]

x = dict(zip(splist, out))
print(sorted(x.items(), key=lambda z:z[1], reverse=True))
"""
##############################################################

x = occ.search(q="Riethia Pantera", limit=2)
#print(x)

dane = (x['results'])
print(dane[0]['country'])
print(dane[0]['scientificName'])
print(dane[0]['eventDate'])
print(dane[0]['recordedBy'])
