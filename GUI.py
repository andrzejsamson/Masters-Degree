import wx
import searchingPanel

class Okno(wx.Frame):
    def __init__ (self,parent,title):
        wx.Frame.__init__(self,parent,title=title)
        self.Maximize()
        self.panel = searchingPanel.Panel(self)


app = wx.App(False)
frame = Okno(None, "GBIF Monitoring v1.0")
frame.Show()
app.MainLoop()
