# ========================================================================== #
#               -----   xlsx_Mngr.py   -----                                 #
#              class  for  xlsx file managiging                              #
# ========================================================================== #

# import sqlite3
# from openpyxl import load_workbook
import pandas as pd
import numpy as np
import warnings
from Data_Classes.Codes_DB import *

class Xlsx_Manager(Codes_db):
    def __init__(self):
        super().__init__()

        #ignore  : warn("Workbook contains no stylesheet, using openpyxl's defaults")
        warnings.simplefilter("ignore")

        self.Dummy   = 0

        # one row on xlsx file   ---------------------------------------------------------------
        #  nRow timeContab timeValuta  Des1  Accred  Addeb  Des2

        self._nRow   = None     # int
        self._Contab = None     # str
        self._Valuta = None     # str
        self._Des1   = None     # str
        self._Accr   = None     # float
        self._Addeb  = None     # float
        self._Des2   = None     # str

        # self._df: pd.DataFrame | None = None      da' warning
        self._df: pd.DataFrame  # Si dichiara qui che self,_df e' tipo pd.DataFrame per il load di xlsx

        # ------------------------             A      B      C      D      E     F  ---------------
        self._Xlsx_Rows_From_Sheet     = []  # _Contab _Valuta _Des1 Accred _Addeb _Des2
        self._Xlsx_Rows_Desc_Compact   = []  #   ""     ""     comp     ""    ""   comp
        self._Xlsx_Rows_Compact        = []  # _Contab _Valuta Accrd  _Addeb  Full_Desc
        # ------------------------
        self._Tot_Rows        = 0
        self._Tot_NOK         = 0
        self._Tot_OK          = 0
        self._TotWith_Code    = 0
        self._TotWihtout_Code = 0
        self._iYear_List      = []

        # -------   _tAtt : temporary attributes  that will be copied on _Att  if all OK  -------------
        self._tXLSX_Rows_From_Sheet    = []
        self._tXLSX_Rows_Desc_Compact  = []
        self._tXlsx_Rows_Compact       = []

        self._tWith_Code_Tree_List     = []
        self._tWihtout_Code_Tree_List  = []

        self._With_Code_Tree_List    = []
        self._Wihtout_Code_Tree_List = []
        self._Records_ToInsert_List  = []

        # ------------------------
        self._tTot_Rows        = 0
        self._tTot_OK          = 0
        self._tTot_NOK         = 0
        self._tTotWith_Code    = 0
        self._tTotWithout_Code = 0
        self._tiYear_List      = []
        # -----------------------------------------------------------------------------------------
        self._tXlsx_Conto    = None  # these attributs are not saved on Selections
        self._tXlsx_Year     = None  # calculated in _Set_Xlsx_Conto_Year_Month()
        self._tXlsx_Month    = None  #    """      "     """      """

        self._Xlsx_Month_Contab_List         = []
        self._Xlsx_Month_Valuta_List         = []
        self._Xlsx_Month_Generic_Valuta_List = []
        self._Xlsx_Month_Generic_Contab_List = []

        # ------------------------------------------------------------ #
        #  -----  the values  are filled  from  Transact_DB.py  ------ #
        #   but they MUST be here because they are used inside here    #
        self._tTransact_Year   = None
        self._tTransact_Table  = []
        # ------------------------------------------------------------ #

        self._Transact_Filename              = ""
        self._Db_Transact_Database           = []
        self.Fetched_List                    = []

    # ----------------------------------------------------------------------------------- #
    #            ----------------      public   methods   -----------------               #
    # ----------------------------------------------------------------------------------- #
    def Get_Total_Rows(self):
        # IX_TOT_ROWS_OK, IX_TOT_ROWS_WITH_CODE, IX_TOT_ROWS_WITHOUT_CODE
        return [self._Tot_OK, self._TotWith_Code, self._TotWihtout_Code]

    # ------------------------------------------------------------------------------------
    def Get_Length_Xlsx(self):
        return len(self._Xlsx_Rows_From_Sheet)

    # -------------------------------------------------------------------------------------
    def Get_WithCodeList(self):
        return self._With_Code_Tree_List

    # -------------------------------------------------------------------------------------
    def Get_WithoutCodeList(self):
        return self._Wihtout_Code_Tree_List

    def Get_Xlsx_Rows_From_Sheet(self):
        return self._Xlsx_Rows_From_Sheet

    def Clear_Xlsx_Conto_Year_Month(self):
        self._tXlsx_Conto = None
        self._tXlsx_Year  = None
        self._tXlsx_Month = None

    # --------------------------------------------------------------------------------------------
    def _Set_Xlsx_Conto_Year_Month(self):
        Filename = self.Get_sel_dictionary_value(XLSX_FILENAME)
        self._tXlsx_Conto = None
        self._tXlsx_Year = None
        self._tXlsx_Month = None
        FullFilename = Filename
        if FullFilename != UNKNOWN:
            filename = Get_File_Name(FullFilename)
            self._tXlsx_Conto = filename[0:5]
            self._tXlsx_Year = int(filename[6:10])
            self._tXlsx_Month = int(filename[11:13])
        pass

    # --------------------------------------------------------------------------------------------
    def _Init_Xlsx_Data(self):
        self._tXLSX_Rows_From_Sheet   = []  # nRow  _Contab  _Valuta  _Des1     _Accr   _Addeb     _Des2
        self._tXLSX_Rows_Desc_Compact = []  # nRow  _Contab  _Valuta  Des1Comp _Accr   _Addeb     Des2Comp
        self._tXlsx_Rows_Compact      = []  # nROw  _Contab  _Valuta  _Accr     _Addeb  Full_Desc

        self._tWith_Code_Tree_List    = []  # nRow Contabile _Valuta Accred _Addeb TRdesc TRcode
        self._tWihtout_Code_Tree_List = []  # nRow Contabile _Valuta Accred _Addeb FullDesc

        # ------------------------
        self._tTot_Rows        = 0
        self._tTot_OK          = 0
        self._tTot_NOK         = 0
        self._tTotWith_Code    = 0
        self._tTotWithout_Code = 0
        self._tiYear_List = []

        # -----------------------------------------------------------------------------------------
        self._tXlsx_Conto    = None  # or on selecting new file  FIDEU_2024_01.xlsx
        self._tXlsx_Year     = None  # they are  calculated on startup
        self._tXlsx_Month    = None

    # --------------------------------------------------------------------------------------------
    def _Save_Xlsx_Data(self):
        self._Xlsx_Rows_From_Sheet   = self._tXLSX_Rows_From_Sheet
        self._Xlsx_Rows_Desc_Compact = self._tXLSX_Rows_Desc_Compact
        self._Xlsx_Rows_Compact      = self._tXlsx_Rows_Compact

        # ------------------------
        self._Tot_Rows        = self._tTot_Rows
        self._Tot_OK          = self._tTot_OK
        self._Tot_NOK         = self._tTot_NOK
        self._TotWith_Code    = self._tTotWith_Code
        self._TotWihtout_Code = self._tTotWithout_Code
        self._iYear_List      = self._tiYear_List

        self._Xlsx_Conto = self._tXlsx_Conto
        self._Xlsx_Year  = self._tXlsx_Year
        self._Xlsx_Month = self._tXlsx_Month

        self._With_Code_Tree_List    = self._tWith_Code_Tree_List
        self._Wihtout_Code_Tree_List = self._tWihtout_Code_Tree_List


    # --------------------------------------------------------------------------------------- #
    #             *****         Get rows from sheet           *****                           #
    #         Create:       self._Xlsx_Rows_From_Sheet                                        #
    #                       self._Xlsx_Rows_Desc_Compact                                      #
    #                       self._Xlsx_Rows_Compact                                           #
    # --------------------------------------------------------------------------------------- #
    @property
    def  Load_Xlsx_Rows(self) -> tuple[bool, str | list]:
        self._Init_Xlsx_Data()
        Filename = self.Get_sel_dictionary_value(XLSX_FILENAME)
        if not Gl_Cek_Xlsx_Name(Filename):
            return False, "FATAL ERROR 12:\nxlsx filename not OK"
        self._Get_Work_Sheet_Rows()
        if self._tTot_Rows == -1:
            return False, "FATAL ERROR 13:\non loading workbook"
        elif self._tTot_Rows == 0:
            return False, "none rows found in xlsx"

        self._Set_Xlsx_Conto_Year_Month()
        if self._tXlsx_Year is None or self._tXlsx_Conto is None or self._tXlsx_Month is None:
            return False, "FATAL ERROR 13\non extracting Year, Conto , Month from xlsx file"

        for idx, row in enumerate(self._df.itertuples(index=False)):
            xlsx_row__as_is = self._get_xlsx_as_is(idx, row)
            pass
            Checked_Row = self._Check_Values(xlsx_row__as_is)
            #
            if Checked_Row:
                self.nRow = idx
                Des1_Comp = Compact_Descr_String(Checked_Row[IX_ROW_DESCR1])
                Des2_Comp = Compact_Descr_String(Checked_Row[IX_ROW_DESCR2])
                Full_Desc  = FullDescr_Setup(Des1_Comp, Des2_Comp)
                self._Set_Year_Contab_Valuta(Checked_Row[IX_ROW_CONTAB])
                self._Set_Year_Contab_Valuta(Checked_Row[IX_ROW_VALUTA])
                Row_Desc_Comp = [self._nRow, self._Contab, self._Valuta, Des1_Comp, self._Accr, self._Addeb, Des2_Comp]
                Row_Compact   = [self._nRow, self._Contab, self._Valuta, self._Accr, self._Addeb, Full_Desc]
                self._tXLSX_Rows_From_Sheet.append(xlsx_row__as_is)    #_tXlsx_Rows_Sheet.append(Checked_Row)
                self._tXLSX_Rows_Desc_Compact.append(Row_Desc_Comp)
                self._tXlsx_Rows_Compact.append(Row_Compact)
                pass

        if self._tXlsx_Conto == FLASH or self._tXlsx_Conto == AMBRA or self._tXlsx_Conto == POSTA:
            self._Adjust_Rows_MostToLess()    # Invert order from Most Recent to Less

        status, data = self._create_With_Out_codes_lists()
        if not status:
            return False, data
        self._Save_Xlsx_Data()
        return True, ''



        if self._tXlsx_Conto == FLASH or self._tXlsx_Conto == AMBRA or self._tXlsx_Conto == POSTA:
            self._Adjust_Rows_MostToLess()    # Invert order from Most Recent to Less

        status, data = self._create_With_Out_codes_lists()
        if not status:
            return False, data
        self._Save_Xlsx_Data()
        return True, ''




        # for nRow in range(1, self._tTot_Rows+1):    # the first row is "1"
        #     XlsxRow_AsItIs = self._Get_xlsx_Row_AsIs(nRow)
        #     Checked_Row = self._Check_Valuesss(XlsxRow_AsItIs)
        #
        #     if Checked_Row:
        #         Des1_Comp = Compact_Descr_String(Checked_Row[IX_ROW_DESCR1])
        #         Des2_Comp = Compact_Descr_String(Checked_Row[IX_ROW_DESCR2])
        #         Full_Desc  = FullDescr_Setup(Des1_Comp, Des2_Comp)
        #         self._Set_Year_Contab_Valuta(Checked_Row[IX_ROW_CONTAB])
        #         self._Set_Year_Contab_Valuta(Checked_Row[IX_ROW_VALUTA])
        #         Row_Desc_Comp = [self._nRow, self._Contab, self._Valuta, Des1_Comp, self._Accr, self._Addeb, Des2_Comp]
        #         Row_Compact   = [self._nRow, self._Contab, self._Valuta, self._Accr, self._Addeb, Full_Desc]
        #         self._tXLSX_Rows_From_Sheet.append(XlsxRow_AsItIs)    #_tXlsx_Rows_Sheet.append(Checked_Row)
        #         self._tXLSX_Rows_Desc_Compact.append(Row_Desc_Comp)
        #         self._tXlsx_Rows_Compact.append(Row_Compact)
        #
        # if self._tXlsx_Conto == FLASH or self._tXlsx_Conto == AMBRA or self._tXlsx_Conto == POSTA:
        #     self._Adjust_Rows_MostToLess()    # Invert order from Most Recent to Less
        #
        # status, data = self._create_With_Out_codes_lists()
        # if not status:
        #     return False, data
        # self._Save_Xlsx_Data()
        # return True, ''

    # --------------------------------------------------------------------------------------------- #
    # _With_Code_Tree_List   : nRow   Contab  Valuta  TR_Desc   Accred  Addeb   TRcode  RowFullDes 
    def _create_With_Out_codes_lists(self) -> tuple[bool, str]:
        self._tWihtout_Code_Tree_List = []
        self._tWith_Code_Tree_List    = []
        self._tTotWith_Code           = 0
        self._tTotWithout_Code        = 0

        for Row in self._tXlsx_Rows_Compact:
            Full_Desc = Row[IX_ROW_COMP_FULLDES]
            TRcodeList  = self._Find_StrToFind_InFullDesc(Full_Desc)
            nCode = len (TRcodeList)
            if nCode == 1:                          # Unic code found for Row
                self.Insert_On_WithCode_List(Row, TRcodeList[0])

            elif nCode > 1:                         # Multiple codes found for a xlsx row
                print(TRcodeList, Row[IX_ROW_COMP_FULLDES])
                message  = f"la descrizione completa per la riga n.  {str(Row[IX_ROW_COMP_NROW])}\n\n"
                message += f"Contab: {Row[IX_ROW_COMP_CONTAB]}\nValuta: {Row[IX_ROW_COMP_VAL]}\n"
                message += f"Accred: {Row[IX_ROW_COMP_ACCR]}\nAddeb: {Row[IX_ROW_COMP_ADDEB]}\n"
                message += f"{Row[IX_ROW_COMP_FULLDES]}\n\n"
                message += f"combacia con piu stringhe per la ricerca:\n\n"
                for code in TRcodeList:
                    strFound =  f"codice: {str(code)}:  descr: {self.Get_TrDesc_FromCode(code)}\n{self.Get_strToFind_FromCode(code)}\n\n"
                    message += strFound        # dlg_select = View_Messa
                return False, message

            else:  # Code NOT found
                myRow = [Row[IX_ROW_COMP_NROW], self._tXlsx_Conto, Row[IX_ROW_COMP_CONTAB], Row[IX_ROW_COMP_VAL],
                         Row[IX_ROW_COMP_ACCR], Row[IX_ROW_COMP_ADDEB], Row[IX_ROW_COMP_FULLDES] ]

                self._tWihtout_Code_Tree_List.append(myRow)
                self._tTotWithout_Code += 1
                pass
        return True, ''

    # -----------------------------Code(TRcode)---------------------------------------------------------------
    def Insert_On_WithCode_List(self, Row, TRcode):
        TRdesc = self.Get_TrDesc_FromCode(TRcode)
        RecForIns   = [Row[IX_ROW_COMP_NROW], self._tXlsx_Conto, Row[IX_ROW_COMP_CONTAB], Row[IX_ROW_COMP_VAL],
                       Row[IX_ROW_COMP_ACCR], Row[IX_ROW_COMP_ADDEB],
                       TRdesc, TRcode,
                       Row[IX_ROW_COMP_FULLDES] ]
        self._tWith_Code_Tree_List.append(RecForIns)
        self._tTotWith_Code += 1
        pass

    # ---------------------------------------------------------------------------------------------
    def _Set_Year_Contab_Valuta(self, Date):
        self.Dummy = 0
        iYear = int(Date[0:4])
        if len(self._tiYear_List) < 2 and not iYear in self._iYear_List:
            self._tiYear_List.append(iYear)

    # ---------------------------------------------------------------------------------------------
    # NB: the full year list should contains all months + full january of next year
    #       January
    # 02/01/23	31/12/22	only contabile
    # 02/01/23	02/01/23	both
    # ..............................
    #       December
    # 02/01/24	30/12/23	only valuta
    # 02/01/24	02/01/24	NOT
    # ---------------------------------------------------------------------------------------------
    def _Date_Check(self,XlsxRow_AsItIs):
        Date_Contab = XlsxRow_AsItIs[IX_ROW_CONTAB]
        Date_Valuta = XlsxRow_AsItIs[IX_ROW_VALUTA]
        if type(Date_Contab) is not datetime or type(Date_Valuta) is not datetime:
            return  False
        str_date_contab = Date_Contab.strftime("%Y-%m-%d")
        str_date_valuta = Date_Valuta.strftime("%Y-%m-%d")
        iYear_Contab    = int(str_date_contab[0:4])
        iYear_Valuta    = int(str_date_valuta[0:4])
        if iYear_Contab != self._tXlsx_Year and iYear_Valuta != self._tXlsx_Year:
            return False
        elif iYear_Contab == self._tXlsx_Year and iYear_Valuta == self._tXlsx_Year:
            return True
        elif iYear_Contab == self._tXlsx_Year or iYear_Valuta == self._tXlsx_Year:
            return True
        return False

    # ---------------------------------------------------------------------------------------------
    def _Check_Values(self, XlsxRow_AsItIs):
        # nRow = XlsxRow_AsItIs[IX_ROW_NROW]

        if not self._Date_Check(XlsxRow_AsItIs):
            return []
        else:
            Xlsx_Row_List_Checked = []
            for Item_ToCheck in LIST_FOR_XLSX_ROW_CONTROL:
                Value = XlsxRow_AsItIs[Item_ToCheck[0]]
                Type = Item_ToCheck[1]
                ItemChecked = self._Check_Val(Value, Type)
                if ItemChecked is None:
                    return []
                else:
                    Xlsx_Row_List_Checked.append(ItemChecked)
            return Xlsx_Row_List_Checked  # as in Xlsx Rows

    # ---------------------------------------------------------------------------------------------
    def _Check_Val(self, Item, Type):
        # LIST_FOR_XLSX_ROW_CONTROL:
        #       [IX_ROW_NROW, INTEGER],
        #       [IX_ROW_CONTAB, DATE],  [IX_ROW_VALUTA, DATE],
        #       [IX_ROW_DESCR1, STRING],
        #       [IX_ROW_ACCRED, NUMERIC], [IX_ROW_ADDEB, NUMERIC],
        #       [IX_ROW_DESCR2, STRING]
        ItemType  = type(Item)
        if Type == STRING:            #   ---  String   -----  (Descriptions)
            if ItemType is str:
                if len(Item) < 3:     # PAM
                    return 'Not assigned'
                return Item
            elif Item is None:
                return 'Not assigned'
            else:
                return None
        elif Type == INTEGER:         #   ---  Integer  -----   (Row Id number)
            if ItemType is int:
                return Item
            return None
        elif Type == NUMERIC:         #   ---  Numeric  -----  (Accred  _Addeb)
            if ItemType is float:
                return Item
            elif ItemType is int:
                return float(Item)
            else:
                if Item is None:
                    return 0.00
        elif Type == DATE:            #   ---  Date    -----
            Ckd_Date = self._Verify_Date(Item)
            if Ckd_Date:
                return Ckd_Date
            else:
                return None
        return None

    # ---------------------------------------------------------------------------------------------
    def _get_xlsx_as_is(self, idf, row):
        # IX_ROW_NROW   = 0
        # IX_ROW_CONTAB = 1
        # IX_ROW_VALUTA = 2
        # IX_ROW_DESCR1 = 3
        # IX_ROW_ACCRED = 4
        # IX_ROW_ADDEB  = 5
        # IX_ROW_DESCR2 = 6

        self.Dummy = 0
        rowList     = list(row)
        data_contab = rowList[0]
        datavaluta  = rowList[1]
        descr1      = rowList[2]
        accred      = rowList[3]
        addeb       = rowList[4]
        descr2      = rowList[5]
        pass
        return [idf, data_contab, datavaluta, descr1, accred, addeb, descr2]

    # ---------------------------------------------------------------------------------------------
    def _Get_xlsx_Row_AsIs(self, nRow):
        self._nRow = nRow
        if self._tXlsx_Conto == FIDEU:                                      ###   FIDEURAM   ###
            Contab = self._Work_Sheet['A' + str(self._nRow)].value
            Valuta = self._Work_Sheet['B' + str(self._nRow)].value
            self._Date_Setup(Contab, Valuta)
            self._Des1   = self._Work_Sheet['C' + str(self._nRow)].value
            XlsxAccr     = self._Work_Sheet['D' + str(self._nRow)].value
            XlsxAddeb    = self._Work_Sheet['E' + str(self._nRow)].value
            self._Des2   = self._Work_Sheet['F' + str(self._nRow)].value
            self._Accr   = Convert_To_Float(XlsxAccr)
            self._Addeb  = Convert_To_Float(XlsxAddeb)

        elif self._tXlsx_Conto == FLASH or self._tXlsx_Conto == AMBRA:      ###   AMBRA & FLASH CARD ###
            Contab = self._Work_Sheet['A' + str(self._nRow)].value
            Valuta = self._Work_Sheet['B' + str(self._nRow)].value
            self._Date_Setup(Contab, Valuta)
            self._Des1   = self._Work_Sheet['C' + str(self._nRow)].value
            XlsxAccr     = self._Work_Sheet['E' + str(self._nRow)].value
            XlsxAddeb    = self._Work_Sheet['G' + str(self._nRow)].value
            self._Des2   = ''
            # -------   Credits and Debits  type are :  float
            self._Accr  = Convert_To_Float(XlsxAccr)
            self._Addeb = -Convert_To_Float(XlsxAddeb)
            typeContab  = type(self._Contab)
            typeValuta  = type(self._Valuta)

            if typeContab is datetime and typeValuta is datetime:
                pass
            elif typeContab is datetime:
                self._Valuta = self._Contab
            elif typeValuta is datetime:
                self._Contab = self._Valuta

        # -----------------------------------------------------------------------------------------
        #     A            B           C         D        E
        # DataContab.	DataVal.	Addebiti  Accred. Descrizione
        # -----------------------------------------------------------------------------------------
        elif self._tXlsx_Conto == POSTA:                                    ###  BANCO POSTA   ###
            Contab = self._Work_Sheet['A' + str(self._nRow)].value
            Valuta = self._Work_Sheet['B' + str(self._nRow)].value
            self._Date_Setup(Contab, Valuta)
            self._Des1   = ''  #self.Work_Sheet['C' + str(self._nRow)].value
            self._Accr   = self._Work_Sheet['D' + str(self._nRow)].value
            self._Addeb  = self._Work_Sheet['C' + str(self._nRow)].value
            self._Des2   = self._Work_Sheet['E' + str(self._nRow)].value
            if type(self._Addeb) is float or type(self._Addeb) is int:
                self._Addeb  = -self._Addeb
            typeContab = type(self._Contab)
            typeValuta = type(self._Valuta)
            if typeContab is datetime and typeValuta is datetime:
                self._Valuta = self._Contab
                self._Contab = self._Valuta
        return [self._nRow, self._Contab, self._Valuta, self._Des1, self._Accr, self._Addeb ,self._Des2]

    # --------_Year_Setup--------------------------------------------------------------------------------------
    def _Date_Setup(self, Contab, Valuta):
        self._Contab = None
        self._Contab = None
        Date = self._Verify_Date(Contab)
        if Date:
            self._Contab = Date
        Date = self._Verify_Date(Valuta)
        if Date:
            self._Valuta = Date

    # ---------------------------------------------------------------------------------------------
    # reorder rows for dates ascending   AMBRA  FLASH  POSTA
    def _Adjust_Rows_MostToLess(self):
        Sheet_Copy     = self._Xlsx_Rows_From_Sheet.copy()
        Desc_Comp_Copy = self._Xlsx_Rows_Desc_Compact.copy()
        Row_Comp_Copy  = self._Xlsx_Rows_Compact.copy()
        self.XLSX_Rows_From_Sheet = []
        self._Xlsx_Rows_Desc_Compact = []
        self._Xlsx_Rows_Compact = []
        Index = self._Tot_OK -1
        for j in range(0, self._Tot_OK):
            self.XLSX_Rows_From_Sheet.append(Sheet_Copy[Index])
            self._Xlsx_Rows_Desc_Compact.append(Desc_Comp_Copy[Index])
            self._Xlsx_Rows_Compact.append(Row_Comp_Copy[Index])

    # --------------------------------------------------------------------------------- #
    #  Workbook is the container of all Worksheets                                      #
    #  while the Worksheet is the container of Data of one Sheet                        #
    # --------------------------------------------------------------------------------- #
    def _Get_Work_Sheet_Rows(self):
        filename = self.Get_sel_dictionary_value(XLSX_FILENAME)
        try:
            # header=None disattiva la ricerca dei titoli delle colonne.
            # Le colonne si chiameranno semplicemente 0, 1, 2, 3...
            self._df = pd.read_excel(filename, sheet_name=0, header=None)

            xl_file = pd.ExcelFile(filename)
            self.SheetName = xl_file.sheet_names[0]

            # TRUCCO FONDAMENTALE:
            # Sostituiamo NaN con None usando replace e object
            self._df = self._df.astype(object).replace({np.nan: None})
            pass
            # Convertiamo i campi vuoti (NaN) nel classico None di Python
            self._df = self._df.astype(object).where(pd.notnull(self._df), None)
            pass
            self._tTot_Rows = len(self._df)
            pass

        except Exception as e:
            print(f"Errore lettura Pandas: {e}")
            self._tTot_Rows = -1
            self._df = None
            self.SheetName = ""
            return -1
        finally:
            pass
        return self._tTot_Rows
    # def _Get_Work_Sheet_Rows(self):
    #     filename = self.Get_sel_dictionary_value(XLSX_FILENAME)
    #     Work_Book = None
    #     try:
    #         Work_Book = load_workbook(filename)
    #     except ValueError as e:
    #         self._tTot_Rows = -1
    #         return
    #     finally:
    #         self.SheetName   = Work_Book.sheetnames[0]   # always the first sheet
    #         self._Work_Sheet = Work_Book[self.SheetName]
    #         self._tTot_Rows  = self._Work_Sheet.max_row
    #         pass

    # -----------------------------------------------------------------------------------
    def _Verify_Date(self, DateToCheck):
        self.Dummy = 0
        myDate = DateToCheck
        if DateToCheck is None:
            return ''
        Type = type(DateToCheck)
        if Type is datetime:
            strDate = str(DateToCheck)
            myDate  = strDate[:10]
        elif Type is not str:
            return ''
        # DateTemplate = 'DD?MM?YYYY'
        DateTemplate = 'YYYY?MM?DD'
        if len(myDate) != 10:
            return ''
        for i in range(0, 10):
            if DateTemplate[i] == '?':
                pass
            else:
                if not myDate[i].isdecimal():
                    return ''
        strYear  = myDate[0:4]
        strMonth = myDate[5:7]
        strDay   = myDate[8:10]
        myDate = strYear + '-' + strMonth + '-' +strDay
        return myDate

# =======================================================================================