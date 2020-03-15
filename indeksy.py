import math

def indeksy(lista):
    #Sprawdzenie czy podany argument jest listą:
    if type(lista) != list:
        return "Podany argument musi być listą"
    maxValue = max(lista) #maksymalna wartosc w populacji
    liczebnosc = 0
    for i in lista:
        liczebnosc = liczebnosc + i #obliczenie liczebności populacji
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
    return bp, sw, sim
