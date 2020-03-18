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

def lista(self,poz1,poz2,roz1=100,roz2=250,style=wx.LC_REPORT):
    listaCtrl = wx.ListCtrl(self, wx.ID_ANY, pos=(poz1,poz2), size=(roz1,roz2), style=style)
    return listaCtrl
