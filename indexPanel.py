import wx
import xlrd
import template as tem #stworzona podkładka do interfejsu
import indeksy as ind #aplikacja licząca indeksy
import openExcelFunction as openExcel #funkcja do otwierania plików excel
import wx.lib.plot as plot

class indexPanel(wx.Panel):
    """
    Panel służy do wczytywania plików typu excel oraz liczeniu parametrów bioróżnorodności na podstawie danych
    z wybranej kolumny wczytanego pliku.
    """
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent,size=parent.GetSize())
        
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
        self.allButton = tem.guzik(self, "Calculate all", 500, 98)
        self.Bind(wx.EVT_BUTTON, self.calculateAll, self.allButton)
        self.checkBox = tem.check(self, 380, 130, 'has headers')

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
            except:
                pass

            try:
                self.nb.Destroy()
            except:
                pass

            try:
                self.plotter1.Destroy()
            except:
                pass

            try:
                self.plotter2.Destroy()
            except:
                pass

            try:
                self.plotter3.Destroy()
            except:
                pass

            try:
                self.savePlotter1.Destroy()
            except:
                pass

            try:
                self.savePlotter2.Destroy()
            except:
                pass

            try:
                self.savePlotter3.Destroy()
            except:
                pass
            
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
        except:
            pass

        try:
            self.nb.Destroy()
        except:
            pass

        try:
            self.plotter1.Destroy()
        except:
            pass

        try:
            self.plotter2.Destroy()
        except:
            pass

        try:
            self.plotter3.Destroy()
        except:
            pass

        try:
            self.savePlotter1.Destroy()
        except:
            pass

        try:
            self.savePlotter2.Destroy()
        except:
            pass

        try:
            self.savePlotter3.Destroy()
        except:
            pass

        #wpisanie danych z excela w tabelę w aplikacji:
        self.listExcel = tem.lista(self, 30, 400, 600)
        for i in range(self.numberOfColumns):
            self.listExcel.InsertColumn(i, self.choices[i], width = 60)

        self.wektor = list()

        if self.numberOfRows > 30: #ograniczenie widocznych wyników do 30 gdy jest ich więcej
            self.values = 30
        else:
            self.values = self.numberOfRows

        for i in range(self.values):
            self.wektor.append(openExcel.readValues(self.directory,i,self.numberOfColumns))

        for i in self.wektor:
            self.listExcel.Append(i)

        #Tworzenie wykresów zmiany bioróżnorodności:
        #Wykres B-P:
        self.plotter1 = plot.PlotCanvas(self, pos=(700,30))
        self.plotter1.SetInitialSize(size=(600,200))
        self.plotter1.enableLegend = True
        self.plotter1.enableZoom = True
        self.dataBP = list()
        self.marker1 = plot.PolyMarker(self.dataBP, marker='circle', colour='red', legend='Berger-Parker')
        self.gc1 = plot.PlotGraphics([self.marker1], 'The change of Berger-Parker index', 'Column', 'Index value')
        self.plotter1.Draw(self.gc1, xAxis=(int(0),int((self.numberOfColumns))), yAxis=(int(0),int(1)))

        #Guzik do zapisywania wykresu B-P:
        self.savePlotter1 = tem.guzik(self, "", 1300, 190, 40, 40)
        self.Bind(wx.EVT_BUTTON, self.save1, self.savePlotter1)
        self.savePlotter1.SetBitmapLabel(wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_BUTTON))

        #Wykres S-W:
        self.plotter2 = plot.PlotCanvas(self, pos=(700,260))
        self.plotter2.SetInitialSize(size=(600,200))
        self.plotter2.enableLegend = True
        self.plotter2.enableZoom = True
        self.dataSW = list()
        self.marker2 = plot.PolyMarker(self.dataSW, marker='triangle', colour='black', legend='Shannon-Wiener')
        self.gc2 = plot.PlotGraphics([self.marker2], 'The change of Shannon-Wiener index', 'Column', 'Index value')
        self.plotter2.Draw(self.gc2, xAxis=(int(0),int((self.numberOfColumns))))

        #Guzik do zapisywania wykresu S-W:
        self.savePlotter2 = tem.guzik(self, "", 1300, 420, 40, 40)
        self.Bind(wx.EVT_BUTTON, self.save2, self.savePlotter2)
        self.savePlotter2.SetBitmapLabel(wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_BUTTON))

        #Wykres Simpsona:
        self.plotter3 = plot.PlotCanvas(self, pos=(700,490))
        self.plotter3.SetInitialSize(size=(600,200))
        self.plotter3.enableLegend = True
        self.plotter3.enableZoom = True
        self.dataSIM = list()
        self.marker3 = plot.PolyMarker(self.dataSIM, marker='cross', colour='blue', legend='Simpson')
        self.gc3 = plot.PlotGraphics([self.marker3], 'The change of Simpson index', 'Column', 'Index value')
        self.plotter3.Draw(self.gc3, xAxis=(int(0),int((self.numberOfColumns))), yAxis=(int(0),int(1)))

        #Guzik do zapisywania wykresu Simpsona:
        self.savePlotter3 = tem.guzik(self, "", 1300, 650, 40, 40)
        self.Bind(wx.EVT_BUTTON, self.save3, self.savePlotter3)
        self.savePlotter3.SetBitmapLabel(wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_BUTTON))

        #Notebook na wyniki:
        self.nb = wx.Notebook(self, pos=(30,180), size=(500,180), name="Results")

    def calculate(self, e):
        """
        Funkcja obliczająca parametry bioróżnorodności po wybraniu kolumny, z której ma liczyć.
        """
        self.message.SetLabel("")
        self.checkValue = self.checkBox.GetValue()
        self.column = self.choicesBox.GetValue() #pobranie informacji o wybranej kolumnie
        #wyświetlenie informacji o błędzie, gdy nie wybrano żadnej kolumny:
        if (self.column == "" or self.column == None):
            self.message.SetLabel("You need to choose a column")
            return

        #zapisanie wybranych daych w liście:
        self.wybranaKolumna = (ord(self.column) - 65)
        self.listForIndexes = openExcel.readColumns(self.directory, self.wybranaKolumna, self.numberOfRows)
        #usunięcie pierwszego wiersza, gdy jest on nagłówkiem 
        if self.checkValue == True:
            del self.listForIndexes[0]

        self.indexes = ind.indeksy(self.listForIndexes)

        #wyświetlenie komunikatu o błędzie, gdyby w danych jedna wartość lub więcej były puste, stringiem lub zerem
        if ((self.indexes[0] == None) or (self.indexes[0] == -1)):
            self.message.SetLabel("Error, could not calculate indexes. Check your data. It can not have strings, empty fields or negative values")
            return

        #Sprawdzenie czy dla danej kolumny już policzono wynik:
        self.pageCount = self.nb.GetPageCount()
        if self.pageCount > 0:
            for i in range(self.pageCount):
                if self.nb.GetPageText(i) == self.column:
                    return

        #obliczenie indeksów za pomocą napisanego skryptu oraz wyświetlenie wyników w panelu:
        self.tab = wx.Panel(self.nb)
        self.richnessText = tem.tekst(self.tab, 10, 17, "Richness: ", 14)
        self.richness = tem.tekst(self.tab, 180, 20, (" " + str(self.indexes[0]) + " "))
        #self.richness.SetBackgroundColour((255,255,255))
        self.bpText = tem.tekst(self.tab, 10, 47, "Berger-Parker:", 14)
        self.bp = tem.tekst(self.tab, 180, 50, (" " + str(self.indexes[1]) + " "))
        #self.bp.SetBackgroundColour((255,255,255))
        self.dataBP.append((self.wybranaKolumna, self.indexes[1]))
        self.swText = tem.tekst(self.tab, 10, 77, "Shannon-Wiener:", 14)
        self.sw = tem.tekst(self.tab, 180, 80, (" " + str(self.indexes[2]) + "  |  max Value: " + str(self.indexes[4]) + " "))
        #self.sw.SetBackgroundColour((255,255,255))
        self.dataSW.append((self.wybranaKolumna, self.indexes[2]))
        self.simText = tem.tekst(self.tab, 10, 107, "Simpson:", 14)
        self.sim = tem.tekst(self.tab, 180, 110, (" " + str(self.indexes[3]) + " "))
        #self.sim.SetBackgroundColour((255,255,255))
        self.dataSIM.append((self.wybranaKolumna, self.indexes[3]))

        #Dodanie zakładki do panelu Notebook:

        self.nb.AddPage(self.tab, self.column, select=True)

        #Zaktualizowanie wykresów o policzone indeksy:
        self.marker1 = plot.PolyMarker(self.dataBP, marker='circle', colour='red', legend='Berger-Parker')
        self.gc1 = plot.PlotGraphics([self.marker1], 'The change of Berger-Parker index', 'Column', 'Index value')
        self.plotter1.Draw(self.gc1, xAxis=(int(0),int((self.numberOfColumns))), yAxis=(int(0),int(1)))

        self.marker2 = plot.PolyMarker(self.dataSW, marker='triangle', colour='black', legend='Shannon-Wiener')
        self.gc2 = plot.PlotGraphics([self.marker2], 'The change of Shannon-Wiener index', 'Column', 'Index value')
        self.plotter2.Draw(self.gc2, xAxis=(int(0),int((self.numberOfColumns))))

        self.marker3 = plot.PolyMarker(self.dataSIM, marker='cross', colour='blue', legend='Simpson')
        self.gc3 = plot.PlotGraphics([self.marker3], 'The change of Simpson index', 'Column', 'Index value')
        self.plotter3.Draw(self.gc3, xAxis=(int(0),int((self.numberOfColumns))), yAxis=(int(0),int(1)))

    def calculateAll(self, e):
        """
        Funkcja obliczająca parametry bioróżnorodności dla wszystkich możliwych kolumn, z których ma liczyć.
        """
        for i in range(len(self.choices)):
            self.choicesBox.SetSelection(i)
            self.calculate(e)

    def save1(self, e):
        """
        Funkcja zapisuje wykres Bergera-Parkera pod wskazaną nazwą i lokalizacją
        """
        self.plotter1.SaveFile()

    def save2(self, e):
        """
        Funkcja zapisuje wykres Shannona-Wienera pod wskazaną nazwą i lokalizacją
        """
        self.plotter2.SaveFile()

    def save3(self, e):
        """
        Funkcja zapisuje wykres Simpsona pod wskazaną nazwą i lokalizacją
        """
        self.plotter3.SaveFile()

