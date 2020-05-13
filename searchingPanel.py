import wx
import template as tem #skrypt ułatwiający tworzenie interfejsu
import zapisDoBazy as zapis #skrypt, zapisujący wyszukiwane zagadnienie do bazy danych
import wczytywanieBazy as wczyt #skrypt wczytujący z bazy danych kiedy ostatni raz wyszukiwano zagadnienia
import pygbifTest as gbifSearch #skrypt obsługujący łączenie się z baza GBIF
import datetime #pakiet potrzebny do pobrania aktualnej daty
import webbrowser #pakiet do wyszukiwania wybranego artykułu w bazie gbif

class searchingPanel(wx.Frame):
    """
    Panel ma na celu przeszukiwać bazę GBIF.org na podstawie wpisanej frazy. Najpierw sprawdza w
    bazie danych tej aplikacji czy taka fraza była już wyszukiwana. Jeżeli tak, pokazuje wyniki
    od czasu ostatniego wyszukiwania. Jeżeli jest to pierwsze wyszukiwanie, to pokazuje wyniki
    z ostatnich 60 dni. Limit wyszukanych rekordów to 300 (ograniczenie narzucone przez funkcję).
    Wyświetla wszystkei wyniki szeregując je od najmłodszego na górze. Kiedy zaznaczy się rekord,
    można nacisnąć guzik i zostanie otwarta przeglądarka internetowa wraz ze stroną dla tego rekordu
    w GBIF.org
    """
    def __init__(self,parent,title):
        wx.Panel.__init__(self, parent=parent, title=title)
        self.Maximize()
        #Wygląd panelu:
        self.searchingTekst = tem.tekst(self, 30, 28, "Enter what you want to search:", 14)
        self.searchingField = tem.pole(self, 300, 30)
        self.Bind(wx.EVT_TEXT_ENTER, self.onEnter, self.searchingField)
        self.searchingButton = tem.guzik(self, "Search by last", 460, 28, 150)
        self.Bind(wx.EVT_BUTTON, self.search ,self.searchingButton)
        self.searchByDateTekst = tem.tekst(self, 630, 28, "or choose a date:", 14)
        self.dateToSearch = tem.data(self, 800, 28)
        self.searchingByDate = tem.guzik(self, "Search by date", 900, 28, 150)
        self.Bind(wx.EVT_BUTTON, self.searchByDate, self.searchingByDate)
        self.message = tem.tekst(self, 30, 55, "", 10)
        self.message.SetForegroundColour((0,0,255))
        self.searchedFraseTekst = tem.tekst(self, 30, 97, "Searched Item:", 14)
        self.searchedFrase = tem.tekst(self, 170, 100, "")
        self.searchedFrase.SetForegroundColour((50,0,255))
        self.searchedFrase.SetBackgroundColour((255,255,255))
        self.searchedDateTekst = tem.tekst(self, 30, 117, "Last searching:", 14)
        self.searchedDate = tem.tekst(self, 170, 120, "")
        self.searchedDate.SetForegroundColour((50,0,255))
        self.searchedDate.SetBackgroundColour((255,255,255))
        self.roz1 = self.GetSize()[0]
        self.listSearched = tem.lista(self, 30, 200, (self.roz1-70), 450)
        self.listSize = self.listSearched.GetSize()[0]
        self.listSearched.InsertColumn(0, "Key:", wx.LIST_FORMAT_CENTER, width=(self.listSize*0.15))
        self.listSearched.InsertColumn(1, "Country:", wx.LIST_FORMAT_CENTER, width=(self.listSize*0.15))
        self.listSearched.InsertColumn(2, "Scientific name:", wx.LIST_FORMAT_CENTER, width=(self.listSize*0.35))
        self.listSearched.InsertColumn(3, "Date:", wx.LIST_FORMAT_CENTER, width=(self.listSize*0.12))
        self.listSearched.InsertColumn(4, "Recorded by:", wx.LIST_FORMAT_CENTER, width=(self.listSize*0.23))
        self.browserButton = tem.guzik(self, "Go to website", 30, 158)
        self.Bind(wx.EVT_BUTTON, self.goToWebsite, self.browserButton)
        self.browserMessage = tem.tekst(self, 150, 162, "", 10)
        self.browserMessage.SetForegroundColour((0,0,255))

    def onEnter(self, e):
        #Funkcja włącza się nie tylko po wcisnięciu guzika, ale również po wciśnięciu 'Enter' w polu tekstowym
        self.search(e)

    def search(self, e):
        """
        Funkcja która szuka rekordów w bazie. Najpierw przeszukuje bazę aplikacji czy fraza była
        już wyszukiwana. Wyświetla błędy, gdy pole do wyszukiwania jest puste
        """
        self.last60Days = (datetime.datetime.now()-datetime.timedelta(60)).strftime("%Y-%m-%d") #zapisanie daty z 60 dni temu
        #czyszczenie wiadomości:
        self.message.SetLabel("")
        self.searchedFrase.SetLabel("")
        self.searchedDate.SetLabel("")
        self.browserMessage.SetLabel("")
        
        self.searchedItem = self.searchingField.GetValue() #zapisanie wyszukiwanej frazy
        try:
            self.listSearched.DeleteAllItems() #wyczyszczenie poprzednich wyszukiwań z tabeli
        except:
            pass
        if self.searchedItem == "":
            self.message.SetLabel("You need to enter an item in the field to search") #wyświetlenie błędu, gdy nic nie będzie wpisane
        else:
            #wczytywanie słowa z bazy danych oraz zapisanie do bazy wyszukania. Wyświtlenie wyników w tabeli
            self.searchedWord = wczyt.wczytanie(self.searchedItem)
            zapis.zapis(self.searchedItem)
            self.searchedFrase.SetLabel(" " + self.searchedItem + " ")
            if self.searchedWord != None:
                self.searchedDate.SetLabel(" " + self.searchedWord + " ")
                self.dataTable = gbifSearch.searching(self.searchedItem, self.searchedWord)
                for i in self.dataTable:
                    self.listSearched.Append(i)
            else:
                self.searchedDate.SetLabel(" First searching - max. 300 results from last 60 days ")
                self.dataTable = gbifSearch.searching(self.searchedItem, self.last60Days)
                for i in self.dataTable:
                    self.listSearched.Append(i)

    def searchByDate(self, e):
        """
        Funckja podobna do funkcji search, jednak wyszukuje frazę na podstawie wybranej daty, a nie ostatniego wyszukiwania
        """
        self.chosenDate = self.dateToSearch.GetValue() #zapisanie wybranej daty
        self.chosenDateStr = (str(self.chosenDate)[0:10]) #zamiana wyniku w string
        self.d = datetime.datetime(int(self.chosenDateStr[6:10]), int(self.chosenDateStr[3:5]), int(self.chosenDateStr[0:2])) #zamiana stringu w date
        self.x = self.d.strftime("%Y-%m-%d") #potrzebny format do funkcji
        
        #czyszczenie wiadomości:
        self.message.SetLabel("")
        self.searchedFrase.SetLabel("")
        self.searchedDate.SetLabel("")
        self.browserMessage.SetLabel("")
        self.searchedItem = self.searchingField.GetValue() #zapisanie wyszukiwanej frazy
        try:
            self.listSearched.DeleteAllItems() #wyczyszczenie poprzednich wyszukiwań z tabeli
        except:
            pass
        if self.searchedItem == "":
            self.message.SetLabel("You need to enter an item in the field to search") #wyświetlenie błędu, gdy nic nie będzie wpisane
        else:
            #wczytywanie słowa z bazy danych oraz zapisanie do bazy wyszukania. Wyświtlenie wyników w tabeli
            self.searchedWord = wczyt.wczytanie(self.searchedItem)
            zapis.zapis(self.searchedItem)
            self.searchedFrase.SetLabel(" " + self.searchedItem + " ")
            if self.searchedWord != None:
                self.searchedDate.SetLabel(" " + self.searchedWord + " ")
                self.dataTable = gbifSearch.searching(self.searchedItem, self.x)
                for i in self.dataTable:
                    self.listSearched.Append(i)
            else:
                self.searchedDate.SetLabel(" First searching - max. 300 results ")
                self.dataTable = gbifSearch.searching(self.searchedItem, self.x)
                for i in self.dataTable:
                    self.listSearched.Append(i)

    def goToWebsite(self, e):
        """
        Po wybraniu rekordu funkcja ta otwiera stronę rekordu w gbif.org w przeglądarce
        """
        self.browserMessage.SetLabel("")
        self.myChoice = self.listSearched.GetFirstSelected()
        if self.myChoice == -1:
            self.browserMessage.SetLabel("You need to choose an item from the list") #wyświetlenie błędu gdy nie wybrano rekordu
            return
        webbrowser.open(('http://gbif.org/occurrence/'+str(self.dataTable[self.myChoice][0])), new=2)


app = wx.App(False)
frame = searchingPanel(None, "GBIF Monitoring v1.0")
frame.Show()
app.MainLoop()
