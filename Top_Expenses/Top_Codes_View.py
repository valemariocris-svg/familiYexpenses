# --------------------------------------------------------------------------- #
#                   ***  Top_Codes_View.py   ***                              #
#   List_Transact_Codes : TRcode  TRDesc  GRdesc  CAdesc  StrToSearch         #
# --------------------------------------------------------------------------- #

from operator import itemgetter
# list_of_lists = [['Urban', 10000000, 200, 3], ['Rural', 5000000, 150, 8], ['Suburban', 8000000, 300, 4]]
# sorted_list = sorted(list_of_lists, key=itemgetter(1)? 0 or 1)

from Top_Expenses.Modules_Manager import Modul_Mngr
from Chat import Ms_Chat
from Data_Classes.Transact_DB import Data_Manager

from Widgt.Dialogs import Print_Received_Message
from Widgt.Tree_Widg import *
from Widgt.Widgets import TheButton, TheText, TheCombo

# ---------------------------------------------------------------------------------------
class Top_View_Codes(tk.Toplevel):
    # List is []       for Full Codes Database large frame
    # [VIEW_ALL_REDUC] for Full Codes Database reduced frame
    # [TRdesc List]    for Query TRcodes list  reduced frame
    def __init__(self, List):
        super().__init__()
        self.Chat     = Ms_Chat
        self.Data     = Data_Manager
        self.Mod_Mngr = Modul_Mngr
        self.Chat.Attach([self, TOP_CODES_VIEW])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)

        self.resizable(True, True)
        self.title('*****     Transactions Codes     ***** ')
        self.configure(background=BACKGND)

        self.Geometry     = TOP_VIEW_GEOMETRY
        self.Dummy        = 0
        self.Codes_List_Reduced = List  # reduced list for selection TRcode on Query or full Table
        self.Codes_List        = None   # as in Codes Table
        self.Cod_List_NameSort = None   # by Code
        self.Cod_List_DescSort = None   # by Description
        self.Cod_List_StrSort  = None   # by String to find
        self.Cod_List_StrLengt = None   # by String Length 
        self.Groups_Table      = None   # as in Groups table

        self.Categ_Table       = None   # as in Category table
        self.Cat_List_DescSort = None   # by Description
        self.Frame_Type         = None

        if not List:
            self.Frame_Type    = VIEW_ALL_LARGE
        else:
            self.Frame_Type    = List[0]
            pass

        if self.Frame_Type    == VIEW_QUERY_REDUC:   # VIEW_QUERY_REDUC reduced list for Queries
            self.nRows        = 20
            self.Widg_PosY    = 510
            self.Geometry     = TOP_VIEW_GEOM_REDUCED
        elif self.Frame_Type  == VIEW_ALL_REDUC:     # VIEW_ALL_REDUC  All Codes but Reduced Geometry
            self.nRows        = 20
            self.Widg_PosY    = 510
            self.Geometry     = TOP_VIEW_GEOM_REDUCED
            pass
        else:                                       # VIEW_ALL_LARGE (default)All Codes + Max Geometry
            self.nRows     = 37
            self.Widg_PosY = 850
            self.Geometry  = TOP_VIEW_GEOMETRY
        self.geometry(self.Geometry)

        self.View_Type  = self.Data.Get_sel_dictionary_value(CODES_VIEW_MODE)
        self.Combo_View = self.View_Type

        # ----------------------------------    B U T T O N S     ---------------------------------
        self.Txt_StrSerch = TheText(self, TXT_DISAB,   580, self.Widg_PosY-35, 26, 4, '')
        self.Txt_FullDesc = TheText(self, TXT_DISAB,    10, self.Widg_PosY-35, 69, 4, '')
        self.View_StrVar  = tk.StringVar()
        self.Combo_Widgt  = TheCombo(self, self.View_StrVar, 320, self.Widg_PosY+105, 31, 19,
                                     CODES_VIEW_MODE, self.Combo_View , self.Clk_OnCombo)
        self.Btn_Groups   = TheButton(self, BTN_DEF_EN,  10, self.Widg_PosY+100, 14,  'show groups ', self.Clk_GR_Mngr)
        self.Btn_Load     = TheButton(self, BTN_DEF_EN,  10, self.Widg_PosY+60, 14,  'reload ', self.ReloadCodes)
        self.Txt_Alphab   = TheText(self,   TXT_ENAB,   160, self.Widg_PosY+65, 16 , 1, 'wxyz')
        self.Btn_Alphab   = TheButton(self, BTN_DEF_EN, 160, self.Widg_PosY+100, 14,  'alphabetically', self.Find_Aplhabet)
        self.Btn_Exit     = TheButton(self, BTN_DEF_EN, 650, self.Widg_PosY+100, 14, '  E X I T ', self.Call_OnClose)

        self.Create_Lists()
        # ---------------------------------    T R E E   of  Codes    -----------------------------
        self.Frame_Codes = TheFrame(self,  10,  10, self.Clk_OnTree_Codes)
        self.Frame_Codes_Setup()
        self.Frame_Codes.Frame_Hide()

        self.Load_List_Selected()

    # ---------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_CODES_VIEW)
        self.destroy()
        return

    # ---------------------------------------------------------------------------------------------
    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Value):
        Print_Received_Message(Transmitter_Name, TOP_CODES_MNGR, Request_Code, Value)
        if Request_Code == CODE_TO_CLOSE:              # Close
            self.Call_OnClose()

        elif Request_Code == CODE_CLEAR_FOCUS:         # Clear Focus
            self.Frame_Codes.Clear_Focus()

        elif Request_Code == CODES_DB_INSERT or Request_Code == CODES_DB_DELETE:
            self.Create_Lists()
            Title = '   ' + str(len(self.Codes_List)) + '   Transactions  Codes   '
            self.Frame_Codes.configure(text=Title)
            self.Load_List_Selected()

        elif Request_Code == CODES_DB_UPDATED:
            TRcode = Value[IX_TR_TR_CODE]
            TrFull  = self.Data.Get_TR_Codes_Full(TRcode)
            TRdesc  = self.Data.Get_TrDesc_FromCode(TRcode)
            GRdesc = TrFull[IX_TR_FULL_GR_DESC]
            CAdesc = TrFull[IX_TR_FULL_CA_DESC]
            Rec_View = [Value[IX_TR_TR_CODE], TRdesc, GRdesc, CAdesc, Value[IX_TR_TR_STR_TO_FIND]]
            self.Frame_Codes.Update_Tree_Values(Rec_View)

        elif Request_Code == CODES_DB_DELETE:
            self.Create_Lists()
            self.Load_List_Selected()

    # ---------------------------------------------------------------------------------------------
    def ReloadCodes(self):
        self.Create_Lists()
        self.Load_List_Selected()
        pass

    # ---------------------------------------------------------------------------------------------
    def Find_Aplhabet(self):
        myString = self.Txt_Alphab.Get_Text(STRING)
        Alphab_List = self.Data.Get_Codes_Alpabet(myString)
        pass
        self.Frame_Codes.Load_Row_Values(Alphab_List)

    # ---------------------------------------------------------------------------------------------
    def Clk_GR_Mngr(self):
        self.Mod_Mngr.Top_Launcher(TOP_GR_MNGR, TOP_CODES_MNGR, [])

    # ---------------------------------------------------------------------------------------------
    def Set_Focus_On_Tcode(self, TRcode):
        Index = -1
        for Rec in self.Frame_Codes.Loaded_List:
            Index +=1
            if Rec[IX_WIEW_TR_CODE] == TRcode:
                self.Frame_Codes.Set_List_For_Focus(Index)
                break

    # ------------------------   T R E E   of  TRcodes  Setup       -------------------------------
    def Frame_Codes_Setup(self):
        self.Frame_Codes.destroy()
        self.Frame_Codes = TheFrame(self, 10, 10, self.Clk_OnTree_Codes)
        Title = '   ' + str(len(self.Codes_List)) + '   Transactions  Codes   '
        self.Frame_Codes.configure(text=Title)
        Nrows       = self.nRows
        nColToVis = 5
        Headings  = ['#0', 'Code', 'Transaction', "Group", 'Category', 'String To Find']
        Anchor    = ['c',  'c',    'w',           'w',     'w',        'w']
        Width     = [ 0,    60,     200,           140,     120,        250]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_Codes.Tree_Setup(Form_List)

    # ---------------------------------------------------------------------------------------------
    def Clk_OnTree_Codes(self, Values):
        TRcode           = int(Values[IX_WIEW_TR_CODE])
        StrToFind        = Values[IX_WIEW_STR_TOFIND]
        Full_TR_RecList  = self.Data.Get_TR_Codes_Full(TRcode)
        TRfullDesc       = Full_TR_RecList[IX_TR_FULL_FULL_DESC]
        self.Txt_FullDesc.Set_Text(TRfullDesc)
        self.Txt_StrSerch.Set_Text(StrToFind)
        self.Chat.Tx_Request([TOP_CODES_VIEW, [ANY], CODE_CLK_ON_TR_CODES, Full_TR_RecList])

    # ---------------------------------------------------------------------------------------------
    #  Code  Transaction  StrToFind  FullDescription
    def Clk_OnTree_FullDesc(self, Values):
        self.Txt_StrSerch.Set_Text(str(Values[2]))
        self.Txt_FullDesc.Set_Text(str(Values[3]))

    # ---------------------------------------------------------------------------------------------
    def Create_Tree_Codes_View_List_FromTRdesc_List(self):
        self.Codes_List = []
        for TR_Rec_InViewList in self.Data.Tree_Codes_View_List:
            TrDesc = TR_Rec_InViewList[IX_WIEW_TR_DESCR]
            if TrDesc in self.Codes_List_Reduced:
                self.Codes_List.append(TR_Rec_InViewList)
                pass

    # ---------------------------------------------------------------------------------------------
    def Create_Lists(self):
        if self.Frame_Type == VIEW_QUERY_REDUC:
            self.Create_Tree_Codes_View_List_FromTRdesc_List()
        else:
            self.Codes_List = self.Data.Tree_Codes_View_List
        self.Cod_List_NameSort = sorted(self.Codes_List, key=itemgetter(IX_WIEW_TR_DESCR))
        self.Cod_List_StrSort = sorted(self.Codes_List, key=itemgetter(IX_WIEW_STR_TOFIND))
        self.Cod_List_StrLengt = sorted(self.Codes_List, key=lambda x: len(x[IX_WIEW_STR_TOFIND]))

    # ----------------------------------------------------------------------------------------------
    def Clk_OnCombo(self, Value):
        self.Txt_StrSerch.Set_Text('')
        self.Txt_FullDesc.Set_Text('')
        self.View_Type = Value

        self.Data.Update_key_dictionary(CODE_CLK_ON_TR_CODES, Value)
        self.Data.Update_key_dictionary(CODES_VIEW_MODE, Value)
        self.Chat.Tx_Request([TOP_CODES_VIEW, [MAIN_WIND], VIEW_SELECTIONS, []])
        self.Load_List_Selected()

    # ----------------------------------------------------------------------------------------------
    def Load_List_Selected(self):
        ListTo_Load = []
        self.Frame_Codes_Setup()
        self.Frame_Codes.Frame_View()

        if self.View_Type == VIEW_BYNAME:
            ListTo_Load = self.Cod_List_NameSort

        elif self.View_Type == VIEW_BY_CODE:
            ListTo_Load = self.Codes_List

        elif self.View_Type == VIEW_SEARCH:
            ListTo_Load = self.Cod_List_StrSort

        elif self.View_Type == GENERIC_BYCODE:
            ListTo_Load = self.Create_GenericCode_List()
        
        elif self.View_Type == GENERIC_BYNAME:
            ListTo_Load = self.Create_GenericCode_List_Ord()
            pass

        elif self.View_Type == VIEW_STRTOSERCH_LEN:
            pass
            # ListTo_Load = self.Create_StrToSearch_List()
        elif self.View_Type == VIEW_EXTRAORDOIN:
            ListTo_Load = self.Create_Extraordin_List()

        self.Frame_Codes.Load_Row_Values(ListTo_Load)

    # ----------------------------------------------------------------------------------------------
    def Create_GenericCode_List(self):
        Cod_List_Ord_Code = []
        GenericCode_List = []
        for Rec in self.Codes_List:
            TrCode = Rec[IX_TR_TR_CODE]
            if TrCode >= GENERIC_CODE_INIT:
                GenericCode_List.append(Rec)
            Cod_List_Ord_Code = sorted(GenericCode_List, key=itemgetter(IX_WIEW_TR_CODE))  
        return Cod_List_Ord_Code

    # ----------------------------------------------------------------------------------------------
    def Create_GenericCode_List_Ord(self):
        GenericCode_List  = []
        Cod_List_Ord_Name = []
        for Rec in self.Codes_List:
            TrCode = Rec[IX_TR_TR_CODE]
            if TrCode >= GENERIC_CODE_INIT:
                GenericCode_List.append(Rec)
            Cod_List_Ord_Name = sorted(GenericCode_List, key=itemgetter(IX_WIEW_TR_DESCR))  
        return Cod_List_Ord_Name

    # ----------------------------------------------------------------------------------------------
    def Create_Extraordin_List(self):
        Extraorinary_List = []
        for Rec in self.Codes_List:
            TrCode = Rec[IX_TR_TR_CODE]
            TrFull = self.Data.Get_TR_Codes_Full(TrCode)
            CaCode = TrFull[IX_TR_FULL_CA_CODE]
            if CaCode == EXTRAORDINARY_CAT_CODE:
                Extraorinary_List.append(Rec)
        if self.Frame_Type == VIEW_ALL_REDUC:
            Cod_List_Ord_Extra = sorted(Extraorinary_List, key=itemgetter(IX_WIEW_TR_DESCR))
            return Cod_List_Ord_Extra
        else:
            Cod_List_Ord_Code = sorted(Extraorinary_List, key=itemgetter(IX_WIEW_TR_CODE))
            return Cod_List_Ord_Code


# *************************************************************************************************
