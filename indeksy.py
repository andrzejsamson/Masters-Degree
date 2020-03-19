import math

def indeksy(lista):
    #Sprawdzenie czy podany argument jest listą:
    if type(lista) != list:
        return "Podany argument musi być listą"
    try:
        maxValue = max(lista) #maksymalna liczebność gatunku w populacji
        liczebnosc = 0
        for i in lista:
            liczebnosc = liczebnosc + i #obliczenie liczebności całej populacji

        #Bogactwo gatunkowe (liczba gatunków):
        rich = len(lista)
        
        #Indeks Bergera-Parkera:
        bp = maxValue/liczebnosc

        #Indeks Shannona-Wienera:
        sw = 0
        for i in lista:
            value = i/liczebnosc
            sw = sw + (value * math.log(value))
        sw = sw * (-1)

        #Indeks Simpsona:
        sim = 0
        for i in lista:
            sim = sim + (i * (i - 1))
        sim = sim / (liczebnosc * (liczebnosc - 1))

        #Zwrócenie wyników indeksów:
        return rich, bp, sw, sim
    except:
        return None, None, None, None
