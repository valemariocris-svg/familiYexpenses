# =========================================================================== #
#               -----   Codes_DB.py   -----                                   #
#          class  for Transactions Codes Database                             #
#     it contains the private methods for codes database                      #
# =========================================================================== #

from operator import itemgetter
import sqlite3
# import re

from Data_Classes.Filesnames_Mngr import Files_Names_Manager
from Common.Common_Functions import *

# ---------------------------------------------------------------------------------
class Codes_DB_Private(Files_Names_Manager):
    def __init__(self):
        super().__init__()
        self.Dummy = 0

        self._database_connect = None
        self._database_cursor  = None

        # ==================================================================================================== #
        #                                     0      1        2       3     4         5       6        7
        self._TR_Codes_Table   = []  # TRCode GRcode SPcode  TRdesc StrToSear FullDesc
        self._TR_Codes_Full    = []  # TRcode GRcode CAcode  TRdesc GRdesc    CAdesc StrToSear FullDesc
        self._GR_Codes_Table   = []  # GRcode GRdescr  CAcode
        self._CA_Codes_Table   = []  # CAcode CAdescr

        self._GR_Codes_Ordered = []  # GRcode GRdescr  CAcode     ordered by GRdescr
        self._CA_Codes_Ordered = []  # CAcode CAdescr             ordered by CAdescr

        self._GRdescr_Ordered_List = []  # only GRdescr ordered
        self._CAdescr_Ordered_List = []  # only Cadescr ordered
        self._GRrecord_CArecord    = []

        self._tTR_Codes_Table      = []
        self._tGR_Codes_Table      = []
        self._tCA_Codes_Table      = []
        self._Extraorinary_TRcode_List = [] # if CAcode==EXTRAORDINARY_CAT_CODE the TRrec is inserted

        self._Multi_Codes_Matching_List = []  # full descriptions matching with the same StrToFind

    # -----------------------------------------------------------------------------------
    def _open_database(self, database) -> tuple[bool, str]:
        # -----------------------   DATABASE SELECTIONS    --------------------------
        if database == CODES_FILE:
            _filename = self.Get_sel_dictionary_value(CODES_FILENAME)
            status, data = Gl_Cek_Codes_Name(_filename)
            if not status:
                return False, "FATAL ERROR 21:\nfile database codici corrotto\nBisogna aggiustarlo"
            sql ="SELECT * FROM TRANSACT_CODES"

        else:
            _filename = self.Get_sel_dictionary_value(TRANSACT_FILENAME)
            if _filename == UNKNOWN:
                return False, "FATAL ERROR 22:\nfile database movimenti sconosciuto\nBisogna crearlo"
            status, data = Gl_Cek_Transactions_Name(_filename)
            if not status:
                return False, "FATAL ERROR 21:\nfile database movimenti corrotto\nBisogna aggiustarlo"
            sql = "SELECT * FROM TRANSACT"

        # ----------   COMMON  CODE   ------------------------------------------
        # Reset se la connessione precedente è chiusa
        if hasattr(self, '_database_connect') and not self._database_connect is None:
            try:
                self._database_connect.execute(sql)   # Test di validita'
                return True, ''
            except sqlite3.Error as e:
                print(f"Errore apertura database: {e}")
                self._database_connect = None  # Era morta, la resettiamo

        # 2. Se non esiste o era morta, apriamola
        try:
            # _filename = self.Get_sel_dictionary_value(CODES_FILENAME)
            self._database_connect = sqlite3.connect(_filename)
            self._database_cursor = self._database_connect.cursor()
            return True, ''
        except sqlite3.Error as e:
            return False, f"FATAL ERROR 23:\nErrore apertura database: {e}"
        finally:
            pass

    # --------------------------------------------------------------------------------------
    def _close_db_connection(self):
        if hasattr(self, '_database_connect'):
            try:
                # È buona pratica chiudere prima il cursore se esiste
                if hasattr(self, '_database_cursor'):
                    self._database_cursor.close()
                self._database_connect.close()
                return True, ''
            except sqlite3.Error as e:
                return False, f"FATAL ERROR 51:\nErrore in chiusura database\n{e}"
            finally:
                pass
        return True, ''

    # --------------------------------------------------------------------------------------
    #  Apre il Codes DB, esegue una query (SELECT o UPDATE) e chiude
    #  la connect se CLOSE_DB   oppure  NO se  KEEP_OPEN
    def _query_execute(self, database, sql, parameters=(), close=True, all_records=False):
        # Validazione rapida del database
        if database not in [CODES_FILE, TRANSACT_FILE]:
            return False, f"Error: Database {database} not recognized"
        # 1. simple request for closing db
        if sql == SQL_CLOSE_DB:
            self._close_db_connection()
            # IMPORTANTE: resettiamo l'oggetto a None così alla prossima chiamata
            # il test 'if not self._database_connect' funzionerà correttamente
            self._database_connect = None
            return True, ''
        # 2. Open
        status, data = self._open_database(database)  # it remains open whith NO_CLOSE request
        if not status:
            return False, data
        try:
            # 3. Esecuzione
            self._database_cursor.execute(sql, parameters)
            sql_clean = sql.strip().upper()
            # Gestione delle SELECT
            if sql_clean.startswith('SELECT'):
                # CASO A: È una query di verifica EXISTS
                if 'EXISTS' in sql_clean:
                    record = self._database_cursor.fetchone()
                    # Se riga esiste e il primo elemento è 1, allora esiste
                    if record and record[0] == 1:
                        return True, True  # Restituiamo True (successo) e True (esiste)
                    else:
                        return True, False  # Restituiamo True (successo) e False (non esiste)

                # CASO B: È una query di estrarre un solo record con Id
                # Modifichiamo solo questa riga:
                # Usa fetchone SOLO SE c'è WHERE e NON hai chiesto esplicitamente tutti i record
                elif 'WHERE' in sql_clean and not all_records:
                    data = self._database_cursor.fetchone()     # is  (nCode,)
                    return True, data
                else:
                    # Cadranno qui tutte le SELECT senza WHERE, E le select con WHERE che hanno all_records=True
                    data = self._database_cursor.fetchall()
                    return True, data
            else:
                # Se è INSERT/UPDATE/DELETE, CREATE  salviamo le modifiche
                self._database_connect.commit()
                return True, ''

        except sqlite3.Error as e:
            str_Err = f"FATAL ERROR 24:\nError on fetching codes records:\n{e}"
            return False, str_Err
        finally:
            # 4. Chiusura garantita (anche in caso di errore)
            if close:
                status, dataclose = self._close_db_connection()
                if not status:
                    return False, dataclose
                # IMPORTANTE: resettiamo l'oggetto a None così alla prossima chiamata
                # il test 'if not self._database_connect' funzionerà correttamente
                self._database_connect = None
                # return True, data
            pass

    # -------------------------------------------------------------------------------------------
    def _get_codes_tables(self):
        self._tTR_Codes_Table  = []  # TRCode GRcode   SPcode   TRdesc  StrToSear  FullDesc
        self._tGR_Codes_Table  = []  # GRcode GRdescr  CAcode
        self._tCA_Codes_Table  = []  # CAcode CAdescr

        status, data = self._query_execute(CODES_FILE, "SELECT * FROM TRANSACT_CODES", (), CLOSE_DB)
        if not status:
            return status, data
        else:
            self._tTR_Codes_Table = data

        status, data = self._query_execute(CODES_FILE, "SELECT * FROM GROUP_CODES", (), CLOSE_DB)
        if not status:
            return status, data
        else:
            self._tGR_Codes_Table = data

        status, data = self._query_execute(CODES_FILE, "SELECT * FROM CATEGORY_CODES", (), CLOSE_DB)
        if not status:
                return status, data
        else:
            self._tCA_Codes_Table = data
        return True, ''

    # -------------------------------------------------------------------------------------- #
    #      private  _methods invoked only inside  the data classes  chain                    #
    #    in case of error on loading TR-GR-CA Tables nothing is changed                      #
    #    return [OK, '']   [STRING, Err Diagnostic]   [MULTI, [_Multi_Codes_Matching_List]   #
    # -------------------------------------------------------------------------------------- #
    def _Load_Codes_Tables(self):
        self._tTR_Codes_Table  = []  # TRCode GRcode   SPcode   TRdesc  StrToSear  FullDesc
        self._tGR_Codes_Table  = []  # GRcode GRdescr  CAcode
        self._tCA_Codes_Table  = []  # CAcode CAdescr

        status, data = self._get_codes_tables()
        if not status:
            return status, data

        self.Tree_Codes_View_List = []
        self._Set_Codes_Tables()
        return True, ''

    # --------------------------------------------------------------------------------------------
    def _Set_Codes_Tables(self):
        self._GR_Codes_Table = self._tGR_Codes_Table
        self._CA_Codes_Table = self._tCA_Codes_Table
        self._TR_Codes_Full  = []
        self._TR_Codes_Table = []
        for Rec in self._tTR_Codes_Table:
            TRlist = list(Rec)
            TRcode = Rec[IX_TR_TR_CODE]
            TRdesc = Rec[IX_TR_TR_DESC]
            GRcode = Rec[IX_TR_GR_CODE]
            GRrec = self._Get_GR_Record(GRcode)
            GRdesc = GRrec[IX_GR_GR_DESC]
            CAcode = self._Get_CA_Code_From_GR_Code(GRcode)
            TRlist[IX_TR_CA_CODE] = CAcode
            CArec = self._Get_CA_Record(CAcode)
            CAdesc = CArec[IX_CA_CA_DESC]
            TRlist[IX_TR_CA_CODE] = CAcode

            self._TR_Codes_Table.append(TRlist)
            self._TR_Codes_Full.append([ TRcode, GRcode, CAcode,
                                         TRdesc, GRdesc, CAdesc,
                                         TRlist[IX_TR_TR_STR_TO_FIND], TRlist[IX_TR_TR_FULL_DESC] ])
        self._Set_TR_View_List()
        self._GR_CA_Lists_Order()

    # ---------------------------------------------------------------------------------------
    def _GR_CA_Lists_Order(self):
        self._GR_Codes_Ordered = sorted(self._GR_Codes_Table, key=itemgetter(1))
        self._CA_Codes_Ordered = sorted(self._CA_Codes_Table, key=itemgetter(1))

    # ---------------------------------------------------------------------------------------
    def _Set_TR_View_List(self):
        #  TRcode  TRDesc    GRdesc    CAdesc   StrToSear
        self.Tree_Codes_View_List = []
        for Rec in self._TR_Codes_Table:
            #     0       1         2        3         4
            #  TRcode  TRDesc    GRdesc    CAdesc   StrToFind
            TRcode = Rec[IX_TR_TR_CODE]

            GRcode = Rec[IX_TR_GR_CODE]
            GRrec  = self._Get_GR_Record(GRcode)
            GRdesc = GRrec[IX_GR_GR_DESC]
            CAcode = GRrec[IX_GR_CA_CODE]
            CAdesc = self._Get_CA_Descr(CAcode)

            List_View_Codes = [TRcode,                    # 0
                               Rec[IX_TR_TR_DESC],        # 1
                               GRdesc,                    # 2
                               CAdesc,                    # 3
                               Rec[IX_TR_TR_STR_TO_FIND]] # 4
            self.Tree_Codes_View_List.append(List_View_Codes)
        self._GR_Table_Ordered     = []
        self._GRdescr_Ordered_List = []
        for Rec in self._GR_Codes_Table:
            self._GRdescr_Ordered_List.append(Rec[IX_GR_GR_DESC])
            self._GR_Table_Ordered.append(Rec)
        self._GRdescr_Ordered_List.sort()

        self._CAdescr_Ordered_List = []
        for Rec in self._CA_Codes_Table:
            self._CAdescr_Ordered_List.append(Rec[IX_CA_CA_DESC])
        self._CAdescr_Ordered_List.sort()

    # ---------------------------------------------------------------------------------------
    def _Get_GR_Record(self, GRcode):
        for Rec in self._GR_Codes_Table:
            if Rec[IX_GR_GR_CODE] == GRcode:
                return Rec
        return [0, UNKNOWN, 0]

    def _Get_CA_Record(self, CAcode):
        for Rec in self._CA_Codes_Table:
            if Rec[IX_GR_GR_CODE] == CAcode:
                return Rec
        return [0, UNKNOWN]

    # ---------------------------------------------------------------------------------------
    def _Get_CA_Code_From_GR_Code(self, GR_Code):
        for Rec in self._GR_Codes_Table:
            if Rec[IX_GR_GR_CODE] == GR_Code:
                return Rec[IX_GR_CA_CODE]
        return 0

    def _Get_CA_Descr(self, CA_Code):
        for Rec in self._CA_Codes_Table:
            if Rec[IX_CA_CA_CODE] == CA_Code:
                return Rec[IX_CA_CA_DESC]
        return ''

    # ---------------------------------------------------------------------------------------
        # TO MODIFY for Top_Queries  ***********
        # =======================================
    # **************************************************************************************
    def Get_GR_CA_desc_From_TRdesc(self, TRDesc):
        GRdesc = ''
        CAdesc = ''
        for Code_Rec in self._TR_Codes_Table:
            if Code_Rec[IX_TR_TR_DESC] == TRDesc:
                Code_GR = Code_Rec[IX_TR_GR_CODE]
                for GrRec in self._GR_Codes_Table:
                    if GrRec[IX_GR_GR_CODE] == Code_GR:
                        GRdesc = GrRec[IX_GR_GR_DESC]
                        CAcode = GrRec[IX_GR_CA_CODE]
                        for CArec in self._CA_Codes_Table:
                            if CArec[IX_CA_CA_CODE] == CAcode:
                                CAdesc = CArec[IX_CA_CA_DESC]
                                break
        return [GRdesc, CAdesc]

    # ---------------------------------------------------------------------------------------
    def _Find_StrToFind_InFullDesc(self, Full_Desc):
        nFound     = 0
        TRcodeList = []    # [Code1, Code2, ...]
        nCount     = 0
        for TRrecord in self._TR_Codes_Table:
            nCount += 1     #  TESTING
            if TRrecord[IX_TR_TR_CODE] == 59:
                pass
            StrToForFind   = TRrecord[IX_TR_TR_STR_TO_FIND]
            StrToFind_List = GetStrList_ForFind(StrToForFind)
            if StrToForFind == '' and Full_Desc == '':
                pass
            if StrToFind_in_Fulldescr(StrToFind_List, Full_Desc):
                nFound += 1
                TRcodeList.append(TRrecord[IX_TR_TR_CODE])
        return TRcodeList

    # ---------------------------------------------------------------------------------------------
    @staticmethod
    def _Clean_Description(raw_desc):
        # 1. Trasforma tutto in maiuscolo
        desc = raw_desc.upper()
        
        # 2. Rimuove i numeri di carta (es: N5167 XXXX XXXX XX57)
        desc.sub(r'CARTA N\d+.*?\d{2,}', '', desc)
        
        # 3. Rimuove sequenze numeriche lunghe (codici operazione, ABI, CAB)
        desc.sub(r'\d{8,}', '', desc)
        
        # 4. Rimuove date e orari (es: 03021116)
        # Spesso le banche attaccano data e ora alla fine dei nomi
        desc.sub(r'\d{4,6}', '', desc)
        
        # 5. Pulisce spazi doppi e caratteri inutili come // o #
        desc = desc.replace('//', ' ').replace('#', ' ')
        desc = ' '.join(desc.split())
        return desc

    # ---------------------------------------------------------------------------------------
    def _Get_Codes_Alpabetically(self, String):
        CapitalStr = String.capitalize()
        Curr_List   = []
        for Rec in self.Tree_Codes_View_List:
            TRdesc = Rec[IX_WIEW_TR_DESCR].capitalize()
            if CapitalStr in TRdesc:
                Curr_List.append(Rec)
            pass
        SortList = sorted(Curr_List, key=itemgetter(IX_WIEW_TR_DESCR))
        return SortList

    # ---------------------------------------------------------------------------------------
    def _Check_Code_For_Update(self, Record):
        CodeToModify = Record[IX_TR_TR_CODE]
        Index = -1
        Found = False
        for RecInTable in self._tTR_Codes_Table:
            Index += 1
            if RecInTable[IX_TR_TR_CODE] == CodeToModify:
                Found = True
                break
        if Found:
            self._tTR_Codes_Table[Index] = Record
            return True
        return False

    # ---------------------------------------------------------------------------------------
    # --------------   update a codes record on data base  ----------------------------------
    def _Update_DB_TR_Record(self, Record):
        self._tTR_Codes_Table = self._TR_Codes_Table
        if not self._Check_Code_For_Update(Record):
            return False, ('Error on updating a '
                           'Transaction code record')
        TR   = Record[IX_TR_TR_CODE]
        GR   = Record[IX_TR_GR_CODE]
        CA   = Record[IX_TR_CA_CODE]
        Desc = Record[IX_TR_TR_DESC]
        StrToFind    = Compact_Descr_String(Record[IX_TR_TR_STR_TO_FIND])
        Full_Descrip = Record[IX_TR_TR_FULL_DESC]

        sql = """UPDATE TRANSACT_CODES SET 
                 GR_Code=?, SP_Code=?, TR_Descr=?, Str_To_Search=?, Str_Full_Descrip=? 
                 WHERE TR_Code==?"""
        parameters = (GR, CA, Desc, StrToFind, Full_Descrip, TR)
        return self._query_execute(CODES_FILE, sql, parameters, CLOSE_DB)

    # ---------------------------------------------------------------------------------------
    # delete "nRow=nnn "  on TRfullDesc and update TRcode record
    def Del_nRow(self):
        nFound = 0
        for Record in self._TR_Codes_Table:
            if Record[IX_TR_TR_CODE] == 382:
                pass
            Full_Desc = Record[IX_TR_TR_FULL_DESC]
            if 'nRow=' in Record[IX_TR_TR_FULL_DESC]:
                RestFullDesc = Full_Desc[5:]
                SPfound   = False
                Index = -1
                for Char in RestFullDesc:
                    Index += 1
                    if not SPfound:
                        if Char == ' ':
                            SPfound = True
                    elif Char == ' ':
                        pass
                    else:
                        strDate = RestFullDesc[Index:Index+10]
                        if not Check_strDate(strDate):
                            break
                        else:
                            nFound += 1
                            NewRecord = Record.copy()
                            NewFull   = strDate + '  - ' + RestFullDesc[Index+11:]
                            NewRecord[IX_TR_TR_FULL_DESC] = NewFull
                            # self.Update_DB_TR_Record(NewRecord)

                            break
                    if Index > 20:
                        break
# ==============================================================================================================
