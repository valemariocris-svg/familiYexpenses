# ============================================================================= #
#               -----   Transact_DB.py   -----                                  #
#              last child class  of data chain                                  #
# ============================================================================= #

from Common.Common_Functions import *
from Data_Classes.Xlsx_Manager import Xlsx_Manager

# -----------------------------------------------------------------------------------------------------
class Transact_Db(Xlsx_Manager):
    def __init__(self):
        super().__init__()
        self.Dummy   = 0
        self._Transact_Records_as_is       = []    # TRANSACT table as in Database
        self._Transact_Table_Order         = []    # TRANSACT table ordered by Contabile ASC
        self._Transact_Records_NormalCode  = []    # TRANSACT table normal code
        self._Transact_Records_GenericCode = []    # TRANSACT table GENERICCODE

        self.Ident  = None # [IX_TRANSACT_IDENT]    # Transact_Db uses without underscore (_)
        self.Conto  = None # [IX_TRANSACT_CONTO]
        self.Contab = None # [IX_TRANSACT_CONTAB]
        self.Valuta = None # [IX_TRANSACT_VALUTA]
        self.Descr  = None # [IX_TRANSACT_TR_DESC]
        self.Accred = None # [IX_TRANSACT_ACCRED]
        self.Addeb  = None # [IX_TRANSACT_ADDEB]
        self.flAccr = None
        self.flAddeb= None
        self.TRcode = None # [IX_TRANSACT_TR_CODE]
        self.FullDes= None # [IX_TRANSACT_FULL_DESC]

        self.Row_To_Del         = []
        self._Count_Contab_Val  = 0
        self._Rows_Tot_xMonth   = None
        self._Found_Except      = False
        self._Transactions_Exceptions = None

        self._Rows_WithCod_List_toInsert = []
        self.TotTransact_ToBeInserted    = 0
        self._Generic_Code_List = []

        self._Full_Transact_List = []
        self._Full_Contab_List   = []
        self._Full_Valuta_List   = []
        self._Month_Contab_List  = []
        self._Month_Valuta_List  = []

        self._Full_Generic_List         = []
        self._Full_Generic_Contab_List  = []
        self._Full_Generic_Valuta_List  = []
        self._Generic_Month_Contab_List = []
        self._Generic_Month_Valuta_List = []

        self._records_to_insert_list = []  # the list of records to be inserted in transactions database
        self._TotTransact_ToBeInserted = 0
        self._transactions_map = {}


    def Get_Xlsx_Transact_Ident(self):
        return [self._Xlsx_Conto, self._Xlsx_Year, self._Transact_Year]

    def Get_Full_Xlsx_Transact_Ident(self):
        return [self._Xlsx_Conto, self._Xlsx_Year, self._Xlsx_Month, self._Transact_Year]

    # -------------------------------------------------------------------------------------------------
    def Get_Generic_Codes_List(self):
        return[len(self._Generic_Code_List), self._Generic_Code_List]

    # -------------------------------------------------------------------------------------------------
    #                      0     1      2     3      4        5      6      7     8
    # List_Transact_DB :  nRow Conto Contab Valuta TR_Desc Accred Addeb  TRcode FullDesc
    # -------------------------------------------------------------------------------------------------
    def Load_Transactions_Table(self) -> tuple[bool, str | list]:
        _filename = self.Get_sel_dictionary_value(TRANSACT_FILENAME)
        if not Gl_Cek_Transactions_Name(_filename):
            return False, 'Transactions filename NOT K\nplease selecte a correct filename'
        status, data = Gl_Cek_Transactions_Name(_filename)
        if not status:
            return False, data

        self._tTransact_Year               = Get_Transactions_Year(_filename)
        self._Transact_Records_as_is       = []    # TRANSACT table as in Database
        self._Transact_Records_NormalCode  = []    # TRANSACT table normal code
        self._Transact_Records_GenericCode = []    # TRANSACT table GENERICCODE
        #
        sql = "SELECT * FROM TRANSACT"
        status, data = self._query_execute(TRANSACT_FILE, sql, (), CLOSE_DB)
        if not status:
            strErr = f"{data}\nOn loading transactions from database"
            return False, strErr
        if not data:
            pass                # all recods are empty
            return True, []
        else:
            self._Transact_Records_as_is = data
            self._Transact_Year          = self._tTransact_Year     # new Year

            sql = "SELECT * FROM TRANSACT ORDER BY Contab ASC"
            status, data = self._query_execute(TRANSACT_FILENAME, sql, (), CLOSE_DB)
            if not status:
                strErr = f"{data}\nOn loading orderedtransactions from database"
                return False, strErr
            self._Transact_Table_Order = data                    # TRANSACT table ordered by Valuta ASC

            for Rec in self._Transact_Table_Order:
                try:
                    if Rec[IX_TRANSACT_TR_CODE] < GENERIC_CODE_INIT:
                        self._Transact_Records_NormalCode.append(Rec)
                    else:
                        self._Transact_Records_GenericCode.append(Rec)
                except Exception as e:
                    return False, f"FATAL ERROR 15:\n{e}\non createing normal/generic codes list"
                finally:
                    pass
            return True, ''

    # -------------------------------------------------------------------------------------------------
    def Get_rec_from_list_toInsert(self, Id):
        pass
        # for rec in self._Transact_Records_Order_ASC:
        #     if rec[IX_TRANSACT_IDENT] == Id:
        #         return rec
        # return []

    # -------------------------------------------------------------------------------------------------
    def Create_records_to_insert_list(self):
        self._records_to_insert_list = []   # the list of records to be inserted in transactions database
        self._TotTransact_ToBeInserted = 0

        # 1. Inizializzi la mappa come dizionario vuoto
        self._transactions_map = {}

        print(f"\n=================== dictionary  ===========================")
        # 2. Cicli sui record caricati dal DB
        for record in []:  #self._Transact_Recods:
            # Assegni dei nomi parlanti alle colonne per non fare confusione con gli indici
            conto      = record[IX_TRANSACT_CONTO]      # nome della banca interessata
            dateContab = record[IX_TRANSACT_CONTAB]     # data contabile
            dateValuta = record[IX_TRANSACT_VALUTA]     # data valuta
            credit     = record[IX_TRANSACT_ACCRED]     # accredito
            debit      = record[IX_TRANSACT_ADDEB]      # debito
            print(
                f"{type(conto)},{conto}  {type(dateContab)},{dateContab}  {type(dateValuta)},{dateValuta}  {type(credit)},{credit}  {type(debit)},{debit}")

            # 3. Crei la chiave unica (una tupla)
            key = (conto, dateContab, dateValuta, credit, debit)

            # 4. Inserisci nella mappa il codice del movimento
            #    uguale per es. a tutti i movimenti tipo "Supermercato PAM"
            self._transactions_map[key] = record[IX_TRANSACT_TR_CODE]  # codice

        pass
        print(f"\n=================== records  ==============================")
        # creazione della lista dei record caricati da .XLSX ma non presenti nel database
        for row in self._tWith_Code_Tree_List:
            # print(row)
            # Esempio di verifica sui nuovi movimenti estratti da Excel
            conto      = self._tXlsx_Conto      # settato nel tirar su .xlsx
            dateContab = row[IX_WITH_CODE_CONTAB]
            dateValuta = row[IX_WITH_CODE_VALUTA]
            credit     = row[IX_WITH_CODE_ACCRED]
            debit      = row[IX_WITH_CODE_ADDEB]
            # se il record non e' presente nel database lo metto in lista
            # il motivo e' che cosi posso caricare i movimenti mese per mese
            # con file xlsx che patono sempre da gennaio fino al mese corrente
            print(
            f"{type(conto)},{conto}  {type(dateContab)},{dateContab}  {type(dateValuta)},{dateValuta}  {type(credit)},{credit}  {type(debit)},{debit}")

            pass
            if not (conto, dateContab, dateValuta, credit, debit) in self._transactions_map:
                # IX_TRANSACT_IDENT = 0, IX_TRANSACT_CONTO = 1, IX_TRANSACT_CONTAB = 2, IX_TRANSACT_VALUTA = 3
                # IX_TRANSACT_ACCRED= 4, IX_TRANSACT_ADDEB = 5, IX_TRANSACT_TR_DESC= 6, IX_TRANSACT_TR_CODE= 7
                # IX_TRANSACT_FULL_DESC= 8

                record = [row[IX_WITH_CODE_NROW], conto, dateContab, dateValuta, credit, debit, row[IX_XLSX_WITH_TRDESC],
                          row[IX_WITH_CODE_TR_CODE], row[IX_WITH_CODE_FULL_DESCR] ]
                # preferisco creare una lista per poterla esaminare al momento di inserirla nel databse
                self._records_to_insert_list.append(record)
                self._TotTransact_ToBeInserted += 1
                pass
            pass
        pass


    # -------------------------------------------------------------------------------------------------
    # def Get_Transact_AllCode_List(self):
    #     pass
    #     # return self._Transact_Records_as_is

    # -------------------------------------------------------------------------------------------------
    def Get_Transact_Contabile_ASC_List(self):
        return self._Transact_Table_Order

    # -------------------------------------------------------------------------------------------------
    def Get_Transact_NormalCode_List(self):
        return self._Transact_Records_NormalCode

    # -------------------------------------------------------------------------------------------------
    def Get_Transact_GenericCode_List(self):
        return self._Transact_Records_GenericCode


    # -------------------------------------------------------------------------------------------------
    #                      0     1      2     3      4        5      6      7     8
    # List_Transact_DB :  nRow Conto Contab Valuta TR_Desc Accred Addeb  TRcode FullDesc
    # -------------------------------------------------------------------------------------------------
    def _Load_Transactions_Table(self, TransacFilename):         # return  OK  or  'Diagnostic '
        pass
        # Filename = TransacFilename

        #     Filename = self.Get_sel_dictionary_value(TRANSACT_FILENAME)
        #
        # Result = self._Connect_Transact_Db(Filename)
        # if Result != OK:
        #     return Result
        # self._tTransact_Year = Get_Transactions_Year(Filename)
        #
        # self._Transact_Records_as_is         = []        # TRANSACT table as in Database
        # self._Transact_Table_Order     = []        # TRANSACT table ordered by Contabile ASC
        # self._Transact_Records_NormalCode  = []    # TRANSACT table normal code
        # self._Transact_Records_GenericCode = []    # TRANSACT table GENERICCODE
        #
        # Sql_Select = """SELECT * FROM TRANSACT ORDER BY Contab ASC"""
        # Result     = self._Make_Select_All(Sql_Select)
        # if Result[0] != OK:
        #     self._Close_Transact_DataBase()
        #     return Result[1]
        # self._tTransact_Table = Result[1]
        # self._Transact_Table_Order  = self._tTransact_Table    # TRANSACT table ordered by Valuta ASC
        # self._Transact_Year         = self._tTransact_Year     # new Year
        #
        # for Rec in self._Transact_Records_as_is:
        #     try:
        #         if Rec[IX_TRANSACT_TR_CODE] < GENERIC_CODE_INIT:
        #             self._Transact_Records_NormalCode.append(Rec)
        #         else:
        #             self._Transact_Records_GenericCode.append(Rec)
        #     except Exception as e:
        #         print(Rec)
        #         strErr = Db_Error(e)
        #         PRINT('Error on separating Normal and Generic Codes from TRANSACT Table\n' + strErr)
        #
        #
        # # the Selections are upadated because TransacFilename can be origened from Search on TRANSACTIONS
        # self.Update_key_dictionary(TRANSACT_FILENAME, Filename)
        # Sql_Select = """SELECT * FROM TRANSACT"""
        # Result = self._Make_Select_All(Sql_Select)
        # if Result[0] != OK:
        #     self._Close_Transact_DataBase()
        #     return Result[1]
        # self._Transact_Records_as_is = Result[1]      # TRANSACT table as in Database
        # self._Close_Transact_DataBase()                                           # CHANGE CLOSE
        # return OK

    # -------------------------------------------------------------------------------------------------
    def Clear_Transact_Year(self):
        self._Transact_Year = None

    # -------------------------------------------------------------------------------------------------
    def _Set_Transact_Year(self):
        # asTransact_2024.db

        FullFilename = self.Get_sel_dictionary_value(TRANSACT_FILENAME)
        # FullFilename = self.Get_Selections_Member(IX_TRANSACT_FILE)

        if FullFilename != UNKNOWN:
            filename = Get_File_Name(FullFilename)
            self._tTransact_Year = int(filename[9:13])
        else:
            self._tTransact_Year = None

    # -------------------------------------------------------------------------------------------------
    def Get_Transact_Table(self):
        Transact_Descr_OK = []
        for Rec in self._Transact_Table_Order:
            RecList = list(Rec)
            TRcode  = RecList[IX_TRANSACT_TR_CODE]
            TRdesc  = self.Get_TrDesc_FromCode(TRcode)        # The Descr was inserted in Database at
            # Accred  = SetNoZero(RecList[IX_TRANSACT_ACCRED])  # inserting but it could be modified later
            # Addeb   = SetNoZero(RecList[IX_TRANSACT_ADDEB])
            RecList[IX_TRANSACT_TR_DESC] = TRdesc
            # TrFull  = self.RecList(IX_TRANSACT_FULL_DESC)
            # RecList[IX_TRANSACT_ACCRED]  = Accred
            # RecList[IX_TRANSACT_ADDEB]   = Addeb
            Transact_Descr_OK.append(RecList)
        return Transact_Descr_OK

    # -------------------------------------------------------------------------------------------------
    def Get_Transact_Table_x_Conto(self, Conto):
        pass
        # Transact_Conto = []
        # for Rec in self._Transact_Records_as_is:
        #     RecList = list(Rec)
        #     if RecList[IX_TRANSACT_CONTO] == Conto:
        #         Transact_Conto.append(RecList)
        # return Transact_Conto

    # -------------------------------------------------------------------------------------------------
    def Get_Len_Transact_Table(self):
        return len(self._Transact_Table_Order)

    # -------------------------------------------------------------------------------------------------
    # def Find_Xlsx_In_Db(self, Conto, Contab, Valuta, Accred, Addeb, FullDesc):
        # for Transact in self._Transact_Records_as_is:
        #     if (Conto    == Transact[IX_TRANSACT_CONTO] and
        #         Contab   == Transact[IX_TRANSACT_CONTAB] and
        #         Valuta   == Transact[IX_TRANSACT_VALUTA] and
        #         Accred   == Transact[IX_TRANSACT_ACCRED] and
        #         Addeb    == Transact[IX_TRANSACT_ADDEB] and
        #         FullDesc == Transact[IX_TRANSACT_FULL_DESC]):
        #         pass
        #         return list(Transact)
        # return None

    # -------------------------------------------------------------------------------------------------
    # def Create_Transact_Filename(self, Year):
    #     Xlsx_CommonDir = self.Get_Xls_CommonDir()
    #     Fullname       = Xlsx_CommonDir + '/' + TRANSACTIONS + '/' + TRANSACT_ + str(Year) + '.db'
    #     return Fullname

    # -------------------------------------------------------------------------------------------------
    def Create_Transact_Table(self) -> tuple[bool, str]:
        sql = """CREATE TABLE TRANSACT \
                 ( \
                     "Ident"   INTEGER NOT NULL UNIQUE, \
                     "nRow"    INTEGER, \
                     "Conto"   TEXT, \
                     "Contab"  TEXT, \
                     "Valuta"  TEXT, \
                     "Accred"  FLOAT, \
                     "Addeb"   FLOAT, \
                     "TRdesc"  TEXT, \
                     "TRcode"  INTEGER, \
                     "FullDes" TEXT, \
                     PRIMARY KEY ("Ident" AUTOINCREMENT)
                 )"""
        parameters = ()
        return self._query_execute(TRANSACT_FILE, sql, parameters, CLOSE_DB)


    def _Create_Transact_List_perMonth(self):
        # DateIndex = IX_TRANSACT_VALUTA
        DateIndex = IX_TRANSACT_CONTAB
        # self.Transact_xMonth_List = [[]] * 12
        # self.DateCount_PerMonth   = [0]  * 12
        self.Transact_xMonth_List = [ [], [], [], [], [], [], [], [], [], [], [], [] ]
        self.DateCount_PerMonth   = [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0  ]
        for Rec in self._Transact_Table_Order:
            iMonth = 0            # self.CheckForInsert(Rec)
            if iMonth >= 0:
                Counts = self.DateCount_PerMonth[iMonth]
                Counts += 1
                if Counts > 10:
                    Counts = 0
                self.DateCount_PerMonth[iMonth] = Counts
                # ['Date', 'Co', 'Description', 'Credits  ', 'Debits  ']
                FullDate = Rec[DateIndex]
                Date     = Set_Month_Day(FullDate, Counts)
                TRcode   = Rec[IX_TRANSACT_TR_CODE]
                TRdescr  = self.Get_TrDesc_FromCode(TRcode)
                Conto    = CONTO_RED[Rec[IX_TRANSACT_CONTO]]
                View_Rec = [Date, Conto, TRdescr, Rec[IX_TRANSACT_ACCRED],
                            Rec[IX_TRANSACT_ADDEB], Rec[IX_TRANSACT_IDENT]]
                self.Transact_xMonth_List[iMonth].append(View_Rec)
                pass

    # -------------------------------------------------------------------------------------------------
    def _Test_if_TRANSACT_TableExists(self):
        pass
        # Result = self._Connect_Transact_Db
        # if Result != OK:
        #     return True
        # try:
        #     self._Transact_Cursor = self._Transact_Connected.cursor()
        #     self._Transact_Cursor.execute("SELECT * FROM TRANSACT")
        #     self._Transact_Cursor.fetchall()
        # except sqlite3.Error:  # in case of error nothing change
        #     Result = False
        # # finally:
        # #     pass
        # self._Close_Transact_DataBase()
        # return Result

    # -------------------------------------------------------------------------------------------------
    def Clear_Transact_Table(self):
        pass

    # -------------------------------------------------------------------------------------------------
    #                   0      1       2      3       4       5       6       7       8
    # Record_List :  (Ident) Conto, Contab, Valuta, Accred, Addeb, TRdesc, TRcode, FullDes)
    # -------------------------------------------------------------------------------------------------
    def Insert_Transact_Record(self, Record_List):
        Conto  = Record_List[IX_TRANSACT_CONTO]
        Contab = Record_List[IX_TRANSACT_CONTAB]
        Valuta = Record_List[IX_TRANSACT_VALUTA]
        TRdesc = Record_List[IX_TRANSACT_TR_DESC]
        Accred = Convert_To_Float(Record_List[IX_TRANSACT_ACCRED])
        Addeb  = Convert_To_Float(Record_List[IX_TRANSACT_ADDEB])
        TRcode = Record_List[IX_TRANSACT_TR_CODE]
        FullDes = Record_List[IX_TRANSACT_FULL_DESC]

        sql = """INSERT INTO TRANSACT (Conto, Contab, Valuta, Accred, Addeb, TRdesc, TRcode, FullDes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        parameters = (Conto, Contab, Valuta, Accred, Addeb, TRdesc, TRcode, FullDes)
        status, data = self._query_execute(TRANSACT_FILENAME, sql, parameters, CLOSE_DB)
        if status:
            self.Load_Transactions_Table()
            return True, ''
        return False, data


    # -------------------------------------------------------------------------------------------------
    def Get_List_Item_From_Ident(self, Ident):
        pass
        # Result = self._Connect_Transact_Db
        # if Result != OK:
        #     self._Close_Transact_DataBase()
        #     return Result
        # Sql = """SELECT * FROM TRANSACT WHERE Ident=?"""
        # Data_Tuple  = (Ident,)
        # Result      = self._Make_Execute(Sql, Data_Tuple)
        # self._Close_Transact_DataBase()
        # if Result[0]== OK:
        #     self._Close_Transact_DataBase()
        #     return Result[1]    # List
        # else:
        #     self._Close_Transact_DataBase()
        #     return Result[1]     # Diagnostic

    # -------------------------------------------------------------------------------------------------
    def Get_Transact_Year_ListInData(self):
        Full_Transact_filename = self.Get_sel_dictionary_value(TRANSACT_FILENAME)

        if Full_Transact_filename == UNKNOWN:
            return [0, []]
        Transact_Dir  = Get_Dir_Name(Full_Transact_filename)  # Get TRANSACTIONS directory
        Transact_List = os.listdir(Transact_Dir)
        if not Transact_List:
            return [0, []]
        Years_List = []
        for Filename in Transact_List:
            if TRANSACT in Filename:           # Transact_2024.db
                strYear = Filename[9:13]
                if CheckInteger(strYear):
                    iYear = int(strYear)
                    Years_List.append(iYear)    # [2020, ..., 2024]
        SelectedFile = Get_File_Name(Full_Transact_filename)
        strYear = SelectedFile[9:13]
        return [strYear, Years_List]

    # -------------------------------------------------------------------------------------------------
    def _Find_Rec_InTransactions_List(self):
        for Transact in self._Transact_Table_Order:
            if  self.Conto   == Transact[IX_TRANSACT_CONTO] and \
                self.Contab  == Transact[IX_TRANSACT_CONTAB] and \
                self.Valuta  == Transact[IX_TRANSACT_VALUTA] and \
                self.flAccr  == Transact[IX_TRANSACT_ACCRED] and \
                self.flAddeb == Transact[IX_TRANSACT_ADDEB] and \
                self.FullDes == Transact[IX_TRANSACT_FULL_DESC]:
                    return Transact
        return []

    # -------------------------------------------------------------------------------------------------
    # Record No Code:     [nRow,   Contab, Valuta, 'Accr', 'Addeb', FullDes]
    # Record to insert :  [(),     Conto,  Contab, Valuta, TRdesc, 'Accr',  'Addeb', TRcode, FullDes]
    # Record on Database: [Ident,  Conto,  Contab, Valuta, TRdesc, flAccr,  flAddeb, TRcode, FullDes]
    # -------------------------------------------------------------------------------------------------
    def _Find_Rec_InTransactions(self): # return [OK, fetch_list] or  [NOK, ' Diagnostic']
        pass
        # Result = self._Connect_Transact_Db  # connect always here;  if connected pass
        # if Result != OK:
        #     return Result
        # Sql = "SELECT * FROM TRANSACT WHERE Conto=? AND Contab=? AND Valuta=? AND Accred=? AND Addeb=? AND FullDes=?"
        # Data = [self.Conto, self.Contab, self.Valuta, self.flAccr, self.flAddeb,self.FullDes]
        # Result     = self._Make_Execute(Sql, Data)
        # self._Close_Transact_DataBase()  #  it will be closed at the end of loop using this  method ###
        # return Result

    # -----------------------------------------------------------------------------------------------
    def _Update_Transact_Record(self):
        pass
        # Sql      = "UPDATE TRANSACT SET (Conto=?, Contab=?, Valuta=?,Accred=?, Addeb=?, TRdesc=? TRcode=?, FullDes=?) WHERE Ident==?"
        # Sql_Data = (self.Conto, self.Contab, self.Valuta, self.Accred, self.Addeb, self.Descr, self.TRcode, self.FullDes, self.Ident)
        # MessgErr = ''
        # try:
        #     self._Transact_Cursor.execute(Sql, Sql_Data)        # Database is already connected
        #     self._Transact_Connected.commit()
        # except sqlite3.Error as e:  # in case of error nothing change
        #     MessgErr = 'ERROR on Updating:\n\n' + 'Record: ' + str(self.Ident) + '\n\n'
        #     MessgErr += ' in Transactions Table:\n\n'
        #     strErr = Db_Error(e)
        #     MessgErr += strErr
        # # finally:
        # #     pass
        # # self._Close_Transact_DataBase()                         # Database closed
        # if MessgErr:
        #     return [NOK, MessgErr]
        # return [OK, []]

    # -------------------------------------------------------------------------------------------------
    def Get_Rows_WithCod_List(self):
        return self._With_Code_Tree_List

    # -------------------------------------------------------------------------------------------------
    def Get_Records_ToInsert_List(self):
        return self._records_to_insert_list

    # -------------------------------------------------------------------------------------------------
    def _Get_Months_Lengths(self, List):
        self.Dummy = 0
        Len_List = []
        for Index in range(0, 12):
            Len_List.append(len(List[Index]))
        return Len_List
    pass
    # -------------------------------------------------------------------------------------------------
    def Get_Transactions_Tables_Lengths(self):
        Full_Transact_List_Len = len(self._Full_Transact_List)
        Full_Contab_List_Len   = len(self._Full_Contab_List)
        Full_Valuta_List_Len   = len(self._Full_Valuta_List)

        Full_Generic_List_Len        = len(self._Full_Generic_List)
        Full_Generic_Contab_List_Len = len(self._Full_Generic_Contab_List)
        Full_Generic_Valuta_List_Len = len(self._Full_Generic_Valuta_List)

        Month_Contab_List_Len = self._Get_Months_Lengths(self._Month_Contab_List)
        Month_Valuta_List_Len = self._Get_Months_Lengths(self._Month_Valuta_List)
        Generic_Month_Contab_List_Len = self._Get_Months_Lengths(self._Generic_Month_Contab_List)
        Generic_Month_Valuta_List_Len = self._Get_Months_Lengths(self._Generic_Month_Valuta_List)
        return [Full_Transact_List_Len,
                Full_Contab_List_Len, Full_Valuta_List_Len,
                Month_Contab_List_Len, Month_Valuta_List_Len,
                Full_Generic_List_Len,
                Full_Generic_Contab_List_Len, Full_Generic_Valuta_List_Len,
                Generic_Month_Valuta_List_Len, Generic_Month_Contab_List_Len
                ]

    # ---------------------------------------------------------------------------------------------
    def Get_Xlsx_Month_List_Lengts(self):
        Total = [0, 0, 0, 0]
        for List in self._Xlsx_Month_Contab_List:
            Total[0] += len(List)
            pass
        for List in self._Xlsx_Month_Valuta_List:
            Total[1] += len(List)
            pass
        for List in self._Xlsx_Month_Generic_Contab_List:
            Total[2] += len(List)
            pass
        for List in self._Xlsx_Month_Generic_Contab_List:
            Total[3] += len(List)
            pass
        return Total

# =====================================================================================================


# ========================== #
#                            #
Data_Manager = Transact_Db() #
#                            #
# ========================== #
