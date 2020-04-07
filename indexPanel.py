import wx
import xlrd
import template as tem #stworzona podkładka do interfejsu
import indeksy as ind #aplikacja licząca indeksy
import openExcelFunction as openExcel #funkcja do otwierania plików excel

class indexPanel(wx.Frame):
    """
    Panel służy do wczytywania plików typu excel oraz liczeniu parametrów bioróżnorodności na podstawie danych
    z wybranej kolumny wczytanego pliku.
    """
    def __init__(self,parent,title):
        wx.Panel.__init__(self, parent=parent, title=title)
        self.Maximize() #okno na cały ekran

        #wygląd panelu:
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
        """
        Funkcja czytająca plik excel. Uruchamia się po kliknięciu guzika 'Excel file'. Otwiera się okno, w którym należy wybrać
        plik typu excel. Gdy nie wybierze się pliku pojawi się informacja o błędzie oraz nie będzie można wykonywać dalszych
        funkcji panelu. FUnkcja korzysta z napisanego skryptu 'openExcelFunction.py'. Gdy plik zostanie wczytany poprawnie,
        informacje z niego pojawią się w tabeli w panelu.
        """
        #czyszczenie informacji:
        self.message.SetLabel("")
        self.directory = ""
        self.file = ""
        self.choices = [""]

        #wybieranie pliku excel:
        self.dialog = wx.FileDialog(self, 'Open File', self.directory, self.file, wildcard="Arkusze (*.xlsx;*.xlsm;*.xlsb;*.xls)|*.xlsx;*.xlsm;*.xlsb;*.xls", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        #wildcard ogranicza wybranie pliku tylko typu excel
        #zapisanie wybranego pliku do zmiennej, gdy się wyjdzie bez wyboru - pojawi się błąd
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

        #zapisanie ścieżki i nazwy pliku:
        self.directory = self.dialog.GetPath()
        self.file = self.dialog.GetFilename()
        self.chosenFile.SetLabel(" " + self.file + " ")
        self.choices.clear()

        #otwarcie pliku excel oraz dodanie kolumn do wyboru
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

        #wpisanie danych z excela w tabelę w aplikacji:
        self.listExcel = tem.lista(self, 30, 200, (100 + (50*self.numberOfColumns)))
        for i in range(self.numberOfColumns):
            self.listExcel.InsertColumn(i, self.choices[i], width = (self.listExcel.GetSize()[0] / self.numberOfColumns))

        self.wektor = list()
        for i in range(self.numberOfRows):
            self.wektor.append(openExcel.readValues(self.directory,i,self.numberOfColumns))

        for i in self.wektor:
            self.listExcel.Append(i)

    def calculate(self, e):
        """
        Funkcja obliczająca parametry bioróznorodności po wybraniu kolumny, z której ma liczyć.
        """
        self.message.SetLabel("")
        self.column = self.choicesBox.GetValue() #pobranie informacji o wybranej kolumnie
        #wyświetlenie informacji o błędzie, gdy nie wybrano żadnej kolumny:
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

        #zapisanie wybranych daych w liście:
        self.listForIndexes = openExcel.readColumns(self.directory, (ord(self.column) - 65), self.numberOfRows)
        #komunikat o błędzie, gdyby w wybranej kolumnie były nazwy zamiast liczb lub kolumna byłaby pusta
        if isinstance(self.listForIndexes[0], str):
            self.message.SetLabel("Chosen data can not be a string or empty")
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

        #wyświetlenie komunikatu o błędzie, gdyby w danych jedna wartość lub więcej były puste, stringiem lub zerem
        if ((self.indexes[0] == None) or (self.indexes[0] == -1)):
            self.message.SetLabel("Error, could not calculate indexes. Check your data. It can not have strings or 0")
            return

        #obliczenie indeksów za pomocą napisanego skryptu oraz wyświetlenie wyników w panelu:
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
