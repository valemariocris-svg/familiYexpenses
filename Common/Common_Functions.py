# ----------------------------------------------------------------------------#
#               *****     Common_Functions.py      *****                      #
# ----------------------------------------------------------------------------#

from pathlib import Path
from datetime import datetime
from Common.Constants import *

# --------- get  ['Dir_Name', 'Filename']  from a generic path ----------------
def Get_Dir_Name(Full_Name):
    iLastBar = int(Full_Name.rfind("/") + 1)
    return Full_Name[:iLastBar]

def Get_File_Name(Full_Name):
    iLastBar = int(Full_Name.rfind("/") + 1)
    return Full_Name[iLastBar:]

# -----------------------------------------------------------------------------
def Compact_Descr_String(Descr):
    """Clean and normalize string: filter range, collapse spaces, uppercase."""
    if not isinstance(Descr, str):
        return ''

    # Keep only characters 0x1F-0x7D
    filtered = ''.join(ch for ch in Descr if 0x1F <= ord(ch) <= 0x7D)

    # Collapse multiple spaces
    normalized = ' '.join(filtered.split())

    # Return uppercase
    return normalized.upper()

# ---------------------------------------------------------------------------------------
def Gl_Cek_Codes_Name(Full_Filename):
    if Full_Filename == UNKNOWN:
        errMessage = 'FATAL ERROR 5:\nCodes filename unknown\nPlease select a Codes file'
        return False, errMessage
    else:
        Dirname = Get_Dir_Name(Full_Filename)
        filename = Get_File_Name(Full_Filename)
        if len(filename) < LEN_CODES_FILENAME_MIN:
            errMessage = 'Len of Codes filename INCORRECT'
            return False, errMessage
        else:
            iLastBar = int(Full_Filename.rfind("/") + 1)
            strCodes = Full_Filename[(iLastBar - 9):(iLastBar + 11)]
            if strCodes != IDENT_CODES_FILENAME:
                errMessage = 'DBcodes filename ERROR:\n\n'
                errMessage += filename + '\n' + Dirname + '\n\nexpected:  ' + IDENT_CODES_FILENAME
                return False, errMessage
        return True, ''


# ---------------------------------------------------------------------------------------
def Gl_Cek_Xlsx_Name(Full_Filename):
    # /FIDEU/FIDEU_2026/FIDEU_2026-01-06...xlsx
    if Full_Filename == UNKNOWN:
        return False, UNKNOWN

    dirname  = Get_Dir_Name(Full_Filename)
    filename = Get_File_Name(Full_Filename)
    YearFilename = filename[0:10]
    if len(filename) < LEN_XLSX_FILENAME_MIN:
        return True, 'Len of xlsx filename INCORRECT'

    full_path = Path(Full_Filename)
    conto = filename[0:5]
    # .parents[n] ti permette di risalire la struttura (0 è la cartella attuale, 1 è quella sopra, ecc.)
    # Nel tuo caso, per tornare indietro di 2 livelli:
    first_back  = full_path.parents[0]
    conto1      = str(first_back.name)[0:5]
    contoYear1   = str(first_back.name)[0:10]
    second_back = full_path.parents[1]
    conto2      = str(second_back.name)[0:5]
    pass
    if conto == conto1 and conto == conto2:
        if YearFilename == contoYear1:
            return True, ''

    errMessage = 'xlsx filename ERROR:\n\n'
    errMessage += filename + '\n' + dirname + '\n' + conto + '\n' + conto1 + '\n' + conto2
    return True, errMessage

# ---------------------------------------------------------------------------------------
# TRANSACTIONS / Transact_2024.db
def Gl_Cek_Transactions_Name(Full_Filename):
    errMessage = ''
    File_Name = Full_Filename
    if File_Name == UNKNOWN:
        return False, 'Transactions filename unknown\na Transactions file MUST BE SELECTED'
    else:
        filename = Get_File_Name(Full_Filename)
        if len(filename) < LEN_TRANSACT_FILENAME:
            errMessage = 'Len of Transactions filename INCORRECT'
        else:
            #  TRANSACTIONS/TRANSACT_   2024.db
            iLastBar = int(File_Name.rfind("/") + 1)
            Transact_Str_Id = File_Name[(iLastBar - 13):(iLastBar + 9)]
            strYear = filename[9:13]
            if Transact_Str_Id != TRANSACT_ID:
                errMessage = 'Transactions filename ERROR:\n\n'
                errMessage += filename + '\n' + Transact_Str_Id
            else:
                Curr_Year = datetime.now().year  # to max years history setup
                Min_Year  = Curr_Year - 9
                Max_Year  = Curr_Year + 1
                if not (Check_strYear(strYear, Min_Year, Max_Year)):
                    errMessage = 'Transactions Year  not OK:  ' + strYear
    if errMessage != '':
        return False, errMessage
    else:
        return True, ''

# ---------------------------------------------------------------------------------------
def CheckInteger(strInt):
    for Digit in strInt:
        if Digit < '0' or Digit > '9':
            return False
    return True

def Check_strYear(strYear, Min, Max):
    for Digit in strYear:
        if Digit < '0' or Digit > '9':
            return False
    intYear = int(strYear)
    if intYear < Min or intYear > Max:
        return False
    return True


def SetNoZero(Value):
    if type(Value) is float:
        if Value == 0.0:
            return ''
        else:
            return Value
    else:
        return Value

# -----------------------------------------------------------------------------------
def FullDescr_Setup(Desc1, Desc2):
    Len1 = 0
    Len2 = 0
    if type(Desc1) is str:
        Len1 = len(Desc1)
    if type(Desc2) is str:
        Len2 = len(Desc2)
    if not Len1 and not Len2:
        return ''
    Full_Desc = str(Desc1) + ' // ' + str(Desc2)
    return Full_Desc

# -----------------------------------------------------------------------------
def Print_Received_Message(Txtr, Recvr, Request, Values_List):
    if not type(Txtr) == str:
        Txtr = UNKNOWN
        print(f"Print_Rcv_Msg:\nFound unknown Txtr")
    strToPrint = '*** '
    strToPrint += 'TXMTR: '+Txtr+'   RECVR: '+Recvr+'   REQUEST: '+Request
    strToPrint += '   VALUES: ' + str(Values_List)
    # PRINT(strToPrint)

def Get_List_Item(List, Ncol_For_Find, ValueToFind, Ncol_To_Get, default):
    index = -1
    for Rec in List:
        index += 1
        if Rec[Ncol_For_Find] == ValueToFind:
            return Rec[Ncol_To_Get]
    return default

def Get_List_Record(List, Ncol_For_Find, ValueToFind, default):
    index = -1
    for Rec in List:
        index += 1
        Value = Rec[Ncol_For_Find]
        if Value == ValueToFind:
            return Rec
    return default

# -----------------------------------------------------------------------------
def Get_Xlsx_FullMonth(Xlsx_Name):
    # FIDEU_2024_09-1.xlsx
    Filename    = Get_File_Name(Xlsx_Name)
    return Filename[11:13]

# -----------------------------------------------------------------------------
def Get_Transactions_Year(transact_filename):
    if transact_filename is UNKNOWN:
        return 0
    Filename = Get_File_Name(transact_filename)
    return int(Filename[9:13])

# 2024-12-15  2024/12/25
def Check_strDate(String):
    for Char in String:
        if '0' <= Char <='9':
            pass
        elif Char == '-':
            pass
        elif Char == '/':
            pass
        else:
            return False
    return True
# -----------------------------------------------------------------------------
def Get_YearMonthDay(FullDate):
    if FullDate   is None:
        return [2999, 12, 31]
    if not Check_strDate(FullDate):
        return [-1, -1, -1]
    iYear  = int(FullDate[:4])
    iMonth = int(FullDate[5:7])
    iDay   = int(FullDate[8:10])
    return [iYear, iMonth, iDay]

def Calc_Delta_Time(Contabile, Valuta):
    YearMonthDay_Contab = Get_YearMonthDay(Contabile)
    Mont_Init_Day = MONTH_INITDAY[YearMonthDay_Contab[1] - 1]
    Progress_Contab_Day = YearMonthDay_Contab[0] * 365 + Mont_Init_Day + YearMonthDay_Contab[2]

    YearMonthDay_Valuta = Get_YearMonthDay(Valuta)
    Mont_Init_Day       = MONTH_INITDAY[YearMonthDay_Valuta[1] - 1]
    Progress_Valuta_Day = YearMonthDay_Valuta[0] * 365 + Mont_Init_Day + YearMonthDay_Valuta[2]
    Delta = Progress_Contab_Day - Progress_Valuta_Day
    return Delta

# ---------------------------------------------------------------------------------------------
def Set_Month_Day(FullDate, Counts):
    iMonth    = int(FullDate[5:7]) -1
    if Counts == 1:
        MonthName = MONTHS_NAMES_COMPACT[iMonth]
    else:
        MonthName = '     '
    Day       = FullDate[8:10]
    MonthDay_Date = MonthName + ' ' + Day
    return MonthDay_Date

# -------------------------------------------------------------------------------------------------
def get_year_month_day(strDate):    # '2026-09-02-12:00:00
    return strDate[0:10]

# -------------------------------------------------------------------------------------------------
def convert_rcord_toView(template, Rec):
    converted_record = []
    for index in range(0, len(template)):
        if template[index] == SIC:
            converted_record.append(Rec[index])
        elif template[index] == YMD:
            conv_value = get_year_month_day(Rec[index])
            converted_record.append(conv_value)
        elif template[index] == FLOAT_TOSTR:
            conv_value = convert_float_toString(Rec[index])
            converted_record.append(conv_value)
        elif template[index] == INT_TOSTRING:
            conv_value = str(Rec[index])
            converted_record.append(conv_value)
        else:
            return '????'
    return converted_record


# ----------------------------------------------------------------------------#
def TestForSign(Sign, FoundNotZ):
    if Sign and FoundNotZ == 1:
        return '-'
    else:
        return ''


# -------------------------------------------------------------------------------------------------------------
# strVal = '(-)DDD.DD   Called from reading Xlsx Rows
def Convert_Str_To_Float(Value):
# Gestione immediata del None
    if Value is None:
        return 0.0

    try:
        # Questo copre int, float e stringhe numeriche pulite (es: "123.45")
        return float(Value)
    except (ValueError, TypeError):
        # Se la conversione fallisce (es: c'è del testo o simboli strani)
        return 0.0
    finally:
        pass

# -------------------------------------------------------------------------------------------------------------
def Convert_To_Float(Value):    # return always a float (0.00) in case of not number
    Type = type(Value)
    if Type is str:
        return 0.00
    if Value is None:
        return 0.0
    if Type is int or Type is float:
        return float(Value)
    return 0.00

# ---------------------------------------------------------------------------------------
def convert_float_toString(Float):
    if not type(Float) is float:
        return '????'
    # 1. Arrotonda a 1 solo decimale
    rounded_float = round(Float, 1)  # Diventa 0.1
    if rounded_float == 0.0:
        return '  '

    # 2. Formatta a stringa (forzando 1 decimale con '.1f')
    # Il modificatore :.1f garantisce che anche se il numero è 0, diventerà "0.0" e non "."
    eng_format = f"{rounded_float:,.1f} "  # Risultato: "0.1"

    # 3. Trasforma il punto in virgola per l'italiano
    # 2. Il gioco dei tre replace:
    passo1 = eng_format.replace(",", "X")  # Diventa: "1X234.6"
    passo2 = passo1.replace(".", ",")     # Diventa: "1X234,6"
    it_format = passo2.replace("X", ".")  # Diventa: "1.234,6"

    return it_format


# ---------------------------------------------------------------------------------------
def Float_ToString_Setup(Val):
    Digit_List = []
    strValue = ''
    if Val == '' or Val == ' ' or Val == 0.0:
        return ' '
    Value = round(Val)
    AbsValue = abs(Value)
    if AbsValue < 15.0 or AbsValue > 100000.0:
        pass
    mySign = False
    flPositValue = Value

    if Value < 0:
        mySign = True
        flPositValue = -Value
    Intx100_Value = int((flPositValue + 0.005) *100.0)     # Truncated at 2 decimal

    if Intx100_Value >= 10000000000:
        Intx100_Value = 9999999999
    #         10.000.000,00
    Divisor = 1000000000
    for iDigit in range(0,10):
        Significant = int(Intx100_Value / Divisor)
        Digit_List.append(Significant)
        Intx100_Value = Intx100_Value - Significant*Divisor
        Divisor = int(Divisor/10)

    for iDigit in range(0,10):          # create 00.000.000,00
        strValue += str(Digit_List[iDigit])
        if iDigit == 1 or iDigit == 4:
            strValue += '.'
        if iDigit == 7:
            strValue += ','

    strValCompact = ''
    FoundNotZ = 0
    for iChar in range(0, 13):
        CurrChar = strValue[iChar]
        if CurrChar == '.':
            if FoundNotZ:
                strValCompact += '.'
        elif CurrChar == ',':
            break
        elif iChar == 9:
            if CurrChar != '0':
                FoundNotZ += 1
                strValCompact += TestForSign(mySign, FoundNotZ)
                mySign = False
                strValCompact += CurrChar
            else:
                FoundNotZ = 1
                strValCompact += TestForSign(mySign, FoundNotZ)
                mySign = False
                strValCompact += '0'
        else:
            if CurrChar != '0':
                FoundNotZ += 1
                strValCompact += TestForSign(mySign, FoundNotZ)
                mySign = False
                strValCompact += CurrChar
            else:
                if FoundNotZ:
                    strValCompact += CurrChar
                else:
                    strValCompact += ' '
    return strValCompact

# -----------------------------------------------------------------------------
# used on _Checked   and 2 times in Codes_Db
def GetStrList_ForFind(strToFind):
    if strToFind[0:1] != '#':
        return [strToFind]
    strList = []
    index = 0
    nextStr = ''
    for Char in strToFind[index+1:]:
        index +=1
        if Char != '#':
            nextStr += Char
        else:
            strList.append(nextStr)
            nextStr = ''
            if index >= len(strToFind):
                break
    return strList

# -----------------------------------------------------------------------------
 # used on Insert coce in codes Table
def GetStrList_ForFind_Checked(strToFind):
    Len = len(strToFind)
    if Len < 3:
        return ''
    if strToFind.rfind('#') == -1:          # any hashtag in
        return [strToFind]
    else:                                   # hashtag in string
        FirstChar  = strToFind[0:1]
        LastChar   = strToFind[(Len-1):]
        if FirstChar == '#':
            if LastChar != '#':
                return ''
        return GetStrList_ForFind(strToFind)

# -----------------------------------------------------------------------------
def StrToFind_in_Fulldescr(strToFind_List, FullDesc):
    MatchToFind = len(strToFind_List)
    OccurenceIndex = 0
    OccurenceList  = []
    for Item in strToFind_List:
        iOccurience = FullDesc.find(Item)
        if iOccurience == -1:
            break
        else:
            OccurenceList.append(iOccurience)
            OccurenceIndex += 1
    if not OccurenceIndex:
        return False
    else:
        if OccurenceIndex != MatchToFind:
            return False
        CurrIndex = 0
        for Index in OccurenceList:
            if Index < CurrIndex:
                return False
            else:
                CurrIndex = Index
        return True

# -------------------------------------------------------------------------------------
def GetNum_fromString(String):
    if "/" in String:
        return OK, int(String.split('/')[0])
    else:
        return NOK, 9999



# -------------------------------------------------------------------------------------
import glob
import os

def Get_Transactions_Years(Transact_Filename_Path):
    transactions_directory = os.path.dirname(Transact_Filename_Path)

    # 2. Creo il pattern per cercare tutti i file Transact_*.db in QUELLA cartella
    # pattern = os.path.join(transactions_directory, "Transact_*.db")
    pattern = transactions_directory + "/Transact_*.db"

    # 3. Cerco i file sul disco di Linux
    Found_Files = glob.glob(pattern)

    YearList = []
    for path in Found_Files:
        filename = os.path.basename(path)
        year = filename.replace("Transact_", "").replace(".db", "")
        if int(year.isdigit()):
            YearList.append(year)

    YearList.sort(reverse=True)
    return YearList

# -------------------------------------------------------------------------------------
def PRINT(message):
    if PRINT_ENABLED:
        print(message)

# =======================================================================================
