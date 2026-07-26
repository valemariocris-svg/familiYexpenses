# =============================================================================================== #
#   Create:                                                                                       #
# Xlsx_Rows_From_Sheet_normalized   nRow    Contab  Valuta    Des1    Accr   Addeb     Des2       #
# Xlsx_Rows_Desc_CompactnRow        Contab  Valuta  Des1Comp  Accr   Addeb    Des2Comp            #
# tXlsx_Rows_Compact                nRow  _Contab   Valuta   Accr     Addeb  Full_Desc            #
#                                                                                                 #
# self._tWith_Code_Tree_List        nRow Contabile _Valuta Accred _Addeb TRdesc TRcode            #
# self._tWihtout_Code_Tree_List     nRow Contabile _Valuta Accred _Addeb FullDesc                 #
# ----------------------------------------------------------------------------------------------- #
import pandas as pd
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

        # ------------------------
        self._Xlsx_Rows_From_Sheet_normalized = []
        # self._Xlsx_Rows_Desc_Compact   = []
        self._Xlsx_Rows_Compact        = []
        # ------------------------
        self._Tot_Rows        = 0
        self._Tot_NOK         = 0
        self._Tot_OK          = 0
        self._TotWith_Code    = 0
        self._TotWihtout_Code = 0
        self._iYear_List      = []

        # -------   _tAtt : temporary attributes  that will be copied on _Att  if all OK  -------------
        self._tXLSX_Rows_From_Sheet_normalized    = []
        # self._tXlsx_Rows_Desc_Compact  = []
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
        return len(self._Xlsx_Rows_From_Sheet_normalized)

    def Get_Xlsx_Rows_From_Sheet_normalized(self):
        return self._Xlsx_Rows_From_Sheet_normalized

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
        self._tXlsx_Rows_From_Sheet_normalized = []
        # self._tXlsx_Rows_Desc_Compact = []
        self._tXlsx_Rows_Compact      = []

        self._tWith_Code_Tree_List    = []
        self._tWihtout_Code_Tree_List = []

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
        self._Xlsx_Rows_From_Sheet_normalized   = self._tXLSX_Rows_From_Sheet_normalized
        # self._Xlsx_Rows_Desc_Compact = self._tXlsx_Rows_Desc_Compact
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

    # --------------------------------------------------------------------------------- #
    #  Workbook is the container of all Worksheets                                      #
    #  while the Worksheet is the container of Data of one Sheet                        #
    # --------------------------------------------------------------------------------- #
    def _Get_Work_Sheet_Rows(self):
        filename = self.Get_sel_dictionary_value(XLSX_FILENAME)
        try:
            self._df = pd.read_excel(
                filename,
                sheet_name=0,
                header=None,    # Nessun titolo
                # usecols="A:G",  # Forza a leggere sempre le colonne A, B, C, D, E, F, G
                keep_default_na=False  # Le celle vuote diventano "" anziché NaN
            )
            self._tTot_Rows = len(self._df)

        except Exception as e:
            print(f"Errore lettura Pandas: {e}")
            self._tTot_Rows = -1
            self._df = None
            return -1
        return self._tTot_Rows

    # ----------------------------------------------------------------------------------------------- #
    def  Load_Xlsx_Rows(self) -> tuple[bool, str | list]:
        self._Init_Xlsx_Data()
        Filename = self.Get_sel_dictionary_value(XLSX_FILENAME)
        if not Gl_Cek_Xlsx_Name(Filename):
            return False, "FATAL ERROR 12:\nxlsx filename not OK"

        self._Get_Work_Sheet_Rows()  # ------------------>>>>>

        if self._tTot_Rows == -1:
            return False, "FATAL ERROR 13:\non loading workbook"
        elif self._tTot_Rows == 0:
            return False, "none rows found in xlsx"

        self._Set_Xlsx_Conto_Year_Month()
        if self._tXlsx_Year is None or self._tXlsx_Conto is None or self._tXlsx_Month is None:
            return False, "FATAL ERROR 13\non extracting Year, Conto , Month from xlsx file"

        for idx, row in enumerate(self._df.itertuples(index=False)):
            rowList = list(row)
            print(f"{idx+1}:  {type(rowList[0])}  {rowList[1]} {rowList[2]} {rowList[3]} {rowList[4]}  {rowList[5]}")

            Checked_Row = self._Check_Values(rowList)

            if Checked_Row:
                self._nRow = idx
                Des1_Comp = Compact_Descr_String(Checked_Row[IX_ROW_DESCR1])
                Des2_Comp = Compact_Descr_String(Checked_Row[IX_ROW_DESCR2])
                Full_Desc  = FullDescr_Setup(Des1_Comp, Des2_Comp)

                self._Set_Year_Contab_Valuta(Checked_Row[IX_ROW_CONTAB])
                self._Set_Year_Contab_Valuta(Checked_Row[IX_ROW_VALUTA])

                # Row_Desc_Comp = [self._nRow, self._Contab, self._Valuta, Des1_Comp, self._Accr, self._Addeb, Des2_Comp]
                Row_Compact   = [self._nRow, self._Contab, self._Valuta, self._Accr, self._Addeb, Full_Desc]
                self._tXLSX_Rows_From_Sheet_normalized.append(Checked_Row)
                # self._tXlsx_Rows_Desc_Compact.append(Row_Desc_Comp)
                self._tXlsx_Rows_Compact.append(Row_Compact)
                pass

        if self._tXlsx_Conto == FLASH or self._tXlsx_Conto == AMBRA or self._tXlsx_Conto == POSTA:
            # self._tXlsx_Rows_Desc_Compact.sort(reverse=True)    # Invert order from Most Recent to Less
            self._tXlsx_Rows_Compact.sort(reverse=True)

        status, data = self._create_With_Out_codes_lists()
        if not status:
            return False, data
        self._Save_Xlsx_Data()
        return True, ''
    # ---------------------------------------------------------------------------------------------
    # def _get_xlsx_row_as_is(self, row):
        # CONTO     A       B       C       D       E       F       G
        #           0       1       2       3       4       5       6
        # FIDEU     Contab  Valuta  Des1    Accred  Added   Des2
        # FLH-AMBR  Contab  Valuta  Des1            Addeb-          Accred
        # POSTA     Contab  Valuta  Addeb-  Accred  Des1
        # FORM nRow,Contab, Valuta, Des1,   Accred, Addeb,  Des2
        #        0     1       2      3        4      5       6

        # rowList   = list(row)
        # Contab    = rowList[0]
        # Valuta    = rowList[1]
        # Des1   = None
        # Accred = None
        # Addeb  = None
        # Des2   = None
        #
        # if self._tXlsx_Conto == FIDEU:
        #     Des1   = rowList[2]
        #     Accred = rowList[3]
        #     Addeb  = rowList[4]
        #     Des2   = rowList[5]
        #
        # elif self._tXlsx_Conto == FLASH or self._tXlsx_Conto == AMBRA:
        #     Des1   = rowList[1]
        #     Accred = rowList[5]
        #     Addeb  = rowList[3]
        #     Des2   = ''
        #
        # elif self._tXlsx_Conto == POSTA:
        #     Des1 = rowList[4]
        #     Accred = rowList[2]
        #     Addeb = rowList[1]
        #     Des2 = ''
        #
        # return [Contab, Valuta, Des1, Accred, Addeb , Des2]

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
    def _Check_Values(self, XlsxRow_AsItIs):
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
    def _Date_Check(self, XlsxRow_AsItIs):
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
    def _Check_Val(self, Item, Type):
        self.Dummy = 0
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
        elif Type == DATE:            #   ---  Date verified on Load_xlsx_rows
            return Item
        return None


    # --------_Year_Setup--------------------------------------------------------------------------------------
    # def _Date_Setup(self, Contab, Valuta):
    #     self._Contab = None
    #     self._Contab = None
    #     Date = self._Verify_Date(Contab)
    #     if Date:
    #         self._Contab = Date
    #     Date = self._Verify_Date(Valuta)
    #     if Date:
    #         self._Valuta = Date

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