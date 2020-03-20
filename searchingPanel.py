import wx
import template as tem
import zapisDoBazy as zapis
import wczytywanieBazy as wczyt

class searchingPanel(wx.Frame):
    def __init__(self,parent,title):
        wx.Panel.__init__(self, parent=parent, title=title)
        self.Maximize()
        self.searchingTekst = tem.tekst(self, 30, 28, "Enter what you want to search:", 14)
        self.searchingField = tem.pole(self, 300, 30)
        self.Bind(wx.EVT_TEXT_ENTER, self.onEnter, self.searchingField)
        self.searchingButton = tem.guzik(self, "Search", 460, 28)
        self.Bind(wx.EVT_BUTTON, self.search ,self.searchingButton)
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
        self.listSearched = tem.lista(self, 30, 200, (self.roz1-70), 300)
        self.listSize = self.listSearched.GetSize()[0]
        self.listSearched.InsertColumn(0, "LP:", wx.LIST_FORMAT_CENTER, width=(self.listSize*0.03))
        self.listSearched.InsertColumn(1, "Region:", wx.LIST_FORMAT_CENTER, width=(self.listSize*0.2))
        self.listSearched.InsertColumn(2, "Nazwa:", wx.LIST_FORMAT_CENTER, width=(self.listSize*0.47))
        self.listSearched.InsertColumn(3, "Data:", wx.LIST_FORMAT_CENTER, width=(self.listSize*0.1))
        self.listSearched.InsertColumn(4, "Wydawca:", wx.LIST_FORMAT_CENTER, width=(self.listSize*0.2))

    def onEnter(self, e):
        self.search(e)

    def search(self, e):
        self.message.SetLabel("")
        self.searchedFrase.SetLabel("")
        self.searchedDate.SetLabel("")
        self.searchedItem = self.searchingField.GetValue()
        if self.searchedItem == "":
            self.message.SetLabel("You need to enter an item in the field to search")
        else:
            self.searchedWord = wczyt.wczytanie(self.searchedItem)
            zapis.zapis(self.searchedItem)
            self.searchedFrase.SetLabel(" " + self.searchedItem + " ")
            if self.searchedWord != None:
                self.searchedDate.SetLabel(" " + self.searchedWord + " ")
            else:
                self.searchedDate.SetLabel(" First searching ")

app = wx.App(False)
frame = searchingPanel(None, "GBIF Monitoring v1.0")
frame.Show()
app.MainLoop()
