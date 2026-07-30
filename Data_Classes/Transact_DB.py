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

        self.Row_To_Del         = []
        self._Count_Contab_Val  = 0
        self._Rows_Tot_xMonth   = None
        self._Found_Except      = False
        self._Transactions_Exceptions = None

        self.all_rows_inserted_list            = []     # the basic rows lists for insert
        self.std_code_rows_to_be_insertd_list  = []
        self.noCode_rows_to_be_inserted_list   = []

        self._transactions_map                 = {}  # dictionary for finding recods on transact Db
        self.Totals_dict                       = Totals_dict_default

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
    # l'elemento nRow da' la certezza che non si creino o si saltino doppioni (ass. Domestic ...)           #
    # PERO' nella inserzione dei movimenti nel Db bisogna ricreare un Transact_yyyy.db                      #
    # ogni volta che si cambia file xlsx, mentre finche' si usa sempre lo stesso,                           #
    # si possono inerire movimenti  in piu' volte                                                           #                                                                                         #
    # ----------------------------------------------------------------------------------------------------- #
    # Liste:                                                                                                #
    # all_rows_inserted_lis(std & generic)  std_code_rows_to_be_insertd_list noCode_rows_to_be_inserted_list#
    # Totale calcolato   = somma(1-3)                                                                       #
    # Premessa:                                                                                             #
    # Alle righe contenute nel file xlsx, di cui non si e' trovato un codice standard corrispondente,       #
    # si potra' abbinare soltanto un codice generico (o creare uno nuovo standard)                          #
    # Nota iniziale:                                                                                        #
    # le righe di xlsx vengono suddivise  in Rows_WithCod_List  e  Rows_NoCode_List                         #
    # Si fanno due passate di ricerca: una sulla lista WithCode ed una sulla lista NoCode:                  #
    # 1) Passata WithCode:                                                                                  #
    #    inizializza  la lista   all_rows_inserted_list   e crea   std_code_rows_to_be_insertd_list         #
    # 2) Passata NoCode:                                                                                    #
    #    Iniizializza noCode_rows_to_be_inserted_list                                                       #
    #    se una riga viene trovata nel Db  significa che le e' stato assegnato un codice generico           #
    #    quindi verra' aggiunta alla  all_rows_inserted_list                                                #
    #    altrimenti viene aggiunta alla noCode_rows_to_be_inserted_list                                     #
    # 3) Risultato finale:                                                                                  #
    #    all_rows_inserted_list:                                                                            #
    #       conterra' le righe  con codice standard e generico                                              #
    #    std_code_rows_to_be_insertd_list:                                                                  #
    #       usata da Frame_WithCodes_ToIns                                                                  #
    #    noCode_rows_to_be_inserted_list:                                                                   #
    #       usata dal  Frame_No_Codes                                                                       #
    # 5) Calcolo totali righe in Db o da inserire:                                                          #
    #    a) all_rows_inserted_list = ( codici standard e generici)                                          #
    #    b) rows_to_be_inserted = with_code_rows_to_be_inserted_list + no_codes_rows_to_be_inserted_list    #
    #    c) NoCodes_List        = rimanenza nella lista dopo ricerca nel Db o spostamenti per assegnazione  #
    # 6) Sequenza gestione rows e movimenti:                                                                #
    #    a) Load Xlsx file (_create_With_Out_codes_lists)    (solo in caso di sezione file xlsx)                                              #
    #    b) Check_create_transact_database_for_xlsx_filename  sel. Transact_yyyy o ne crea uno nuovo        #
    #    c) Load_Transact_Mngr()                                                                            #
    #    d Create_rows_to_insert_list                                                                       #
    #    d) Richiamare questa sequenza ad ogni modifica effettuata in Top_Codes_Mng (per xlsx, insert)      #
    #    e) per aggiornamenti Codes_database questa sequenza dev esser sempre invocata                      #
    # ----------------------------------------------------------------------------------------------------- #
    # Codice std inseriti /	Codice std da inserire / NoCode da inserire
    def Create_rows_to_insert_list(self):
        self.all_rows_inserted_list           = []
        self.std_code_rows_to_be_insertd_list = []
        self.noCode_rows_to_be_inserted_list  = []

        #   crea la mappa come dizionario vuoto: la chiave e' una tupla di 5 elementi
        #   ed il valore
        self._transactions_map = {}
        for record in self._Transact_Records_as_is:
            nRow       = record[IX_TRANSACT_NROW]
            conto      = record[IX_TRANSACT_CONTO]
            dateContab = record[IX_TRANSACT_CONTAB]     # from xlsx wit/out rows is datetime
            dateValuta = record[IX_TRANSACT_VALUTA]     # is string
            credit     = record[IX_TRANSACT_ACCRED]
            debit      = record[IX_TRANSACT_ADDEB]

            # Crea la chiave unica (una tupla) e la inserisce nel dizionario
            key = (nRow, conto, dateContab, dateValuta, credit, debit)
            self._transactions_map[key] = record[IX_TRANSACT_IDENT]  # numero riga
        # creazione della lista dei record caricati da .XLSX ma non presenti nel database
        # esaminando la lista delle righe xlsx, di cui si e' trovato un codice Db
        for row in self._tWith_Code_Tree_List:
            conto      = self._tXlsx_Conto      # settato nel tirar su .xlsx
            nRow       = row[IX_WITH_CODE_NROW]
            dateContab = get_D_M_Y_H_m_S_for_insert(row[IX_WITH_CODE_CONTAB])   # is datetime
            dateValuta = get_D_M_Y_H_m_S_for_insert(row[IX_WITH_CODE_VALUTA])         # from Db fullDate
            credit     = row[IX_WITH_CODE_ACCRED]
            debit      = row[IX_WITH_CODE_ADDEB]
            TRdesc     = row[IX_WITH_CODE_TR_DESCR]
            TRcode     = row[IX_WITH_CODE_TR_CODE]
            FullDesc   = row[IX_WITH_CODE_FULL_DESCR]
            pass
            record = [nRow, conto, dateContab, dateValuta, credit, debit, TRdesc,
                      TRcode, FullDesc]
            if (nRow, conto, dateContab, dateValuta, credit, debit) in self._transactions_map:
                self.all_rows_inserted_list.append(record)
            else:
               self.std_code_rows_to_be_insertd_list.append(record)
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

            record     = [nRow, conto, dateContab, dateValuta, credit, debit, FullDesc]
            if not (nRow, dateContab, dateValuta, credit, debit) in self._transactions_map:
                self.noCode_rows_to_be_inserted_list.append(record)
            else:
                self.all_rows_inserted_list.append(record)
            pass
        self.Totals_dict[TOT_ROWS_INSERTED]    = len(self.all_rows_inserted_list)
        self.Totals_dict[TOT_STD_COD_TOBE_INS] = len(self.std_code_rows_to_be_insertd_list)
        self.Totals_dict[TOT_NOCOD_TO_INSERT]  = len(self.noCode_rows_to_be_inserted_list)
        pass

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
    #                   0      1       2      3       4       5       6       7       8
    # Record_List :  (Ident) Conto, Contab, Valuta, Accred, Addeb, TRdesc, TRcode, FullDes)
    # -------------------------------------------------------------------------------------------------
    def Insert_oneRow_on_Transact_Db(self, nRow, Conto, Contab, Valuta, Accred, Addeb, TRdesc, TRcode, FullDes):
        sql = """INSERT INTO TRANSACT (nRow, Conto, Contab, Valuta, Accred, Addeb, TRdesc, TRcode, FullDes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        parameters = (nRow, Conto, Contab, Valuta, Accred, Addeb, TRdesc, TRcode, FullDes)
        status, data = self._query_execute(TRANSACT_FILE, sql, parameters, CLOSE_DB)
        if not status:
            return False, data
        return True, ''

    # --------------------------------------------------------------------------------------------------
    def Insert_std_code_rows_to_be_insertd(self):
        for row in self.std_code_rows_to_be_insertd_list:
            nRow    = row[IX_ROW_TOINS_NROW]
            Conto   = row[IX_ROW_TOINS_CONTO]
            Contab  = row[IX_ROW_TOINS_CONTAB]
            Valuta  = row[IX_ROW_TOINS_VALUTA]
            Accred  = Convert_Str_To_Float(row[IX_ROW_ACCRED])
            Addeb   = Convert_Str_To_Float(row[IX_ROW_ADDEB])
            TRdesc  = row[IX_ROW_TOINS_TR_DESC]
            TRcode  = row[IX_ROW_TOINS_TR_CODE]
            FullDes = row[IX_ROW_TOINS_FULL_DESC]

            sql = """INSERT INTO TRANSACT (nRow, Conto, Contab, Valuta, Accred, Addeb, TRdesc, TRcode, FullDes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            parameters = (nRow, Conto, Contab, Valuta, Accred, Addeb, TRdesc, TRcode, FullDes)
            status, data = self._query_execute(TRANSACT_FILE, sql, parameters, KEEP_OPEN)
            if not status:
                data = f"{data}\n\non inserting row\n{nRow}  {Contab}  {Valuta}  {Accred}  {Addeb}\n"
                return False, data
            # self._query_execute(TRANSACT_FILE, SQL_CLOSE_DB, (), CLOSE_DB)
            #     messg  = f"FATAL ERROR 41:\non inserting row\n{nRow}  {Contab}  {Valuta}  {Accred}  {Addeb}\n"
            #     messg += f"{TRdesc}  {TRcode}\n{FullDes}\n"
            #     return False, messg

        self._query_execute(TRANSACT_FILE, SQL_CLOSE_DB, (), CLOSE_DB)
        return True, ''

    # -------------------------------------------------------------------------------------------------
    # Record No Code:     [nRow,   Contab, Valuta, 'Accr', 'Addeb', FullDes]
    # Record to insert :  [(),     nRow, Conto,  Contab, Valuta, TRdesc, 'Accr',  'Addeb', TRcode, FullDes]
    # Record on Database: [Ident,  nRow, Conto,  Contab, Valuta, TRdesc, flAccr,  flAddeb, TRcode, FullDes]
    # -------------------------------------------------------------------------------------------------
    def Get_transact_rec_from_id(self, Id) -> tuple[bool, list | str]: # return [OK, fetch_list] or  [NOK, ' Diagnostic']
        sql  = "SELECT * FROM TRANSACT WHERE Ident=?"
        status, data = self._query_execute(TRANSACT_FILE, sql, (Id,), CLOSE_DB)
        if not status:
            return False, f"record with Ident {Id} not found"
        return True, data


    # self.all_rows_inserted_list            = []
    # self.std_code_rows_to_be_insertd_list  = []
    # self.noCode_rows_to_be_inserted_list   = []
    def get_all_rows_inserted_list(self):
        return self.all_rows_inserted_list

    def get_std_code_rows_to_be_insertd_list(self):
        return self.std_code_rows_to_be_insertd_list

    def get_noCode_rows_to_be_inserted_list(self):
        return self.noCode_rows_to_be_inserted_list

    # -------------------------------------------------------------------------------------------------
    def get_totals_dict_as_list(self, Conto):
        self.Totals_dict[TOT_CONTO] = Conto
        Tot_calculated = self.Totals_dict[TOT_ROWS_INSERTED] + self.Totals_dict[TOT_STD_COD_TOBE_INS] + \
                         self.Totals_dict[TOT_NOCOD_TO_INSERT]
        self.Totals_dict[TOT_CALCULATED]  = Tot_calculated
        self.Totals_dict[TOT_ROWS_IN_XLSX] = self.Get_Length_Xlsx()
        totals_list = []
        for key, value in self.Totals_dict.items():
            totals_list.append(str(value))
        return [totals_list]

    def get_tot_rows_inserted(self):
        return self.Totals_dict[TOT_ROWS_INSERTED]

    def get_tot_std_cod_to_be_inserted(self):
        return self.Totals_dict[TOT_STD_COD_TOBE_INS]

    def get_tot_rows_NoCode_to_insert(self):
        return self.Totals_dict[TOT_NOCOD_TO_INSERT]

    def get_tot_dict_totals(self):
        return self.Totals_dict[TOT_CALCULATED]

    # --------------------------------------------------------------------------------------------------
    def update_totals_dict(self, key, value):
        self.Totals_dict[key] = value

# ========================== #
#                            #
Data_Manager = Transact_Db() #
#                            #
# ========================== #
