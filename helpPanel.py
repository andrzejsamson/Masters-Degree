import wx
import template as tem #stworzona podkładka do interfejsu

class helpPanel(wx.Panel):
    """
    Panel wyświetlający pomoc do aplikacji.
    """
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent,size=parent.GetSize())

        #opis działania aplikacji:
        self.pomocTitle = tem.tekst(self, 30, 30, "Pomoc dotycząca działania programu:", 15)
        self.pomocText = tem.tekst(self, 60, 60, " Aplikacja została stworzona do monitorowania bazy danych GBIF oraz obliczania parametrów bioróżnorodności.\n"
                                   " Dzieli się ona na 2 panele:\n"
                                   "\t1. Panel składa się z pola, w którym należy wpisać frazę, jakiej chce się wyszukać w bazie danych. Na podstawie wpisanego tekstu\n"
                                   "\t przeszukana zostanie baza albo według ostatniego wyszukiwania tej frazy w aplikacji, albo po wybraniu odpowiedniego przycisku - po wybranej dacie.\n"
                                   "\t Następnie pojawią się w tabeli rekordy pasujące do wyszukiwanego pola. Gdy jest to pierwsze przeszukanie, wyświetli się 300 najnowszych wpisów.\n"
                                   "\t Im dokładniejsza będzie wpisana fraza, tym również wyniki z bazy będą dokładniejsze. Aby nie przegapić nowych wpisów, należy aplikacji używać\n"
                                   "\t w miarę często, gdyż maksymalna liczba wyszukiwanych wyników to 300. Jeżeli chcemy otrzymywać wyniki dla tej samej rzeczy, należy zawsze wpisywać\n"
                                   "\t identyczną nazwę. Mała zmiana, dopisanie kolejnych liter lub usunięcie niektórych już może wpłynąć na wyszukanie, dlatego też jest traktowane jako\n"
                                   "\t inne zapytanie. Gdy wybierany zostanie z tabeli wyników rekord, można kliknąć przycisk, który spowoduje otwarcie przeglądarki internetowej\n"
                                   "\t na wybranym rekordzie w bazie danych gbif.org. Po każdym przeszukaniu aktualizuje się data ostatniego szukania w bazie aplikacji.\n"
                                   "\t Informacje z wyszukiwania pozostaną tak długo wyświetlone, aż nie zamknie się aplikacji lub nie wykona nowego wyszukania w bazie.\n\n"
                                   "\t2. Drugi panel składa się z przycisku, który każe nam wybrać plik typu Excel i ładuje go do aplikacji. W okienku można mieć podgląd jak wygladają\n"
                                   "\t kolumny w pliku. Następnie po wybraniu odpowiedniej kolumny lub wybraniu opcji, aby policzyć dla wszystkich możliwych kolumn - aplikacja policzy\n"
                                   "\t wybrane parametry określające bioróżnorodność. Po wybraniu zakładek odpowiednich kolumn można przeglądać otrzymane wyniki. Są one również\n"
                                   "\t prezentowane na wykresach znajdujących się po prawej stronie. Po naciśnięciu guzika znajdującego się po prawej stronie wykresu, można go zapisać.\n"
                                   "\t Gdy plik z danymi posiada nagłówki, należy zaznaczyć opcję, aby obliczenia odbywały się bez nich, gdyż nagłówek mógłby zmienić wyniki.\n"
                                   "\t Policzone parametry, wykresy oraz załadowany plik excel pozostaną niezmienne, aż do zamknięcia aplikacji lub nowego wczytania pliku z danymi.\n\n"
                                   " W obu panelach wbudowane są odpowiednie ostrzeżenia, które pojawiają się gdy jakaś czynność wykonywana jest niepoprawnie lub jej wykonanie jest niemożliwe,\n"
                                   " tak jak np. policzenie parmetrów, gdy w komórce pliku z danymi podany będzie tekst lub liczba inna niż ze zbioru liczb naturalnych. Odpowiednie\n"
                                   " ostrzeżenia informują o błedzie jaki się popełniło i można go poprawić.\n\n")
        self.pomocText.SetBackgroundColour((255,255,255))
        self.pomocAutor = tem.tekst(self, 30, 550, "Autor: Andrzej Samson\n"
                                    "Uczelnia: Uniwersytet Przyrodniczy we Wrocławiu\n"
                                    "Kierunek studiów: Bioinformatyka II-stopnia\n"
                                    "Praca magisterska\n"
                                    "Wersja: v1.0")
        self.pomocAutor.SetForegroundColour((50,0,255))
