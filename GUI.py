import wx

def tekst(self,poz1,poz2,napis,font=12):
    staticText = wx.StaticText(self, wx.ID_ANY, pos=(poz1,poz2), label=napis)
    rozmiar = wx.Font(font, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
    staticText.SetFont(rozmiar)
    return staticText

def pole(self,poz1,poz2,roz1=150,roz2=20,style=wx.TE_PROCESS_ENTER):
    tekstCtrl = wx.TextCtrl(self, wx.ID_ANY, pos=(poz1,poz2), size=(roz1,roz2), style=style)
    return tekstCtrl

def box(self,poz1,poz2,wybory,roz1=150,roz2=20,style=wx.CB_DROPDOWN):
    comboBox = wx.ComboBox(self, wx.ID_ANY, pos=(poz1,poz2), size=(roz1,roz2), choices=wybory, style=style)
    return comboBox

def guzik(self,napis,poz1,poz2,roz1=100,roz2=25,font=12):
    button = wx.Button(self, label=napis, pos=(poz1,poz2), size=(roz1,roz2))
    rozmiar = wx.Font(font, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
    button.SetFont(rozmiar)
    return button

class Panel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent, size=parent.GetSize())
        self.tekst = tekst(self, 10, 10, "Test")
        self.pole1 = pole(self, 30, 40)
        self.pole2 = pole(self, 30, 70)
        wybory = ["test", "czy", "działa"]
        self.box = box(self, 30, 100, wybory)
        self.guzik = guzik(self, "guzik", 200, 100)

class Okno(wx.Frame):
    def __init__ (self,parent,title):
        wx.Frame.__init__(self,parent,title=title)
        self.Maximize()
        self.panel = Panel(self)


app = wx.App(False)
frame = Okno(None, "Tytuł")
frame.Show()
app.MainLoop()
