# ---------------------------------------------------------------------------------- #
#            *****     Super_Top_Codes_Mngr.py     *****                             #
#                                                                                    #
#      here  are contained the two Frames  without/with code                         #
#      List_Rows_WithoutCode : nRow    Date      FullDesc                            #
#      List View Codes       : TR_Code  TR_Desc   GR_Desc  CA_Desc  StrToSearch      #
#                                                                                    #
#                        VIEW  DELETE  ADD  UPDATE                                   #
#                             on the child                                           #
# ---------------------------------------------------------------------------------- #
from Common.Common_Functions import *
from Chat import Ms_Chat
from Data_Classes.Transact_DB import Data_Manager
from Top_Expenses.Modules_Manager import Modul_Mngr

from Widgt.Widgets import *
from Widgt.Tree_Widg import *
from Widgt.Canvas_Frame import *

# -------------------------------------------------------------------------------------------------------------
class Super_Top_Mngr(tk.Toplevel):
    def __init__(self, Child_ClkNoCode, Child_ClkWithCode):
        super().__init__()
        self.Chat          = Ms_Chat
        self.Data          = Data_Manager
        self.Mod_Mngr      = Modul_Mngr
        self.Chat.Attach([self, TOP_CODES_MNGR])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)

        self.resizable(False, False)
        self.geometry('5x5+10000+10000')
        self.title('*****     Transactions  Codes  Manager     *****')
        self.configure(background=BACKGND)

        self.TR_Code     = None
        self.GR_Code     = None
        self.CA_Code     = None
        self.TR_Desc     = None
        self.GR_Desc     = None
        self.CA_Desc     = None
        self.FullDesc    = None

        self.Generic_Codes = []

        self.Child_ClkNoCode   = Child_ClkNoCode
        self.Child_ClkWithCode = Child_ClkWithCode
        self.View_Without_Code = True
        self.Rows_NoCode_List  = self.Data.Get_WithoutCodeList()
        self.Row_WithoutCode   = None  # it is the Row clicked on Frame_NoCodes
        self.Rows_WitCode_List = self.Data.Get_Rows_WithCod_List()

        # ----------------------   Frames   -------------------------------------------------------------------
        self.Frame_NoCodes = TheFrame(self,   10, 20, self.Clk_OnTree_NoCodes)
        self.Frame_NoCodes_Setup()
        self.Frame_WithCodes = TheFrame(self, 10, 20, self.Clk_OnTree_WithCodes)
        self.Frame_WithCodes_Setup()

        # ***************************     C A N V A  S    *****************************************************
        self.Canv_CodData = CreateCanvas(self, 10, 640, 380, 130)
        TheLable(self.Canv_CodData, LAB_BLUE, 60, 1, 26, "impostazioni dati per il codice")

        self.Canv_Tr_Mngr = CreateCanvas(self, 450, 820, 380, 80)
        TheLable(self.Canv_Tr_Mngr, LAB_BLUE, 90, 1, 25, " gestione Db  movimenti   ")

        # --------------------------------   Groups    C O M B O            -----------------------------------
        self.StrVar1    = tk.StringVar()
        self.GR_Combo1  = TheCombo(self.Canv_CodData, self.StrVar1, XY_TO_HIDE, XY_TO_HIDE, 1, 1, [], '', self.Clk_Combo)

        # ------------  TEXT Boxes   and   Btn_SelCode  used  on  Child  --------------------------------------
        self.Txt_StrFullDesc1 = TheText(self,              TXT_ENAB,      10, 583,  95, 2, '')   # not in canvas
        self.Txt_StrToFind1   = TheText(self.Canv_CodData, TXT_ENAB,      20, 30,   40, 1, STRTOFIND)
        self.Txt_TR_Code1     = TheText(self.Canv_CodData, TXT_DIS_BLACK, 20, 65,    5, 1, '0')
        self.Txt_TR_Desc1     = TheText(self.Canv_CodData, TXT_ENAB,      82, 65,   33, 1, TRDESC)
        #
        self.Txt_GR_Code1     = TheText(self.Canv_CodData, TXT_DIS_BLACK,  20, 100,  5, 1, '0')
        self.Txt_CA_Code1     = TheText(self.Canv_CodData, TXT_DIS_BLACK,  20, 134,  5, 1, '0')
        self.Txt_CAdesc1      = TheText(self.Canv_CodData, TXT_DIS_BLACK,  82, 134, 33, 1, CATDESC)
        #
        self.Btn_SelGeneric    = TheButton(self.Canv_Tr_Mngr, BTN_DEF_DIS, 485, 735, 19, '', None)

    # ---------------------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Tx_Request([TOP_CODES_MNGR, [ANY], CODE_TO_CLOSE, []])
        self.Chat.Detach(TOP_CODES_MNGR)
        self.destroy()

    # ==========================  T R E E     Without  Codes   ========================================
    def Frame_NoCodes_Setup(self):
        Nrows     = 25
        nColToVis = 6
        Headings  = ['#0', 'Row', 'Contab  ', 'Valuta  ', 'Accred  ', 'Addeb  ', 'Full Description']
        Anchor    = ['c',   'w',    'c',      'c',        'e',        'e',        'w']
        Width     = [0,      50,     80,       80,         70,         70,         490]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_NoCodes.Tree_Setup(Form_List)

    # -------------------------------------------------------------------------------------------------
    def Clk_OnTree_NoCodes(self, Values):
        #  [nRow, Contab, Valuta, Accred, Addeb, FullDes
        Row      = int(Values[IX_NO_CODE_NROW])
        Valuta    = Values[IX_NO_CODE_VALUTA]
        FullDesc  = Values[IX_NO_CODE_FULL_DESCR]
        self.Txt_StrFullDesc1.Set_Text(Valuta + '  - ' + FullDesc)

        flAccred  = Convert_Str_To_Float(Values[IX_NO_CODE_ACCRED])
        flAddeb   = Convert_Str_To_Float(Values[IX_NO_CODE_ADDEB])
        intValues = [Row, Values[IX_NO_CODE_CONTAB], Values[IX_NO_CODE_VALUTA],
                     flAccred, flAddeb, Values[IX_NO_CODE_FULL_DESCR]]
        self.Row_WithoutCode = intValues
        self.Btn_SelGeneric.Btn_Enable()
        self.Frame_WithCodes.Clear_Focus()
        self.Child_ClkNoCode()

    # ==========================  T R E E     With  Codes   ===========================================
    def Frame_WithCodes_Setup(self):
        self.Frame_WithCodes.Frame_Title('  ')
        Nrows     = 25
        nColToVis = 7
        # Headings = ['#0',  'Row ', 'Contab ', 'Valuta ', 'Description',  'Accred ', 'Addeb ', 'Code ']
        # Anchor   = ['c',   'w',     'c',       'c',       'w',            'e',       'e',      'c'    ]
        # Width    = [ 0,     50,      80,        80,        230,            70,        70,       50    ]
        Headings = ['#0',  'Row ', 'Contab ', 'Valuta ', 'Accred  ', 'Addeb  ', 'Description ', 'Code ']
        Anchor   = ['c',   'w',     'c',       'c',      'e',        'e',       'w',           'c'    ]
        Width    = [ 0,     50,      80,        80,       70,         70,        440,           50    ]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_WithCodes.Tree_Setup(Form_List)

    # -------------------------------------------------------------------------------------------------
    def Clk_OnTree_WithCodes(self, Values):
        #  Row    Date   Descrip   Accred   Addeb   TR_Code
        nRow      = int(Values[IX_WITH_CODE_NROW])
        self.TR_Code    = int(Values[IX_WITH_CODE_TR_CODE])
        Descrip = Values[IX_WITH_CODE_TR_DESCR]
        self.Frame_NoCodes.Clear_Focus()
        if int(nRow) < 1 or not Descrip:
            return
        self.Frame_NoCodes.Clear_Focus()
        self.View_Descr_Text(self.TR_Code, self.GR_Combo1)
        self.View_Descr_Text(self.TR_Code, self.GR_Combo1)

        # self.Btn_SelGeneric.Btn_Disable()
        self.Frame_NoCodes.Clear_Focus()
        self.Child_ClkWithCode()

    # -------------------------------------------------------------------------------------------------
    def View_Frames(self, Total_WthoutCode):
        if Total_WthoutCode == 0:               # 0 No Rows Without codes
            self.View_Without_Code = False
            self.Frame_WithCodes.Frame_View()
            self.Frame_NoCodes.Frame_Hide()
        elif Total_WthoutCode > 0:              # some Rows Without codes
            self.View_Without_Code = True
            self.Frame_WithCodes.Frame_Hide()
            self.Frame_NoCodes.Frame_View()
        elif Total_WthoutCode < 0:              # -1 view frames as selected
            if self.View_Without_Code:
                self.Frame_WithCodes.Frame_Hide()
                self.Frame_NoCodes.Frame_View()
                self.Frame_NoCodes.Clear_Focus()
            else:
                self.Frame_WithCodes.Frame_View()
                self.Frame_NoCodes.Frame_Hide()
                self.Frame_WithCodes.Clear_Focus()

    # -------------------------------------------------------------------------------------------------
    # invoked on  Delete  Add  and Update  Record
    def Frames_Refresh(self):
        self.Mod_Mngr.Load_xlsx_Mngr(TOP_CODES_MNGR)
        self.Mod_Mngr.Init_CodesMngr_and_Insert(TOP_CODES_MNGR)
        self.Load_Trees()
        self.View_Frames(-1)

    # -------------------------------------------------------------------------------------------------
    def Load_Trees(self):
        With_Code_List   = self.Data.Get_WithCodeList()
        XlsxFilename     = Get_File_Name(self.Data.Get_sel_dictionary_value(XLSX_FILENAME))
        Total            = self.Data.Get_Total_Rows()
        Total_WthoutCode = Total[IX_TOT_ROWS_WITHOUT_CODE]
        Total_WithCode   = Total[IX_TOT_ROWS_WITH_CODE]
        self.Generic_Codes = self.Data.Get_Generic_Codes_List()
        Generic_Len = self.Generic_Codes[0]

        TitleNoCode  = '   ' + XlsxFilename + '       senza codice:  ' + str(Total_WthoutCode)
        TitleNoCode += '   con codice:  ' +  str(Total[IX_TOT_ROWS_WITH_CODE]) + '   '

        TitleWith    = '   ' + XlsxFilename + '       con codice:  ' + str(Total_WithCode)
        TitleWith   += '    senza codice:  ' + str(Total_WthoutCode) + '   '

        self.Frame_NoCodes.Frame_Title(TitleNoCode)
        self.Frame_WithCodes.Frame_Title(TitleWith)

        self.Frame_NoCodes.Load_Row_Values(self.Data.Get_WithoutCodeList())
        self.Frame_WithCodes.Load_Row_Values(With_Code_List)
        self.View_Frames(Total_WthoutCode)

    # -------------------------------------------------------------------------------------------------
    def Clk_Combo(self, GRdesc):
        GRrec = Get_List_Record(self.Data.Get_GR_Codes_Table(), IX_GR_GR_DESC, GRdesc, [])
        if not GRrec:
            return
        CAcode = GRrec[IX_GR_CA_CODE]
        CArec = Get_List_Record(self.Data.Get_CA_Codes_Table(), IX_CA_CA_CODE, CAcode, -1)
        if not CArec:
            return
        self.Txt_GR_Code1.Set_Text(GRrec[IX_GR_GR_CODE])
        self.Txt_CA_Code1.Set_Text(CArec[IX_CA_CA_CODE])
        self.Txt_CAdesc1.Set_Text(CArec[IX_CA_CA_DESC])
        self.Txt_CAdesc1.Set_Text(CArec[IX_CA_CA_DESC])

    # -------------------------------------------------------------------------------------------------
    def View_Descr_Text(self, TRstrCode, GRcombo):
        self.TR_Code       = int(TRstrCode)
        TR_Full_Code = self.Data.Get_TR_Codes_Full(self.TR_Code)      # <<<<<<<<<<-----------------

        TRfullRec    = Get_List_Record(TR_Full_Code, IX_TR_FULL_TR_CODE, self.TR_Code, [])
        if not TRfullRec:
            return
        self.Txt_TR_Code1.Set_Text(self.TR_Code)
        self.Txt_GR_Code1.Set_Text(TRfullRec[IX_TR_FULL_GR_CODE])
        self.Txt_CA_Code1.Set_Text(TRfullRec[IX_TR_FULL_CA_CODE])
        self.Txt_TR_Desc1.Set_Text(TRfullRec[IX_TR_FULL_TR_DESC])
        self.Txt_StrToFind1.Set_Text(TRfullRec[IX_TR_FULL_STR_TO_FIND])

        self.Txt_TR_Code1.Set_Text(self.TR_Code)
        self.Txt_GR_Code1.Set_Text(TRfullRec[IX_TR_FULL_GR_CODE])
        self.Txt_CA_Code1.Set_Text(TRfullRec[IX_TR_FULL_CA_CODE])
        self.Txt_TR_Desc1.Set_Text(TRfullRec[IX_TR_FULL_TR_DESC])
        self.Txt_StrToFind1.Set_Text(TRfullRec[IX_TR_FULL_STR_TO_FIND])

        self.Txt_TR_Code1.Set_Text(self.TR_Code)
        self.Txt_GR_Code1.Set_Text(TRfullRec[IX_TR_FULL_GR_CODE])
        self.Txt_CA_Code1.Set_Text(TRfullRec[IX_TR_FULL_CA_CODE])
        self.Txt_TR_Desc1.Set_Text(TRfullRec[IX_TR_FULL_TR_DESC])
        self.Txt_StrToFind1.Set_Text(TRfullRec[IX_TR_FULL_STR_TO_FIND])
        self.Txt_StrFullDesc1.Set_Text(TRfullRec[IX_TR_FULL_FULL_DESC])

        self.Txt_CA_Code1.Set_Text(TRfullRec[IX_TR_FULL_CA_CODE])
        self.Txt_CAdesc1.Set_Text(TRfullRec[IX_TR_FULL_CA_DESC])

        GRdesc = TRfullRec[IX_TR_FULL_GR_DESC]
        GRcombo.SetSelText(GRdesc)

    # -------------------------------------------------------------------------------------------------
    def Clear_Text_Widg(self, Full):
        if Full:
            self.Txt_StrFullDesc1.Set_Text('')
        self.Txt_StrToFind1.Set_Text(STRTOFIND)
        self.Txt_TR_Desc1.Set_Text(TRDESC)
        self.Txt_CAdesc1.Set_Text(CATDESC)

        self.Txt_TR_Code1.Set_Text('0')
        self.Txt_GR_Code1.Set_Text('0')
        self.Txt_CA_Code1.Set_Text('0')

        self.Txt_TR_Code1.Set_Text('0')
        self.Txt_GR_Code1.Set_Text('0')
        self.Txt_CA_Code1.Set_Text('0')

        self.GR_Combo1.SetSelText(GROUPSEL)
    # =================================================================================================
