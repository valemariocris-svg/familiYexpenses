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

        # self.Ident  = None # [IX_TRANSACT_IDENT]    # Transact_Db uses without underscore (_)
        # self.Conto  = None # [IX_TRANSACT_CONTO]
        # self.Contab = None # [IX_TRANSACT_CONTAB]
        # self.Valuta = None # [IX_TRANSACT_VALUTA]
        # self.Descr  = None # [IX_TRANSACT_TR_DESC]
        # self.Accred = None # [IX_TRANSACT_ACCRED]
        # self.Addeb  = None # [IX_TRANSACT_ADDEB]
        # self.flAccr = None
        # self.flAddeb= None
        # self.TRcode = None # [IX_TRANSACT_TR_CODE]
        # self.FullDes= None # [IX_TRANSACT_FULL_DESC]

        self.Row_To_Del         = []
        self._Count_Contab_Val  = 0
        self._Rows_Tot_xMonth   = None
        self._Found_Except      = False
        self._Transactions_Exceptions = None

        # self._Full_Transact_List = []
        # self._Full_Contab_List   = []
        # self._Full_Valuta_List   = []
        # self._Month_Contab_List  = []
        # self._Month_Valuta_List  = []

        # self._Full_Generic_List         = []
        # self._Full_Generic_Contab_List  = []
        # self._Full_Generic_Valuta_List  = []
        # self._Generic_Month_Contab_List = []
        # self._Generic_Month_Valuta_List = []
        self.rows_inserted_list                 = []
        self.with_code_rows_to_be_inserted_list = []
        self.no_codes_rows_to_be_inserted_list  = []
        self._records_to_insert_list            = []

        self.tot_with_code_rows_to_be_inserted  = 0
        self.tot_nocodes_rows_to_be_inserted    = 0
        self._TotTransact_ToBeInserted          = 0
        self._transactions_map  = {} # dictionary for finding recods on transact Db

    # -------------------------------------------------------------------------------------------------
    def Get_Full_Xlsx_Transact_Ident(self):
        return [self._Xlsx_Conto, self._Xlsx_Year, self._Xlsx_Month, self._Transact_Year]

    # -------------------------------------------------------------------------------------------------
    def Get_Transact_recs_asis(self):
        return self._Transact_Records_as_is

    # -------------------------------------------------------------------------------------------------
    def Get_Transact_recs_ordered(self):
        return self._Transact_Table_Order

    # -------------------------------------------------------------------------------------------------
    def Get_Transact_NormalCode_List(self):
        return self._Transact_Records_NormalCode

    # -------------------------------------------------------------------------------------------------
    def Get_Transact_GenericCode_List(self):
        return self._Transact_Records_GenericCode

    # ---------------------------------------------------------------------------------------------
    #                     0    1     2      3      4      5      6      7        8      9
    # List_Transact_DB :  Id  nRow  Conto Contab Valuta Accred  Addeb  TR_Desc TRcode FullDesc
    # ----------------------------------------------------------------------------------------------
    def Load_Transactions_Table(self) -> tuple[bool, str | list]:
        _filename = self.Get_sel_dictionary_value(TRANSACT_FILENAME)
        if not Gl_Cek_Transactions_Name(_filename):
            return False, 'Transactions filename NOT K\nplease selecte a correct filename'
        status, data = Gl_Cek_Transactions_Name(_filename)
        if not status:
            return False, data

        self._tTransact_Year               = Get_Transactions_Year(_filename)
        self._Transact_Records_as_is       = []    # TRANSACT table as in Database
        self._Transact_Records_NormalCode  = []    #9 TRANSACT table normal code
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
            status, data = self._query_execute(TRANSACT_FILE, sql, (), CLOSE_DB)
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

    # ----------------------------------------------------------------------------------------------------- #
    # Chiave per la ricerca nel Db movimenti:                                                               #
    # (conto, nRow, contab, valuta, Accred, Addeb)                                                          #
    # l'elento nRow da' la certezza che non si creino o si saltino doppioni (ass. Domestic ...)             #
    # PERO' nella inserzione dei movimenti nel Db bisogna ricreare un Transact_yyyy.db                      #
    # ogni volta che si cambia file xlsx, mentre finche' si usa sempre lo stesso,                           #
    # si possono inerire movimenti  in piu' volte                                                           #                                                                                         #
    # ----------------------------------------------------------------------------------------------------- #
    # Liste:                                                                                                #
    # Rows_WithCode_List,                   Rows_NoCode_List,                 rows_inserted_list,           #
    # with_code_rows_to_be_inserted_list,   no_codes_rows_to_be_inserted_list                               #
    # Premessa:                                                                                             #
    # Alle righe contenute nel file xlsx, di cui non si e' trovato un codice standard corrispondente,       #
    # si potra' abbinare soltanto un codice generico (o creandone uno nuovo standard ad hoc)                #
    # per cui nel Db si avranno solo record con codice standard  o con  codice generico                     #
    #                                                                                                       #
    # Nota iniziale: le righe di xlsx vengono suddivise  in Rows_WithCod_List  e  Rows_NoCode_List          #
    # Si fanno due passate di ricerca: una sulla lista WithCode ed una sulla lista NoCode:                  #
    # 1) Passata WithCode:                                                                                  #
    #    genera le liste   rows_inserted_list   e   with_code_rows_to_be_inserted_list                      #
    #    nella Top_Codes_Mngr verra' usata quest' ultima lista nella Frame  WithCode                        #
    # 2) Passata NoCode:                                                                                    #
    #    se una riga viene trovata nel Db  significa che le e' stato assegnato un codice generico           #
    #    quindi verra' aggiunta alla rows_inserted_list (cod.gen) e tolta dalla NoCode                      #
    # 3) Risultato finale:                                                                                  #
    #    rows_inserted_list   conterra record con codice standard e generico                                #
    #    with_code_rows_to_be_inserted_list     per la visualizzazione i  Top_Codes_Mngr                    #
    #    la   Rows_NoCode_List   debitamente decurtata, conterra' solo le liste NoCode da abbinare          #
    #    ad un codice generico, oppure ad un codice standard creato seduta stante ad hoc                    #
    #    e sara' visualizzata sulla NoCodes  Frame                                                          #
    # 4) Gestione in Top_Codes manager:                                                                     #
    #    a) abbinare un codice generico: +1 no_codes_rows_to_be_inserted_list                               #
    #                                    -1 NoCodes_List                                                    #
    #     b) creare un codice standard o generico:  rilanciare  Create_records_to_insert_list               #
    # 5) Calcolo totali righe in Db o da inserire:                                                          #
    #    a) rows_inserted_list = ( codici standard e generici)                                              #
    #    b) rows_to_be_inserted = with_code_rows_to_be_inserted_list + no_codes_rows_to_be_inserted_list    #
    #    c) NoCodes_List        = rimanenza nella lista dopo ricerca nel Db o spostamenti per assegnazione  #
    # 6) Sequenza gestione rows e movimenti:                                                                #
    #    a) Load Xlsx file (_create_With_Out_codes_lists)                                                   #
    #    b) Check_create_transact_database_for_xlsx_filename select Transact_yyyy o creazione               #
    #    c) Load_Transact_Mngr()                                                                            #
    #    d Create_records_to_insert_list                                                                    #
    #    d) Richiamare questa sequenza ad ogni modifica effettuata in Top_Codes_Mng + Load_Codes            #
    # ----------------------------------------------------------------------------------------------------- #
    def Create_records_to_insert_list(self):
        self.rows_inserted_list                 = []
        self.with_code_rows_to_be_inserted_list = []   # the list of records to be inserted in transactions database
        self.no_codes_rows_to_be_inserted_list  = []
        self.tot_with_code_rows_to_be_inserted   = 0
        self.tot_nocodes_rows_to_be_inserted     = 0

        #   crea la mappa come dizionario vuoto: la chiave e' una tupla di 5 elementi
        #   ed il valore
        self._transactions_map = {}
        for record in self._Transact_Records_as_is:
            nRow       = record[IX_TRANSACT_NROW]
            conto      = record[IX_TRANSACT_CONTO]
            dateContab = record[IX_TRANSACT_CONTAB]
            dateValuta = record[IX_TRANSACT_VALUTA]
            credit     = record[IX_TRANSACT_ACCRED]
            debit      = record[IX_TRANSACT_ADDEB]

            # Crea la chiave unica (una tupla) e la inserisce nel dizionario
            key = (nRow, conto, dateContab, dateValuta, credit, debit)
            self._transactions_map[key] = record[IX_TRANSACT_NROW]  # numero riga

        # creazione della lista dei record caricati da .XLSX ma non presenti nel database
        # esaminando la lista delle righe xlsx, di cui si e' trovato un codice Db
        for row in self._tWith_Code_Tree_List:
            conto      = self._tXlsx_Conto      # settato nel tirar su .xlsx
            nRow       = row[IX_WITH_CODE_NROW]
            dateContab = row[IX_WITH_CODE_CONTAB]
            dateValuta = row[IX_WITH_CODE_VALUTA]
            credit     = row[IX_WITH_CODE_ACCRED]
            debit      = row[IX_WITH_CODE_ADDEB]
            TRdesc     = row[IX_XLSX_WITH_TRDESC]
            TRcode     = row[IX_XLSX_WITH_TRCODE]
            FullDesc   = row[IX_XLSX_WITH_FULLDES]

            record = [nRow, conto, dateContab, dateValuta, credit, debit, TRdesc,
                      TRcode, FullDesc]
            if (nRow, conto, dateContab, dateValuta, credit, debit) in self._transactions_map:
                self.rows_inserted_list.append(record)
            else:
               self.with_code_rows_to_be_inserted_list.append(record)
            pass
        pass
        # ========================================================================================
        # creazione della lista dei record caricati da .XLSX ma non presenti nel database
        # esaminando la lista delle righe xlsx, di cui NON si e' trovato un codice Db
        for row in self._tWihtout_Code_Tree_List:
            conto      = self._tXlsx_Conto      # settato nel tirar su .xlsx
            nRow       = row[IX_NO_CODE_NROW]
            dateContab = row[IX_NO_CODE_CONTAB]
            dateValuta = row[IX_NO_CODE_VALUTA]
            credit     = row[IX_NO_CODE_ACCRED]
            debit      = row[IX_NO_CODE_ADDEB]
            FullDesc   = row[IX_NO_CODE_FULL_DESCR]

            record     = [nRow, conto, dateContab, dateValuta, credit, debit, FullDesc],
            if not (nRow, dateContab, dateValuta, credit, debit) in self._transactions_map:
                self.no_codes_rows_to_be_inserted_list.append(record)
                pass
            pass
        pass

    # -------------------------------------------------------------------------------------------------
    def _Set_Transact_Year(self):
        # asTransact_2024.db
        FullFilename = self.Get_sel_dictionary_value(TRANSACT_FILENAME)
        if FullFilename != UNKNOWN:
            filename = Get_File_Name(FullFilename)
            self._tTransact_Year = int(filename[9:13])
        else:
            self._tTransact_Year = None

    # -------------------------------------------------------------------------------------------------
    #   (auto)  Id, riga, conto, contab, valuta, accred, addeb, TRdesc, TRcode, full_desc
    def Get_Transact_Table(self):
        return self.Get_Transact_recs_asis()

    # -------------------------------------------------------------------------------------------------
    def Get_Len_Transact_Table(self):
        return len(self._Transact_Table_Order)

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

    # -------------------------------------------------------------------------------------------------
    # def _Create_Transact_List_perMonth(self):
    #     # DateIndex = IX_TRANSACT_VALUTA
    #     DateIndex = IX_TRANSACT_CONTAB
    #     # self.Transact_xMonth_List = [[]] * 12
    #     # self.DateCount_PerMonth   = [0]  * 12
    #     self.Transact_xMonth_List = [ [], [], [], [], [], [], [], [], [], [], [], [] ]
    #     self.DateCount_PerMonth   = [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0  ]
    #     for Rec in self._Transact_Table_Order:
    #         iMonth = 0            # self.CheckForInsert(Rec)
    #         if iMonth >= 0:
    #             Counts = self.DateCount_PerMonth[iMonth]
    #             Counts += 1
    #             if Counts > 10:
    #                 Counts = 0
    #             self.DateCount_PerMonth[iMonth] = Counts
    #             # ['Date', 'Co', 'Description', 'Credits  ', 'Debits  ']
    #             FullDate = Rec[DateIndex]
    #             Date     = Set_Month_Day(FullDate, Counts)
    #             TRcode   = Rec[IX_TRANSACT_TR_CODE]
    #             TRdescr  = self.Get_TrDesc_FromCode(TRcode)
    #             Conto    = CONTO_RED[Rec[IX_TRANSACT_CONTO]]
    #             View_Rec = [Date, Conto, TRdescr, Rec[IX_TRANSACT_ACCRED],
    #                         Rec[IX_TRANSACT_ADDEB], Rec[IX_TRANSACT_IDENT]]
    #             self.Transact_xMonth_List[iMonth].append(View_Rec)
    #             pass
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

    # # -------------------------------------------------------------------------------------------------
    # def Get_Transact_Year_ListInData(self):
    #     Full_Transact_filename = self.Get_sel_dictionary_value(TRANSACT_FILENAME)
    #
    #     if Full_Transact_filename == UNKNOWN:
    #         return [0, []]
    #     Transact_Dir  = Get_Dir_Name(Full_Transact_filename)  # Get TRANSACTIONS directory
    #     Transact_List = os.listdir(Transact_Dir)
    #     if not Transact_List:
    #         return [0, []]
    #     Years_List = []
    #     for Filename in Transact_List:
    #         if TRANSACT in Filename:           # Transact_2024.db
    #             strYear = Filename[9:13]
    #             if CheckInteger(strYear):
    #                 iYear = int(strYear)
    #                 Years_List.append(iYear)    # [2020, ..., 2024]
    #     SelectedFile = Get_File_Name(Full_Transact_filename)
    #     strYear = SelectedFile[9:13]
    #     return [strYear, Years_List]

    # -------------------------------------------------------------------------------------------------
    # Record No Code:     [nRow,   Contab, Valuta, 'Accr', 'Addeb', FullDes]
    # Record to insert :  [(),     Conto,  Contab, Valuta, TRdesc, 'Accr',  'Addeb', TRcode, FullDes]
    # Record on Database: [Ident,  Conto,  Contab, Valuta, TRdesc, flAccr,  flAddeb, TRcode, FullDes]
    # -------------------------------------------------------------------------------------------------
    def Get_transact_rec_from_id(self, Id) -> tuple[bool, list | str]: # return [OK, fetch_list] or  [NOK, ' Diagnostic']
        sql  = "SELECT * FROM TRANSACT WHERE Ident=?"
        status, data = self._query_execute(TRANSACT_FILE, sql, (Id,), CLOSE_DB)
        if not status:
            return False, f"record with Ident {Id} not found"
        return True, data

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
    # def Get_Transactions_Tables_Lengths(self):
    #     Full_Transact_List_Len = len(self._Full_Transact_List)
    #     Full_Contab_List_Len   = len(self._Full_Contab_List)
    #     Full_Valuta_List_Len   = len(self._Full_Valuta_List)
    #
    #     Full_Generic_List_Len        = len(self._Full_Generic_List)
    #     Full_Generic_Contab_List_Len = len(self._Full_Generic_Contab_List)
    #     Full_Generic_Valuta_List_Len = len(self._Full_Generic_Valuta_List)
    #
    #     Month_Contab_List_Len = self._Get_Months_Lengths(self._Month_Contab_List)
    #     Month_Valuta_List_Len = self._Get_Months_Lengths(self._Month_Valuta_List)
    #     Generic_Month_Contab_List_Len = self._Get_Months_Lengths(self._Generic_Month_Contab_List)
    #     Generic_Month_Valuta_List_Len = self._Get_Months_Lengths(self._Generic_Month_Valuta_List)
    #     return [Full_Transact_List_Len,
    #             Full_Contab_List_Len, Full_Valuta_List_Len,
    #             Month_Contab_List_Len, Month_Valuta_List_Len,
    #             Full_Generic_List_Len,
    #             Full_Generic_Contab_List_Len, Full_Generic_Valuta_List_Len,
    #             Generic_Month_Valuta_List_Len, Generic_Month_Contab_List_Len
    #             ]

    # ---------------------------------------------------------------------------------------------
    # def Get_Xlsx_Month_List_Lengts(self):
    #     Total = [0, 0, 0, 0]
    #     for List in self._Xlsx_Month_Contab_List:
    #         Total[0] += len(List)
    #         pass
    #     for List in self._Xlsx_Month_Valuta_List:
    #         Total[1] += len(List)
    #         pass
    #     for List in self._Xlsx_Month_Generic_Contab_List:
    #         Total[2] += len(List)
    #         pass
    #     for List in self._Xlsx_Month_Generic_Contab_List:
    #         Total[3] += len(List)
    #         pass
    #     return Total

# =====================================================================================================


# ========================== #
#                            #
Data_Manager = Transact_Db() #
#                            #
# ========================== #
