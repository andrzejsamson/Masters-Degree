import math

def indeksy(lista):
    #Sprawdzenie czy podany argument jest listą:
    if type(lista) != list:
        return "Podany argument musi być listą"
    try:
        maxValue = max(lista) #maksymalna liczebność gatunku w populacji
        liczebnosc = 0
        rich = 0 #Bogactwo gatunkowe
        for i in lista:
            if i < 0:
                return -1, -1, -1, -1, -1
            if i == 0:
                liczebnosc = liczebnosc #gdy liczebność gatunku wynosi 0 nie jest on wliczany do liczebności
                rich = rich #gdy liczebność gatunku wynosi 0 nie jest on wliczany do bogactwa gatunkowego
            else:
                liczebnosc = liczebnosc + i #obliczenie liczebności całej populacji
                rich = rich + 1 #obliczenie ilości gatunków na obszarze, czyli indeks bogactwa gatunkowego
        
        #Indeks Bergera-Parkera:
        bp = maxValue/liczebnosc

        #Indeks Shannona-Wienera:
        sw = 0
        for i in lista:
            if i == 0:
                sw = sw
            else:
                value = i/liczebnosc
                sw = sw + (value * math.log(value))
        sw = sw * (-1)

        #maksymalna wartość indeksu Shannona-Wienera:
        maxSW = math.log(rich)

        #Indeks Simpsona:
        sim = 0
        for i in lista:
            sim = sim + (i * (i - 1))
        if liczebnosc <= 1:
            sim = 0
        else:
            sim = sim / (liczebnosc * (liczebnosc - 1))

        #Zwrócenie wyników indeksów:
        return rich, round(bp,5), round(sw,5), round(sim,5), round(maxSW,5)
    except: #w razie niepowodzenia (gdy w komórce będzie tekst):
        return None, None, None, None, None
