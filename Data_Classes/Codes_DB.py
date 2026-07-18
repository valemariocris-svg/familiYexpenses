# =========================================================================== #
#               -----   Codes_DB.py   -----                                   #
#          it contains all the methods invoked from external                  #
# =========================================================================== #

from Data_Classes.Codes_DB_Private import Codes_DB_Private
from Common.Common_Functions import *

"""
from operator import itemgetter
list_of_lists = [['Urban', 10000000, 200, 3], ['Rural', 5000000, 150, 8], ['Suburban', 8000000, 300, 4]]
sorted_list   = sorted(list_of_lists, key=itemgetter(1)? 0 or 1)
"""

# ---------------------------------------------------------------------------------
class Codes_db(Codes_DB_Private):
    def __init__(self):
        super().__init__()
        self.Dummy = 0

    def Get_Codes_Alpabet(self, String):
        return self._Get_Codes_Alpabetically(String)

    # ----------------------------------------------------------------------------------------
    def Get_MultiCodes_Match_List(self):
        return self._Multi_Codes_Matching_List

    # ----------------------------------------------------------------------------------------
    def Load_Codes_Tables(self):
        return self._Load_Codes_Tables()

    # -----------------------------   TR Codes   ----------------------------------
    def Get_Codes_Table(self):
        return self._TR_Codes_Table

    def Get_TR_Codes_Full(self, TRcode):
        if TRcode == -1:
            return self._TR_Codes_Full      # <<<<<<<<<<<<<<<<<<<<-------------------- 
        else:
            for TRfull in self._TR_Codes_Full:
                if TRfull[IX_TR_FULL_TR_CODE] == TRcode:
                    return TRfull
            return []

    def Get_TR_Rec_From_Code(self, TRcode):
        for TRrec in self._TR_Codes_Full:
            if TRrec[IX_TR_TR_CODE] == TRcode:
                return TRrec
        return[]

    def Get_TrDesc_FromCode(self, TRcode):
        for Rec in self._TR_Codes_Table:
            if Rec[IX_TR_TR_CODE] == TRcode:
                return Rec[IX_TR_TR_DESC]
        return "Unkown"

    def Get_strToFind_FromCode(self, TRcode):
        for Rec in self._TR_Codes_Table:
            if Rec[IX_TR_TR_CODE] == TRcode:
                return Rec[IX_TR_TR_STR_TO_FIND]
        return "Unkown"


    def Get_TRcodes_Table_Length(self):
        return len(self._TR_Codes_Table)

    # -----------------------------   GR Codes   ----------------------------------
    def Get_GR_Codes_Table(self):
        return self._GR_Codes_Table

    def Get_GR_Codes_Ordered(self):
        return self._GR_Codes_Ordered

    def Get_GRdescr_Ordered_List(self):
        return self._GRdescr_Ordered_List

    def Get_GR_RecFull_From_GRcode(self, GRcode):
        NotFound_Record = [0, UNKNOWN, 0, UNKNOWN]
        if not type(GRcode) is int:
            return NotFound_Record
        GRrecFound = []
        CArecFound = []
        for GRrec in self._GR_Codes_Table:
            if GRrec[IX_GR_GR_CODE] == GRcode:
                GRrecFound = GRrec
                break
        if not GRrecFound:
            return NotFound_Record

        CAcode = GRrecFound[IX_GR_CA_CODE]
        for CArec in self._CA_Codes_Table:
            if CArec[IX_CA_CA_CODE] == CAcode:
                CArecFound = CArec
                break
        if not CArecFound:
            return [GRrecFound[IX_GR_GR_CODE], GRrecFound[IX_GR_GR_DESC], CAcode, UNKNOWN]
        return [ GRrecFound[IX_GR_GR_CODE],
                 GRrecFound[IX_GR_GR_DESC],
                 GRrecFound[IX_GR_CA_CODE],
                 CArecFound[IX_CA_CA_DESC], ]

    # -----------------------------   CA Codes   ----------------------------------
    def Get_CA_Codes_Table(self):
        return self._CA_Codes_Table

    def Get_CA_Codes_Ordered(self):
        return self._CA_Codes_Ordered

    def Get_CAdescr_Ordered_List(self):
        return self._CAdescr_Ordered_List

    def Get_CA_Code_From_Desc(self, CAdesc):
        for CArec in self._CA_Codes_Table:
            if CArec[IX_CA_CA_DESC] == CAdesc:
                return CArec[IX_CA_CA_CODE]
        return  0

    def Get_CAdescr(self, CAcode):
        for CArec in self._CA_Codes_Table:
            if CArec[IX_CA_CA_CODE] == CAcode:
                return CArec[IX_CA_CA_DESC]
        return  UNKNOWN

    # --------------------------------------------------------------------------------------------
    def Get_Extraordinary_List(self):
        self._Extraorinary_TRcode_List = []
        for TRrec in self._TR_Codes_Table:
            GRcode = TRrec[IX_TR_GR_CODE]
            CAcode = self._Get_CA_Code_From_GR_Code(GRcode)
            if CAcode == EXTRAORDINARY_CAT_CODE:
                self._Extraorinary_TRcode_List.append(TRrec[IX_TR_TR_CODE])
        return self._Extraorinary_TRcode_List


    # ---------------------------------------------------------------------------------------
    def Check_If_Code_Exist(self, TRcode):
        sql = "SELECT EXISTS(SELECT 1 FROM TRANSACT_CODES WHERE TR_Code = ?)"
        status, data = self._query_execute(CODES_FILE, sql, (TRcode,), CLOSE_DB)
        if not status:
            return False, 'Fatal error on checking code exists\n'
        return True, ''

    # ------------------------------------------------------------------------------------------- #
    #    ***   Codes in 1-10.000 are the normal code with StrToFind.                              #
    #          All Xlsx Records with Full description that matches StrToFind                      #
    #          are  automatically selected for insert in transactions DB                          #
    #    ***   Codes  > 10.000   are generic code that can be assigned manually to                #
    #          any Xlsx Record. The assignement must be made for each Xlsx Record                 #
    # ------------------------------------------------------------------------------------------- #
    def Get_New_Code(self, Table) -> tuple[bool, str|int]:
        status = False
        data   = []
        if Table == STANDARD_CODE:
            sql_query = "SELECT MAX(TR_Code) FROM TRANSACT_CODES WHERE TR_Code < ?"
            status, data = self._query_execute(CODES_FILE, sql_query, (10000,), CLOSE_DB)

        elif Table == GENERICCODE:
            sql_query = "SELECT MAX(TR_Code) FROM TRANSACT_CODES WHERE TR_Code > ?"
            status, data = self._query_execute(CODES_FILE, sql_query, (10000,), CLOSE_DB)

        elif Table == GROUP_CODE:
            status, data = self._query_execute(CODES_FILE, "SELECT MAX(GR_Code) FROM GROUP_CODES", (), CLOSE_DB)

        elif Table == CATEG_CODE:
            status, data = self._query_execute(CODES_FILE, "SELECT MAX(CA_Code) FROM CAT_CODES", (), CLOSE_DB)

        # risultato sarà una lista di tuple, es: [(9998,)] oppure [(None,)]
        if status and data[0][0] is not None:
            found_code = data[0][0]
            print(f"Il codice trovato è: {found_code}")
            return True, found_code
        else:
            return False, "None code found withh SELECT"

    # -----------------------   Add  transaction code record         ------------------------
    def Add_DB_TR_Record(self, Record):
        TR        = Record[IX_TR_TR_CODE]
        GR        = Record[IX_TR_GR_CODE]
        CA        = self._Get_CA_Code_From_GR_Code(IX_GR_CA_CODE)
        Desc      = Record[IX_TR_TR_DESC]
        StrToFind = Compact_Descr_String(Record[IX_TR_TR_STR_TO_FIND])
        Full_Descrip = Record[IX_TR_TR_FULL_DESC]

        sql = "INSERT INTO TRANSACT_CODES (TR_Code, GR_Code, SP_Code, TR_Descr, Str_To_Search, Str_Full_Descrip) VALUES (?, ?, ?, ?, ?, ?)"
        parameters = (TR, GR, CA, Desc, StrToFind, Full_Descrip,)

        status, data = self._query_execute(CODES_FILE, sql, parameters, CLOSE_DB)
        if not status:
            return False, data
        return True, ''

    # ----------        delete the transaction codes record         -------------------------
    def Delete_DB_TR_Record(self, TRcode):
        sql_query = """DELETE FROM TRANSACT_CODES WHERE TR_Code = ?"""
        return self._query_execute(CODES_FILE, sql_query, (TRcode,), CLOSE_DB)

    # --------------   update a codes record on data base  ----------------------------------
    def Update_DB_TR_Record(self, Record):          # public
        TR   = Record[IX_TR_TR_CODE]
        GR   = Record[IX_TR_GR_CODE]
        CA   = Record[IX_TR_CA_CODE]
        Desc = Record[IX_TR_TR_DESC]
        StrToFind    = Compact_Descr_String(Record[IX_TR_TR_STR_TO_FIND])
        Full_Descrip = Record[IX_TR_TR_FULL_DESC]

        sql = """UPDATE TRANSACT_CODES SET 
                 GR_Code=?, SP_Code=?, TR_Descr=?, Str_To_Search=?, Str_Full_Descrip=? 
                 WHERE TR_Code = ?"""
        return self._query_execute(CODES_FILE, sql, (GR, CA, Desc, StrToFind, Full_Descrip, TR), CLOSE_DB)


    # ----------------------------------------------------------------------------------
    def Add_CA_Record(self, CAcode, CAdesc):
        sql = """INSERT INTO CATEGORY_CODES (CA_Code, CA_Descr) VALUES (?, ?)"""
        parameters = (CAcode, CAdesc)
        return self._query_execute(CODES_FILENAME, sql, parameters, CLOSE_DB)


    def Del_CA_Record(self, CAcode):
        sql = """ DELETE FROM CATEGORY_CODES WHERE CA_Code = ?"""
        parameters = (CAcode,)
        return self._query_execute(CODES_FILE, sql, parameters)

    # ----------------------------------------------------------------------------------
    def Add_GR_Record(self, GRcode, GRdesc, CAcode):
        sql = """INSERT INTO GROUP_CODES (GR_Code, GR_Descr, CA_Code) VALUES (?, ?, ?)"""
        parameters = (GRcode, GRdesc, CAcode)
        return self._query_execute(CODES_FILE, sql, parameters, CLOSE_DB)

    def Del_GR_Record(self, GRcode):
        sql = """DELETE FROM GROUP_CODES WHERE GR_Code = ?"""
        parameters = (GRcode,)
        return self._query_execute(CODES_FILENAME, sql, parameters, CLOSE_DB)

    def Update_GR_CA_Rec(self, GRcode, GRdesc, CAcode, CAdesc):
        sql = "UPDATE GROUP_CODES SET GR_Descr=?, CA_Code=?, CAdesc=? WHERE GR_Code = ?"
        parameters = (GRdesc, CAcode, CAdesc, GRcode)
        return self._query_execute(CODES_FILE, sql, parameters, CLOSE_DB)

    def Check_if_stringToFind_matches(self, strToFind_list, TR_code):
        for record in self._TR_Codes_Table:
            if record[IX_TR_TR_CODE] != TR_code:
                FullDesc = record[IX_TR_TR_FULL_DESC]
                if StrToFind_in_Fulldescr(strToFind_list, FullDesc):
                    return True, f"{strToFind_list}  matches also in\ncode: {record[IX_TR_TR_CODE]}"
        return False, ''
# ==============================================================================================================
