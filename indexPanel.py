import wx
import xlrd
import template as tem
import indeksy as ind
import openExcelFunction as openExcel

class indexPanel(wx.Frame):
    def __init__(self,parent,title):
        wx.Panel.__init__(self, parent=parent, title=title)
        self.Maximize()
        self.excelFile = tem.tekst(self, 30, 30, "Choose an excel file:", 14)
        self.excelButton = tem.guzik(self, "Excel file", 230, 30)
        self.Bind(wx.EVT_BUTTON, self.readExcel, self.excelButton)
        self.message = tem.tekst(self, 30, 55, "", 10)
        self.message.SetForegroundColour((0,0,255))
        self.chosenFileText = tem.tekst(self, 30, 73, "Chosen file:", 14)
        self.chosenFile = tem.tekst(self, 150, 75, "")
        self.chosenFile.SetForegroundColour((50,0,255))
        self.chosenFile.SetBackgroundColour((255,255,255))
        self.choicesText = tem.tekst(self, 30, 98, "Choose the column with data:", 14)
        self.choices = [""]
        self.choicesBox = tem.box(self, 300, 100, self.choices, roz1 = 50, style = wx.CB_DROPDOWN | wx.CB_READONLY)
        self.indexButton = tem.guzik(self, "Calculate", 370, 98)
        self.Bind(wx.EVT_BUTTON, self.calculate, self.indexButton)

    def readExcel(self, e):
        self.message.SetLabel("")
        self.directory = ""
        self.file = ""
        self.choices = [""]
        self.dialog = wx.FileDialog(self, 'Open File', self.directory, self.file, wildcard="Arkusze (*.xlsx;*.xlsm;*.xlsb;*.xls)|*.xlsx;*.xlsm;*.xlsb;*.xls|All files (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if self.dialog.ShowModal() == wx.ID_CANCEL:
            self.message.SetLabel("You need to choose a file")
            self.chosenFile.SetLabel("")
            self.choicesBox.SetItems(self.choices)
            try:
                self.listExcel.Destroy()
                self.richnessText.Destroy()
                self.richness.Destroy()
                self.bpText.Destroy()
                self.bp.Destroy()
                self.swText.Destroy()
                self.sw.Destroy()
                self.simText.Destroy()
                self.sim.Destroy()
                return
            except:
                return
        
        self.directory = self.dialog.GetPath()
        self.file = self.dialog.GetFilename()
        self.chosenFile.SetLabel(" " + self.file + " ")
        self.choices.clear()
        self.numberOfColumns, self.numberOfRows = openExcel.openFile(self.directory)
        if self.numberOfColumns == 0:
            self.choices = [""]
        else:
            for i in range(self.numberOfColumns):
                self.letter = chr(i+65)
                self.choices.append(self.letter)
        self.choicesBox.SetItems(self.choices)
        
        try:
            self.listExcel.Destroy()
            self.richnessText.Destroy()
            self.richness.Destroy()
            self.bpText.Destroy()
            self.bp.Destroy()
            self.swText.Destroy()
            self.sw.Destroy()
            self.simText.Destroy()
            self.sim.Destroy()
        except:
            pass
        
        self.listExcel = tem.lista(self, 30, 200, (100 + (50*self.numberOfColumns)))
        for i in range(self.numberOfColumns):
            self.listExcel.InsertColumn(i, self.choices[i], width = (self.listExcel.GetSize()[0] / self.numberOfColumns))

        self.wektor = list()
        for i in range(self.numberOfRows):
            self.wektor.append(openExcel.readValues(self.directory,i,self.numberOfColumns))

        for i in self.wektor:
            self.listExcel.Append(i)

    def calculate(self, e):
        self.message.SetLabel("")
        self.column = self.choicesBox.GetValue()
        if (self.column == "" or self.column == None):
            self.message.SetLabel("You need to choose a column")
            try:
                self.richnessText.Destroy()
                self.richness.Destroy()
                self.bpText.Destroy()
                self.bp.Destroy()
                self.swText.Destroy()
                self.sw.Destroy()
                self.simText.Destroy()
                self.sim.Destroy()
                return
            except:
                return

        self.listForIndexes = openExcel.readColumns(self.directory, (ord(self.column) - 65), self.numberOfRows)
        if isinstance(self.listForIndexes[0], str):
            self.message.SetLabel("Chosen data can not be a string")
            try:
                self.richnessText.Destroy()
                self.richness.Destroy()
                self.bpText.Destroy()
                self.bp.Destroy()
                self.swText.Destroy()
                self.sw.Destroy()
                self.simText.Destroy()
                self.sim.Destroy()
                return
            except:
                return

        self.indexes = ind.indeksy(self.listForIndexes)

        try:
            self.richnessText.Destroy()
            self.richness.Destroy()
            self.bpText.Destroy()
            self.bp.Destroy()
            self.swText.Destroy()
            self.sw.Destroy()
            self.simText.Destroy()
            self.sim.Destroy()
        except:
            pass

        if self.indexes[0] == None:
            self.message.SetLabel("Error, could not calculate indexes. Check your data")
            return
        
        self.richnessText = tem.tekst(self, (self.listExcel.GetSize()[0] + 100), 247, "Richness: ", 14)
        self.richness = tem.tekst(self, (self.listExcel.GetSize()[0] + 270), 250, (" " + str(self.indexes[0]) + " "))
        self.richness.SetBackgroundColour((255,255,255))
        self.bpText = tem.tekst(self, (self.listExcel.GetSize()[0] + 100), 277, "Berger-Parker:", 14)
        self.bp = tem.tekst(self, (self.listExcel.GetSize()[0] + 270), 280, (" " + str(self.indexes[1]) + " "))
        self.bp.SetBackgroundColour((255,255,255))
        self.swText = tem.tekst(self, (self.listExcel.GetSize()[0] + 100), 307, "Shannon-Wiener:", 14)
        self.sw = tem.tekst(self, (self.listExcel.GetSize()[0] + 270), 310, (" " + str(self.indexes[2]) + " "))
        self.sw.SetBackgroundColour((255,255,255))
        self.simText = tem.tekst(self, (self.listExcel.GetSize()[0] + 100), 337, "Simpson:", 14)
        self.sim = tem.tekst(self, (self.listExcel.GetSize()[0] + 270), 340, (" " + str(self.indexes[3]) + " "))
        self.sim.SetBackgroundColour((255,255,255))


app = wx.App(False)
frame = indexPanel(None, "GBIF index v1.0")
frame.Show()
app.MainLoop()
