# ------------------------------------------------------------#
#           *****     Constants.py      *****                 #
#        Contains Constants Definition   23-11-11(!)          #
#                         last version   26-06-18             #
# ------------------------------------------------------------#

# ------------------   Constants  for Widgets  ----------------
BACKGND   ='#567688'    # for all widgets
FORGND    = "white"     # for all   " "
PRINT_ENABLED = True    # Enable printing

DUAL_DISPLAY  = False
if DUAL_DISPLAY:
    MAIN_WIND_GEOMETRY     = '330x310+1580+1'     # '330x310+1700+10'
    # SETTINGS_GEOMETRY      = '330x400+1580+390'   # 330x400+1700+370
    # TOP_MNGR_GEOMETRY      = '660x1000+1200+10'   # 660x1000+2100+10
    # TOP_VIEW_GEOMETRY      = '890x1000+2000+10'
    # TOP_VIEW_GEOM_REDUCED  = '890x1000+150+200'
    # TOP_VIEW_MESS_GEOMETRY = '450x470+600+10'
    # TOP_GRCODES_GEOMETRY   = '830x1000+1600+10'
    # TOP_XLSX_VIEW_GEOMETRY = '820x1000+1300+10'   # '820x1000+2040+10'
    # TOP_INSERT_GEOMETRY    = '740x1000+2200+10'   # '610x1000+2870+10'
    # TOP_TR_VIEW_GEOMETRY   = '820x1000+3000+10'
    #                             1 Frame               2 Frames           3 Frames
    # TOP_QUERY_GEOMETRY     = ['550x1000+3200+10', '1090x1000+640+10', '1200x1000+20+10']
else:
    MAIN_WIND_GEOMETRY     = '380x410+1500+10'
    SETTINGS_GEOMETRY      = '330x390+1580+360'
    TOP_MNGR_GEOMETRY      = '890x1010+870+10'     # 1590
    TOP_VIEW_GEOMETRY      = '820x1000+20+10'      # Top View Codes
    TOP_VIEW_GEOM_REDUCED  = '820x655+100+10'
    TOP_GRCODES_GEOMETRY   = '830x1000+210+10'
    TOP_XLSX_VIEW_GEOMETRY = '820x1000+200+10'      # Top View Xlsx
    TOP_VIEW_MESS_GEOMETRY = '450x520+600+10'
    TOP_INSERT_GEOMETRY    = '740x1000+50+10'
    TOP_TR_VIEW_GEOMETRY   = '940x1000+500+10'      # top View Transactions
    TOP_TRANSACT_VERIF_GEO = '1200x1000+200+10'     # Top Verify   XLSX and Transactions

XY_TO_HIDE   = 10000   # Hide widget
COL_MUSTARD  = '#749D5F'

# =========================================================== #
#       CHAT:   echanging   DATA between classes              #
# =========================================================== #
MAIN_WIND           = 'Main_Window     '
MODULES_MNGR        = 'Modules Manager'       # Top_Level Launcher
FILES_NAMES_MNGR    = 'Files_Names_Mngr'    # .txt .db .xlsx files names manager
CODES_CLASS         = 'Codes_Class     '    # Codes Manager
XLSX_CLASS          = 'Xlsx_Class      '    # xlsx File Manager
TRANSACT_CLASS      = 'Transact_Class  '    # Transactions DB Manager
DATA_CLASS          = 'Data_Class'          # Class derived from all Data_Classe

# TOP_SETTINGS        = 'Top_Settings    '      # Toplevel for Settings
TOP_CODES_MNGR      = 'Top_Codes_Mngr  '      # Toplevel TR Codes Manager
TOP_CODES_VIEW      = 'Top_Codes_View  '      # Toplevel Codes Viewer
TOP_GR_MNGR         = 'Top_GR_Manager  '      # Toplevel GR Codes Manager
TOP_XLSX_VIEW       = 'Xlsx Rows View  '      # Toplevel  xlsx File Viewer
TOP_INS             = 'Top_Ins_Tansact '      # Toplevel Insert Transactions on DB
TOP_VIEW_TRANSACT   = 'Top View Transact'     # Topleveel view transactions
TOP_QUERY           = 'Top_Queries     '      # Toplevel for Queries
TOP_VIEW_MESS       = 'Top show messages '    # Toplevel to shaw messages
TOP_TRANSACT_VERIFY = 'Top Transactions Verify'
ANY                 = 'All Modules     '

# Checkes to be made before a Tolevel launch
CEK_CODES_DB     = 'Check codes DB OK  '
CEK_XLSX_LIST    = 'Check xlsx lists   '
CEK_TOP_MNGR     = 'Check Top Codes Mngr'
CEK_TOP_INSERT   = 'Check Top_Insert    '
CEK_TRANSACTIONS = 'Check Transactions Db'

IX_TOP_CLASS = 0
IX_TOP_NAME  = 1

# Requests Code for Messages between classes
CODE_TO_CLOSE        = 'Close window'
CODE_SHOW_PARTIC_LIST= 'Show Participants List'     # Show Chat Participants List

VIEW_SELECTIONS     = 'View selections on Main_Wind'
CODE_CLK_ON_TR_CODES= 'Clicked Row with TR Codes'   # Clkd on Codes_DB Record Values = [TRcode]
CODES_DB_INSERT     = 'Code database inserted'
CODES_DB_DELETE     = 'Code database deleted'
CODES_DB_UPDATED    = 'Code database updated'
CODES_DB_LOADED     = 'Codes database loaded'

CODE_CLIK_ON_XLSX   = 'Clkded On_Xlsx_Tree  '       # Clkd on Xlsx Row  Value = [nRow, Data_Valuta]
CODE_CLEAR_FOCUS    = 'Clear Focus   '
XLSX_UPDATED        = 'Xlsx updated'

# =========================================================== #
#             FILES  PARAMETERS                               #
# =========================================================== #
UNKNOWN = 'unknown'
NEW     = 'New file created'
YES     = 'YES'
NO      = 'NO'
CHANGE  = 'CHANGE'
EXIT    = 'EXIT'

CATEG       = 'Category '
GROUP       = 'Group'
ADD         = 'Add '
DEL         = 'Delete '
UPDT_GR_CAT = "Update Group and Categ"
MAX_CODE    = 10000

NONE   = 'None'
OK     = 'OK'
NOK    = 'NOK'
LOADED = 'Loaded'   # it means that the file or Db are Loaded but can contains error
EMPTY  = 'Empty'
MULTI  = 'Multiple Row Match'
FILE_FAILS = 'Transactions file NOT found'

STRTOFIND   = 'String to find'
TRDESC      = 'TR code description'
GROUPSEL    = 'Select a group'
CATDESC     = 'Category'

IX_CODES_LOADED      = 0
IX_XLSX_LISTS_LOADED = 1
IX_TRANSACT_LOADED   = 2

# =========================================================== #
#             QUERIES  constants                              #
# =========================================================== #
ALL_MONTHS  = 'all Months'
ALL_RECORDS = 'all Records'

SELTR      = 'select a code'
ALLTR      = 'tutti i movimenti'
ALL_CODES  = 'tutti i codici'
ALL_GROUPS = 'tutti i gruppi'
ALL_CAT    = 'tutte le categorie'
EXTRAORD_EXCL = 'escl. straord.'
EXTRAORD_INCL = 'inclusi straord.'

XLSX_AND_TRANSACT = 'Transacts and Xlsx'
VIEW_ALL_LARGE    = 'All Large'             # to select frame type in Tpo_CodesView
VIEW_ALL_REDUC    = 'All Reduced'
VIEW_QUERY_REDUC  = 'Query Reduced'

JAN   = 'Gennaio'
FEB   = 'Febbraio'
MARCH = 'Marzo'
APR   = 'Aprile'
MAY   = 'Maggio'
JUNE  = 'Giugno'
JULY  = 'Luglio'
AUG   = 'Agosto'
SEPT  = 'Settembre'
OCT   = 'Ottobre'
NOV   = 'Novembre'
DEC   = 'Dicembre'

#        Delta      0  +31  +28  +31   +30   +31  +30   +31   +31   +30  +31   +30
#        Index      0    1    2    3     4     5    6     7     8     9   10    11
#                   J    F    M    A     M     J    J     A     S     O    N     D
MONTH_INITDAY   = [ 0,  31,  59,  90,  120,  151, 181,  212,  243,  273, 304,  334 ]


HEAD_MONTH_NAM  = (JAN, FEB, MARCH, APR, MAY, JUNE, JULY, AUG, SEPT, OCT, NOV, DEC, ALL_MONTHS, ALL_RECORDS)
MONTHS_NAMES    = (JAN, FEB, MARCH, APR, MAY, JUNE, JULY, AUG, SEPT, OCT, NOV, DEC)
MONTHS_NAMES_COMPACT = ('Gen ','Feb ','Mar ','Apr ','Mag ','Giu ','Lug ','Ago ','Set','Ott ','Nov ','Dic ')
ONE_MONTH     = 'un mese '
TWO_MONTHS    = ' 2 mesi '
THREE_MONTHS  = ' 3 mesi '
FOUR_MONTHS   = ' 4 mesi '
SIX_MONTHS    = ' 6 mesi '
TWELVE_MONTHS = '12 mesi '

MONTH_INT     = {JAN: 1, FEB:2, MARCH:3, APR:4, MAY:5, JUNE:6, JULY:7, AUG:8, SEPT:9, OCT:10, NOV:11, DEC:12}

TOT_MONTH_INT = {ONE_MONTH:1, TWO_MONTHS:2, THREE_MONTHS:3, FOUR_MONTHS:4, SIX_MONTHS:6, TWELVE_MONTHS:12}

LIST_TOT_12 = [ONE_MONTH, TWO_MONTHS, THREE_MONTHS, FOUR_MONTHS, SIX_MONTHS, TWELVE_MONTHS]
LIST_TOT_6  = [ONE_MONTH, TWO_MONTHS, THREE_MONTHS, FOUR_MONTHS, SIX_MONTHS]
LIST_TOT_4  = [ONE_MONTH, TWO_MONTHS, THREE_MONTHS, FOUR_MONTHS]
LIST_TOT_3  = [ONE_MONTH, TWO_MONTHS, THREE_MONTHS]
LIST_TOT_2  = [ONE_MONTH, TWO_MONTHS]
LIST_TOT_1  = [ONE_MONTH]
QUERIES_TOT_DICT = {JAN:  LIST_TOT_12, FEB: LIST_TOT_6,  MARCH: LIST_TOT_6, APR: LIST_TOT_6,
                    MAY: LIST_TOT_6,   JUNE: LIST_TOT_6, JULY:LIST_TOT_6,   AUG: LIST_TOT_4,
                    SEPT: LIST_TOT_4,  OCT: LIST_TOT_3,  NOV: LIST_TOT_2,   DEC: LIST_TOT_1}

TOP_QUERY_GEOMETRY = ['700x1000+1090+10', '1210x1000+590+10', '1710x1000+90+10']

# ----------------------------------   queries :  trees, months, geomety  -----------------------------------
# Frames in view :   Frame1   Frame1-Frame2  Frame1-Frame2 -Frame3
#                          Frame geometry index per total Months   (see TOP_QUERY_GEOMETRY)
QUERIES_GEOMETRY_INDEX  = {ONE_MONTH:0, TWO_MONTHS:1, THREE_MONTHS:2, FOUR_MONTHS:1, SIX_MONTHS:2, TWELVE_MONTHS:2}

# Widgets (Text, Button, Combo) position for  1, 2 or 3 frames
#                         0 - one Frame                      1 - two Frames             2 - three Frames
#                         -------------------------------    ------------------------   ----------------------
#                         x1                         Widg    x1   x2             Widg    x1   x2   x3  Widg
QUERIES_FRAMES_POS_X = [ [10, XY_TO_HIDE, XY_TO_HIDE, 530], [10, 520, XY_TO_HIDE, 1030], [10, 520, 1030, 1540] ]

WIDGETS_POS_Y        = [450, 880, 1310]
#                          total frames per total months
QUERIES_NR_FRAMES    = {ONE_MONTH:1, TWO_MONTHS:2, THREE_MONTHS:3, FOUR_MONTHS:2, SIX_MONTHS:3, TWELVE_MONTHS:3}

#                          total months per frame
QUERIES_NR_MONTHS_BY_TREE = {ONE_MONTH:1, TWO_MONTHS:1, THREE_MONTHS:1, FOUR_MONTHS:2, SIX_MONTHS:2, TWELVE_MONTHS:4}

IX_QUERY_CONTO    = 0   # Row on transactions database
IX_QUERY_CONTAB   = 1
IX_QUERY_VALUTA   = 2
IX_QUERY_DESCR    = 3
IX_QUERY_ACCRED   = 4
IX_QUERY_ADDEB    = 5
IX_QUERY_IDENT    = 6


IX_TREE_ROW    = 0      # Tree number of columns to view
IX_TREE_COLMN  = 1
IX_TREE_HEAD   = 2
IX_TREE_ANCHOR = 3
IX_TREE_WIDTH  = 4

NO_FOCUS       = -1

VIEW_BY_CODE        = 'vis. per codice'
VIEW_SEARCH         = 'vis. per stringa ricerca'
VIEW_BYNAME         = 'vis. per nome'
GENERIC_BYCODE      = 'vis. per codice generico'
GENERIC_BYNAME      = 'vis. generici per nome'
VIEW_EXTRAORDOIN    = 'vis. mov. straordinari'
VIEW_STRTOSERCH_LEN = 'vis. per lungh. stringa ricerca'

GENERICCODE         = 'GENERICCODE'
STANDARD_CODE       = 'STANDARD_CODE'
CODES_VIEW_SEL      = [VIEW_BY_CODE, VIEW_BYNAME, VIEW_SEARCH, GENERIC_BYCODE, GENERIC_BYNAME,
                       VIEW_STRTOSERCH_LEN, VIEW_EXTRAORDOIN]

TRANSACT_VIEW_ALL          = 'View all transactions'
TRANSACT_VIEW_CONTAB_ASC   = 'View transact Contab ASC'
TRANSACT_VIEW_NORMAL_CODE  = 'normal code transactions'
TRANSACT_VIEW_GENERIC      = 'generic code transactions'
TRANSACT_VIEW_AS_IS        = 'View transactions as is'
TRANSACT_VIEW_SEL = [TRANSACT_VIEW_CONTAB_ASC, TRANSACT_VIEW_NORMAL_CODE,
                     TRANSACT_VIEW_GENERIC, TRANSACT_VIEW_AS_IS ]

# =========================================================== #
#             DATA BASES  STRUCTURE                           #
# =========================================================== #
CHECK_DBCODES_LOADED  = 1
CHECK_TEMT_DBCODES    = 2

# ***************************************************************** #
EXTRAORDINARY_CAT_CODE = 7  # ***    DO NOT CHANGE  THIS CODE ***** #
# ***************************************************************=* #

#   -----  Database  Codes_DB_yyy-mm-dd.db -----------------
NORMAL_CODE          = 'New Transaction Cod < 10.000'
GENERIC_CODE_INIT    = int(10000)       #  NEVER NEVER CHANGE this CONSTANT variable
TRANSACT_CODES_TABLE = 'Transactions Codes Table'
GROUPS_CODES_TABLE   = 'Groups Codes Table'
CATEG_CODES_TABLE    = 'Categories Codes Table'

LEN_CODES_FILENAME_MIN  = 22
LEN_XLSX_FILENAME_MIN   = 17
IDENT_CODES_FILENAME= 'Codes_DB/Codes_DB_20'
GENERICCODEstr      = 'GENERICCODE'
IX_TR_TR_CODE       = 0  # UNIC TR CODE
IX_TR_GR_CODE       = 1
IX_TR_CA_CODE       = 2  # selected from GROUPS_TABLE
                         # do not use this index in Code recods, it is something
                         # to have the category of a Code it should be search
                         # on the Group of TRcode through IX_GR_CA_CODE.
                         # the chain is  TRcode--> GRcode --> CAcode
IX_TR_TR_DESC       = 3
IX_TR_TR_STR_TO_FIND= 4
IX_TR_TR_FULL_DESC  = 5  # 2024-01-01  - '''''' // ''''''''

IX_TR_FULL_TR_CODE     = 0
IX_TR_FULL_GR_CODE     = 1
IX_TR_FULL_CA_CODE     = 2
IX_TR_FULL_TR_DESC     = 3
IX_TR_FULL_GR_DESC     = 4
IX_TR_FULL_CA_DESC     = 5
IX_TR_FULL_STR_TO_FIND = 6
IX_TR_FULL_FULL_DESC   = 7     # The full description of Row when the new code was created

MAX_TR_CODE_NUM = 100
MAX_GR_CODE_NUM = 50

# TABLE  GROUP_CODES
IX_GR_GR_CODE = 0
IX_GR_GR_DESC = 1
IX_GR_CA_CODE = 2

# TABLE  CATEGORY_CODES
IX_CA_CA_CODE = 0
IX_CA_CA_DESC = 1

IX_XLSX_CONTO    = 0    # used on Data.Get_Full_Xlsx_Transact_Ident
IX_XLSX_YEAR     = 1
IX_XLSX_MONTH    = 2
IX_TRANSACT_YEAR = 3

IX_XLSX_NROW     = 0
IX_XLSX_CONTAB   = 1
IX_XLSX_VALUTA   = 2
IX_XLSX_DESC1    = 3
IX_XLSX_CREDIT   = 4
IX_XLSX_DEBIT    = 5
IX_XLSX_DESC2    = 6

IX_XLSX_WITH_ROW     = 0
IX_XLSX_WITH_CONTAB  = 1
IX_XLSX_WITH_VALUTA  = 2
IX_XLSX_WITH_ACCR    = 3
IX_XLSX_WITH_DEBIT   = 4
IX_XLSX_WITH_TRDESC  = 5
IX_XLSX_WITH_FULLDES = 6
IX_XLSX_WITH_TRCODE  = 7


#   -----  Database  /TRNSACTIONS/Transact_2024.db  ----------
TRANSACTIONS = 'TRANSACTIONS'
TRANSACT     = 'TRANSACT'
TRANSACT_ID  = 'TRANSACTIONS/Transact_'
LEN_TRANSACT_FILENAME= 16
IX_TRANSACT_IDENT    = 0
IX_TRANSACT_CONTO    = 1
IX_TRANSACT_CONTAB   = 2
IX_TRANSACT_VALUTA   = 3
IX_TRANSACT_ACCRED   = 4
IX_TRANSACT_ADDEB    = 5
IX_TRANSACT_TR_DESC  = 6
IX_TRANSACT_TR_CODE  = 7
IX_TRANSACT_FULL_DESC= 8  # DESC1 / DESC2

FIDEU       = 'FIDEU'      # Fideuram Account    Must be 5 chars length
FLASH       = 'FLASH'      # Flash Card          Must be 5 chars length
FIDFLH      = 'FID+FLH' # FIDEU/FLASH/POSTA   Doesn't matter
POSTA       = 'POSTA'      # Poste Italiane      Must be 5 chars length
AMBRA       = 'AMBRA'      # Credit Card Ambra   Must be 5 chars length
CONTO_LIST  = [FIDEU, FLASH, FIDFLH, POSTA, AMBRA]
CONTO_RED   = {FIDEU:'F', FLASH:'L', POSTA:'P', AMBRA:'C'}

CONTABILE   = 'contabile'
VALUTA      = 'valuta'

# ALL_REC     = 'all records'
STEP        = 'Inserisci uno per volta'
CONTINUOUS  = 'Inserisci tutti i movimenti'
NREC        = 'Insert total rows'
CONTINUE_LIST = [STEP, CONTINUOUS, NREC]

NOTASK        = 'Not Ask Dialog'
ASK           = 'Ask Dialog'
STOP          = 'Stop'
NOSELECT      = 'nessuna scelta'

# -----------------------------------    Codes     ---------------------------------------------------------
#                         0       1        2         3         4        5        6        7        8
# View Codes List       TRcode TR_Desc   GR_Desc   CA_Desc   StrToFind
#_Records_ToInsert_List Ident  Conto    Contab    Valuta    TRdesc    Accred   Addeb   TRcode  Full_Desc
# Transact DB List      Ident  Conto    Contab    Valuta    TR_Desc   Accred   Addeb   TRcode  FullDesc
# On Top_Queries  Only TRcode is used:
#                 TRdesc GRdesc CAdesc are refreshed as in Codes Tables.
#

# =====================================          XLSX             ========================================= #
#                            0      1       2      3       4         5       6                              #
# XLS_Row_List           : nRow   Contab  Valuta  Des1      Accr    Addeb   Des2      as in xlsx File       #
# XLS_Row_Compact        : nRow   Contab  Valuta  Des1Comp  Accr    Addeb   Des2Comp                        #
# _Wihtout_Code_Tree_List: nRow   Contab  Valuta  Accr      Addeb   FullDes             7          8        #
# _With_Code_Tree_List   : nRow   Contab  Valuta  TR_Desc   Accred  Addeb   TRcode  RowFullDes              #
# Xlsx_Rows_MultiMatch_List : [Row, [TRrec, .., TRrec], .., Row, [] ]                                       #
#                                                                                                           #
# Query_View_List        : Date    TR_Desc   Accred    Addeb                                                #
# ========================================================================================================= #
IX_TOT_ROWS_OK           = 0
IX_TOT_ROWS_WITH_CODE    = 1
IX_TOT_ROWS_WITHOUT_CODE = 2

Len_Xlsx_Filename_Min = 18
# XLS_Row_List          (as in xlsx spreadsheet)
IX_ROW_NROW   = 0
IX_ROW_CONTAB = 1
IX_ROW_VALUTA = 2
IX_ROW_DESCR1 = 3
IX_ROW_ACCRED = 4
IX_ROW_ADDEB  = 5
IX_ROW_DESCR2 = 6

# all Xlsx Rows         (Compact)
IX_ROW_COMP_NROW    = 0
IX_ROW_COMP_CONT    = 1
IX_ROW_COMP_VAL     = 2
IX_ROW_COMP_ACCR    = 3
IX_ROW_COMP_ADDEB   = 4
IX_ROW_COMP_FULLDES = 5  # (Descr1/Descr2

# List_WithoutCode      (only without code)
IX_NO_CODE_NROW       = 0
IX_NO_CODE_CONTAB     = 1
IX_NO_CODE_VALUTA     = 2
IX_NO_CODE_ACCRED     = 3
IX_NO_CODE_ADDEB      = 4
IX_NO_CODE_FULL_DESCR = 5     # The Fulll_Desc of Row inserted in Transact_Db

# List_WithCode         (only with code)
IX_WITH_CODE_NROW       = 0
IX_WITH_CODE_CONTAB     = 1
IX_WITH_CODE_VALUTA     = 2
IX_WITH_CODE_ACCRED     = 3
IX_WITH_CODE_ADDEB      = 4
IX_WITH_CODE_TR_DESCR   = 5
IX_WITH_CODE_TR_CODE    = 6
IX_WITH_CODE_FULL_DESCR = 7  # The Fulll_Desc of Row inserted in Transact_Db

# List_View_Codes
IX_WIEW_TR_CODE    = 0
IX_WIEW_TR_DESCR   = 1
IX_WIEW_GR_DESCR   = 2 # these constants are not used
IX_WIEW_CA_DESCR   = 3 # because GRdesc CAdesc StrToFind are
IX_WIEW_STR_TOFIND = 4 # as on Codes Tables



# =============================================================
#             WIDGETS  CONSTANTS                              =
# =============================================================
# XY_TO_HIDE = 10000 # setted higher for use
LAB_BLUE     = 1
LAB_FILE_SEL = 2
LAB_ERR      = 3
VIEW_MESSAGE = 'View Message'

BTN_DEF_EN  = 1      # Button Default greeen     Enabled
BTN_COL_EN  = 2      # Button Colored (brown)
BTN_BOL_EN  = 3      # Button green bold
BTN_DEF_DIS = 4      # Button Default greeen     Disabled
BTN_COL_DIS = 5      # Button Colored (brown)
BTN_BOL_DIS = 6      # Button green bold
BTN_MSG     = 7      # Button for Message

BTN_DISAB    = "Disable buttons"
BTN_RESET    = "Buttn reset"
BTN_DEL      = "Delete Rec"
BTN_UPDT     = "Update Rec"
BTN_ADD      = "Add code"
BTN_ADD_GEN  = "Add generic"
BTN_INS      = "Insert"
ONLY_TRCODE  = "test only Tr code"
BOTH_TR_GR   = "test Tr and Gr data"
CLK_NOCODE   = "click on No Code frame"
CLK_WITHCODE = "click on with code frame"

MSG_BOX_INFO     = 'Info message'
MSG_BOX_ASK      = 'Ask Yes No Nomessage'
MSG_BOX_ASK_YNCH = 'Ask Yes No Change'
MSG_BOX_ASK_EXIT = 'Ask Yes No Exit'
MSG_BOX_ERR      = 'Err message'

TXT_ENAB      = 'TXT_ENAB'       # Text enable     Black on Mustard
TXT_DISAB     = 'TXT_DISAB'      # Text disabled   White on Light Blue
TXT_DIS_BLACK = 'TXT_DIS_BLACK'  # Text Disabled   Black on Light Blue
TXT_MSG_WHITE = 'TXT_MSG_WHITE'  # Text for MsgBox White on Mustard
TXT_MSG_ERR   = 'TXT_MSG_ERR'    # Text for MsgBox Red on Mustard


# ----------------------  List of Controls  To Check on XLS rows Data ------------------------------------------
INTEGER       = 'Integer'
NOT_INT       = 'String'
NUMERIC       = 'Numeric'
DATE          = 'Date'
STRING        = 'String'
VAL_DATE      = 'Valuta'
CONTAB_DATE   = 'Contabile'
DIRECT_NOCODE = -1

LIST_FOR_XLSX_ROW_CONTROL = [
    [IX_ROW_NROW,   INTEGER],
    [IX_ROW_CONTAB, DATE],    [IX_ROW_VALUTA, DATE],   [IX_ROW_DESCR1, STRING],
    [IX_ROW_ACCRED, NUMERIC], [IX_ROW_ADDEB, NUMERIC], [IX_ROW_DESCR2, STRING]]

VIEW_TOTAL_INLIST = 'View total in check list'
VIEW_NOT_INLIST   = 'View total not in check list'

# types of conversion for displaying in frames
SIC          = 'sic'   # no conversion
YMD          = 'year_month day' # convert datetime in year-month
INT_TOSTRING = 'integer to str'
FLOAT_TOSTR  = 'float to string'    # convert float to str 1.234,56

SELECTIONS_DIR_NAME    = '/home/mario/bExp_Selections'
SELECTIONS_FULL_NAME   = '/home/mario/bExp_Selections/Selections'
DICTIONARY_FULL_NAME   = '/home/mario/bExp_Selections/Sel_dictionary.json'

DEFAULT_INIT_DIR       = '/home/mario'

# -------------------------------------------------------------------------------
# used on File_Dialog and in _sql_execute for selecting database
CODES_FILE    = 'Codes file'    # for File_Dalog
XLSX_FILE     = 'Xlsx file'
TRANSACT_FILE = 'Transact file'

# -------------------------------------------------------------------------------
CODES_FILENAME       = 'codes_filename'     # for selections dictionary names
XLSX_FILENAME        = 'xlsx_filename'
TRANSACT_FILENAME    = 'transact_filename'
CODES_DIRECTORY      = 'Codes directory'
XLSX_DIRECTORY       = 'Xlsx directory'
TRANSACT_DIRECTORY   = 'Transactions directory'

QUERY_CONTO          = 'query_conto'
QUERY_START_MONTH    = 'query_start_month'
QUERY_TOT_MONTHS     = 'query_total_months'
QUERY_VAL_CONT_DATE  = 'query_val_cont_date'
QUERY_CODE_SEL       = 'query_code_selection'
QUERY_GROUP_SEL      = 'query_group_selection'
QUERY_CATEGORY_SEL   = 'query_category_selection'

CODES_VIEW_MODE      = 'codes_view_mode'
TRANSACT_INSERT_MODE = 'transact_insert_mode'

CLOSE_DB  = True
KEEP_OPEN = False

Dict_Keys_List = [
    CODES_FILENAME, XLSX_FILENAME, TRANSACT_FILENAME, CODES_DIRECTORY, XLSX_FILENAME, TRANSACT_DIRECTORY,
	CODES_VIEW_MODE, TRANSACT_INSERT_MODE,  QUERY_CONTO, QUERY_START_MONTH,
    QUERY_TOT_MONTHS, QUERY_VAL_CONT_DATE, QUERY_CODE_SEL, QUERY_GROUP_SEL, QUERY_CATEGORY_SEL,
    CODES_VIEW_MODE, TRANSACT_INSERT_MODE]


#  -------------------------------------------
Default_selections_dictionary  = {
    CODES_FILENAME:         UNKNOWN,
    XLSX_FILENAME:          UNKNOWN,
    TRANSACT_FILENAME:      UNKNOWN,
    CODES_DIRECTORY:        UNKNOWN,
    XLSX_DIRECTORY:         UNKNOWN,
    TRANSACT_DIRECTORY:     UNKNOWN,
    #
    CODES_VIEW_MODE:        VIEW_BYNAME,
    TRANSACT_INSERT_MODE:   STEP,

    QUERY_CONTO:            FIDEU,
    QUERY_START_MONTH:      JAN,
    QUERY_TOT_MONTHS:       ONE_MONTH,
    QUERY_VAL_CONT_DATE:    VALUTA,
    QUERY_CODE_SEL:         ALL_CODES,
    QUERY_GROUP_SEL:        ALL_GROUPS,
    QUERY_CATEGORY_SEL:     ALL_CAT,
    #
}
# ===========================================================================================================
