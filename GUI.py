import wx
import searchingPanel
import indexPanel

class Okno(wx.Frame):
    def __init__ (self,parent,title):
        wx.Frame.__init__(self,parent,title=title)
        self.Maximize()
        self.panel_search = searchingPanel.searchingPanel(self)
        self.panel_search.Hide()
        self.panel_index = indexPanel.indexPanel(self)
        self.panel_index.Hide()

        #MENU
        self.CreateStatusBar()
        menubar = wx.MenuBar()
        menu1 = wx.Menu()
        searching = menu1.Append(wx.ID_ANY, "Search", "Searching in GBIF")
        indexing = menu1.Append(wx.ID_ANY, "Calculator", "Calculate biodiversity indexes")
        pomoc = menu1.Append(wx.ID_ANY, "Help", "How to use this app")
        menubar.Append(menu1,"GBIF")

        self.SetMenuBar(menubar)

        #Przypisanie do menu
        self.Bind(wx.EVT_MENU, self.searching, searching)
        self.Bind(wx.EVT_MENU, self.indexing, indexing)
        self.Bind(wx.EVT_MENU, self.help, pomoc)

    def searching(self, e):
        try:
            self.panel_index.Hide()
        except:
            pass
        self.panel_search.Show()

    def indexing(self, e):
        try:
            self.panel_search.Hide()
        except:
            pass
        self.panel_index.Show()

    def help(self, e):
        try:
            self.panel_search.Hide()
        except:
            pass
        try:
            self.panel_index.Hide()
        except:
            pass


app = wx.App(False)
frame = Okno(None, "GBIF Monitoring v1.0")
frame.Show()
app.MainLoop()
